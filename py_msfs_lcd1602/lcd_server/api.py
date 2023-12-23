import zmq
import uvicorn
import argparse

from fastapi import FastAPI, Request, HTTPException


app = FastAPI()

parser = argparse.ArgumentParser("LCD1602 controller API")
parser.add_argument("--port", default=5555)
params = parser.parse_args()

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://localhost:{params.port}")


@app.post("/")
async def root(request: Request):
    body = await request.body()

    if body:
        socket.send(body)
    return "OK"


uvicorn.run(app)