#!/bin/bash -e

export PYTHONPATH=$(pwd)

for f in unit_tests/*_tests.py; do
  python3 $f 
done

