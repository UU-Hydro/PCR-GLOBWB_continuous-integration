
import pathlib as pl
import netCDF4 as nc
import numpy as np
import sys

if len(sys.argv) < 2:
    raise ValueError('Please provide the reference directory as argument')
if len(sys.argv) < 3:
    raise ValueError('Please provide the comparison directory as argument')

reference_dir = pl.Path(sys.argv[1])
comparison_dir = pl.Path(sys.argv[2])

reference_files = [f for f in reference_dir.glob('*.nc') if f.is_file()]

reference_file = reference_files[0]
for reference_file in reference_files:
    print(f'Assert file {reference_file.stem}')
    
    comparison_file = comparison_dir / reference_file.name
    assert comparison_file.exists()
    
    with nc.Dataset(reference_file, 'r') as example_nc, nc.Dataset(comparison_file, 'r') as comparison_nc:
        
        for var_name in example_nc.variables:
            print(f'\tAssert variable {var_name}')
            
            assert var_name in comparison_nc.variables
            
            example_var = example_nc.variables[var_name][:]
            comparison_var = comparison_nc.variables[var_name][:]
            assert np.allclose(example_var, comparison_var, rtol=1e-5, atol=1e-5)