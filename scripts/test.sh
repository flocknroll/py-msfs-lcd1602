#/usr/bin/env bash

curl -XPOST http://localhost:8081/clear
curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "INDICATED ALTITUDE", "value": "1060.54545454" } ] }'
curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "AIRSPEED INDICATED", "value": "254.24545454" } ] }'
curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "VERTICAL SPEED", "value": "-1554.145454545" } ] }'
curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "AIRSPEED MACH", "value": "0.336" } ] }'

curl -XPOST http://localhost:8081/set_rgb/200/0/0

curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "INDICATED ALTITUDE", "value": "10060.54545454" } ] }'
curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "AIRSPEED INDICATED", "value": "0254.24545454" } ] }'
curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "VERTICAL SPEED", "value": "554.145454545" } ] }'
curl -XPOST http://localhost:8081/update_data -H "Content-Type: application/json" --data '{ "data": [ { "name": "AIRSPEED MACH", "value": "1.537" } ] }'