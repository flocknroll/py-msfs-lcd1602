import logging
import requests
import argparse
import json

from time import sleep
from simconnect import SimConnect, PERIOD_VISUAL_FRAME

from py_msfs_lcd1602.models.api import MSFSDataList, MSFSData



parser = argparse.ArgumentParser("MSFS to LCS service")
parser.add_argument("--api-host", default="http://192.168.1.25:8081")

if __name__ == "__main__":
    params = parser.parse_args()

    sc = None
    while not sc:
        try:
            sc = SimConnect()
        except OSError as oe:
            logging.error(oe)
            sleep(1)

    dd = sc.subscribe_simdata(
        [
            "INDICATED ALTITUDE",
            "AIRSPEED INDICATED",
            "AIRSPEED MACH",
            "VERTICAL SPEED"
        ],
        # request an update every ten rendered frames
        period=PERIOD_VISUAL_FRAME,
        interval=30,
    )

    latest = 0
    headings = None

    try:
        while True:
            sc.receive(timeout_seconds=1)

            changed = dd.simdata.changedsince(latest)

            logging.info(dict(dd.simdata))
            logging.info(changed)

            data = [MSFSData(name = k, value = v) for k, v in changed.items()]
            model = MSFSDataList(data = data)

            requests.post(params.api_host, model.model_dump_json())

            latest = dd.simdata.latest()
    finally:
        sc.Close()