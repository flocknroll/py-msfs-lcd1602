#!/usr/bin/env bash

nix-shell -p python311Packages.smbus2 \
          -p python311Packages.fastapi \
          -p python311Packages.pyzmq \
          -p python311Packages.smbus2 \
          -p python311Packages.requests \
          -p python311Packages.uvicorn