import logging
import requests
import argparse
import json
import time

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
            "VERTICAL SPEED",
            "VARIOMETER RATE",
            "PLANE ALTITUDE"
        ],
        # request an update every ten rendered frames
        period=PERIOD_VISUAL_FRAME,
        interval=30,
    )

    latest = 0
    headings = None

    last_alt = {
        "value": 0,
        "time": time.time()
    }

    try:
        while True:
            sc.receive(timeout_seconds=1)
            received_time = time.time()
            changed = dd.simdata.changedsince(latest)

            logging.info(dict(dd.simdata))
            logging.info(changed)

            data = [MSFSData(name = k, value = v) for k, v in changed.items()]

            if "PLANE ALTITUDE" in dd.simdata:
                plane_alt = dd.simdata["PLANE ALTITUDE"]
                calculated_vs = (plane_alt - last_alt["value"]) / (received_time - last_alt["time"]) * 60.0
                last_alt = {
                    "value": plane_alt,
                    "time": received_time
                }
                data.append(MSFSData(name = "CALCULATED_VS", value = calculated_vs))
            
            model = MSFSDataList(data = data)

            if len(data):
                requests.post(f"{params.api_host}/update_data", model.model_dump_json())

            latest = dd.simdata.latest()
    finally:
        sc.Close()