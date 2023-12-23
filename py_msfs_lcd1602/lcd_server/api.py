import zmq
import argparse
import time

from datetime import datetime


parser = argparse.ArgumentParser("LCD1602 controller backend")
parser.add_argument("--bus-id", default=3)
parser.add_argument("--port", default=5555)

if __name__ == "__main__":
    params = parser.parse_args()

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://*:{params.port}")

    while True:
        socket.send_string(f"{datetime.now().strftime('%H:%M:%S:%f')}")

        time.sleep(1)