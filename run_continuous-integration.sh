#!/bin/bash

python run_assert_simulation.py
if [ $? -ne 0 ]; then
    echo "ERROR: Simulation assertion failed"
    exit 1
fi