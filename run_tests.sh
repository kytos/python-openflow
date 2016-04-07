#!/bin/bash

#export PYTHONPATH=ofp:$PYTHONPATH
python3 -m unittest discover -s tests/ -p "*_test.py"
