import zmq
import uvicorn
import argparse
import logging
import json

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from joserfc.jws import deserialize_compact

from py_msfs_lcd1602.models.api import MSFSDataList

app = FastAPI()

parser = argparse.ArgumentParser("LCD1602 controller API")
parser.add_argument("--zmq-port", default=5555)
parser.add_argument("--http-port", default=8081)
params = parser.parse_args()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://localhost:{params.zmq_port}")


def jws_validation(token=Depends(HTTPBearer())):
    return deserialize_compact(token, "test", [ "HS256" ])

@app.post("/update_data", status_code=202)
async def update_data(mdl: MSFSDataList):
    socket.send_string(mdl.model_dump_json())

@app.post("/clear", status_code=202)
async def clear(authorized=Depends(jws_validation)):
    if not authorized:
        raise HTTPException(403)

    data = { "command": "clear" }
    socket.send_string(json.dumps(data))

@app.post("/set_rgb/{r}/{g}/{b}", status_code=202)
async def set_rgb(r: int, g: int, b: int):
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