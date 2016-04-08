#!/bin/bash

if [ -z "${PYTHONPATH}" ]
then
  export PYTHONPATH=.
else
  export PYTHONPATH=.:$PYTHONPATH
fi
python3 -m unittest discover -s ofp/v0x02/tests/ -p "test_*.py"
