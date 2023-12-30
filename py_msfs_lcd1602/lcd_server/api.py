import zmq
import uvicorn
import argparse
import logging
import json
import pendulum

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer
from joserfc.jws import deserialize_compact

from py_msfs_lcd1602.models.api import MSFSDataList

app = FastAPI()

parser = argparse.ArgumentParser("LCD1602 controller API")
parser.add_argument("--zmq-port", default=5555)
parser.add_argument("--http-port", default=8081)
parser.add_argument("--pub-key-path", "-k", default="foo")
params = parser.parse_args()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://127.0.0.1:{params.zmq_port}")


async def jws_validation(token=Depends(HTTPBearer())):
    try:
        ts = int(json.loads(deserialize_compact(token.credentials, params.pub_key_path, [ "HS256" ]).payload)["ts"])
        if pendulum.now('UTC').int_timestamp - ts <= 1:  # We allow a 1sec lag
            return True
        else:
            raise HTTPException(403, "Obsolete timestamp")

    except Exception as e:
        logging.info(e)
        raise HTTPException(403, "Invalid token")

@app.post("/update_data", status_code=202)
async def update_data(mdl: MSFSDataList, auth=Depends(jws_validation)):
    socket.send_string(mdl.model_dump_json())

@app.post("/clear", status_code=202)
async def clear(auth=Depends(jws_validation)):

    data = { "command": "clear" }
    socket.send_string(json.dumps(data))

@app.post("/set_rgb/{r}/{g}/{b}", status_code=202)
async def set_rgb(r: int, g: int, b: int, auth=Depends(jws_validation)):
    data = {
        "command": "set_rgb",
        "r": r,
        "g": g,
        "b": b
    }
    socket.send_string(json.dumps(data))

def run():
    uvicorn.run(app, host="0.0.0.0", port=params.http_port)

if __name__ == "__main__":
    run()