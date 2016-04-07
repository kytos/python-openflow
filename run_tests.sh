#!/bin/bash

if [ -z "${PYTHONPATH}" ]
then
  export PYTHONPATH=.:ofp
else
  export PYTHONPATH=.:ofp::$PYTHONPATH
fi
python3 -m unittest discover -s tests/ -p "*_test.py"
