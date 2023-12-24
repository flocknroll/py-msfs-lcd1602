import zmq
import uvicorn
import argparse
import logging

from fastapi import FastAPI, Request, HTTPException

from py_msfs_lcd1602.models.api import MSFSDataList, MSFSData

app = FastAPI()

parser = argparse.ArgumentParser("LCD1602 controller API")
parser.add_argument("--port", default=5555)
params = parser.parse_args()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://localhost:{params.port}")


@app.post("/")
async def root(mdl: MSFSDataList):

    payload = MSFSDataList(mdl)
    socket.send_string(payload.model_dump_json())
    
    return "OK"


uvicorn.run(app, host="0.0.0.0", port=8081)