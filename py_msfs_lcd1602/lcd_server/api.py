import zmq
import uvicorn
import argparse
import logging

from fastapi import FastAPI, HTTPException

from py_msfs_lcd1602.models.api import MSFSDataList

app = FastAPI()

parser = argparse.ArgumentParser("LCD1602 controller API")
parser.add_argument("--zmq-port", default=5555)
parser.add_argument("--http-port", default=8081)
params = parser.parse_args()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://localhost:{params.zmq_port}")


@app.post("/update_data", status_code=202)
async def update_data(mdl: MSFSDataList):
    socket.send_string(mdl.json())


uvicorn.run(app, host="0.0.0.0", port=params.http_port)