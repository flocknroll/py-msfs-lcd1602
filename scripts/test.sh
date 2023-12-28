#/usr/bin/env bash

curl -XPOST http://localhost:8081/clear
curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "INDICATED ALTITUDE", "value": "1060.5" } ] }'
curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "AIRSPEED INDICATED", "value": "254.2" } ] }'
curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "VERTICAL SPEED", "value": "-1554.1" } ] }'
