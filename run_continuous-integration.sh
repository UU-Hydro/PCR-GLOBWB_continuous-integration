#!/bin/bash

## Assert simulation
reference_dir=./simulation/reference_output/main_20240326/RhineMeuse_30min_natural/netcdf/
comparison_dir=./simulation/output/RhineMeuse_30min_natural/netcdf/
python ./assert_simulation_netcdf.txt $reference_dir $comparison_dir

reference_dir=./simulation/reference_output/main_20240326/RhineMeuse_30min_natural/states/
comparison_dir=./simulation/output/RhineMeuse_30min_natural/states/
python ./assert_simulation_states.txt $reference_dir $comparison_dir