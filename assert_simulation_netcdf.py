import pathlib as pl
import netCDF4 as nc
import numpy as np

def assert_simulation_netcdf(reference_dir: pl.Path,
                             comparison_dir: pl.Path) -> None:
    reference_files = [f for f in reference_dir.glob('*.nc') if f.is_file()]

    reference_file = reference_files[0]
    for reference_file in reference_files:
        print(f'Assert file {reference_file.stem}')
        
        comparison_file = comparison_dir / reference_file.name
        
        assert comparison_file.exists(), f'File {comparison_file} does not exist'
        
        with nc.Dataset(reference_file, 'r') as reference_nc, nc.Dataset(comparison_file, 'r') as comparison_nc:
            
            for var_name in reference_nc.variables:
                print(f'\tAssert variable {var_name}')
                
                assert var_name in comparison_nc.variables, f'Variable {var_name} not found'
                
                reference_array = reference_nc.variables[var_name][:]
                comparison_array = comparison_nc.variables[var_name][:]
                if not np.allclose(reference_array, comparison_array, rtol=1e-5, atol=1e-5):
                    
                    reference_min = np.min(reference_array)
                    reference_max = np.max(reference_array)
                    reference_mean = np.mean(reference_array)
                    reference_std = np.std(reference_array)
                    print(f'\t> Reference min: {reference_min} max: {reference_max} mean: {reference_mean} std: {reference_std}')
                    
                    comparison_min = np.min(comparison_array)
                    comparison_max = np.max(comparison_array)
                    comparison_mean = np.mean(comparison_array)
                    comparison_std = np.std(comparison_array)
                    print(f'\t> Comparison min: {comparison_min} max: {comparison_max} mean: {comparison_mean} std: {comparison_std}')
                    
                    raise AssertionError(f'Array not equal')