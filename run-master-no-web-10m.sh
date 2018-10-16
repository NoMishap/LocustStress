#!/bin/bash

python3 locust_master.py -f=nomishap.py --host=http://localhost:5555 --no-web -c=100 -r=0.16667 -t=10m --slaves=2
