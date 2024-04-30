import pathlib as pl
import pcraster as pcr
import numpy as np

def assert_simulation_states(reference_dir: pl.Path,
                             comparison_dir: pl.Path) -> None:
    reference_files = [f for f in reference_dir.glob('*.map') if f.is_file()]

    reference_file = reference_files[0]
    for reference_file in reference_files:
        print(f'Assert file {reference_file.stem}')
        
        comparison_file = comparison_dir / reference_file.name
        assert comparison_file.exists(), f'File {comparison_file} does not exist'
        
        pcr.setclone(str(reference_file))
        reference_map = pcr.readmap(str(reference_file))
        comparison_map = pcr.readmap(str(comparison_file))
        
        reference_array = pcr.pcr2numpy(reference_map, 0)
        comparison_array = pcr.pcr2numpy(comparison_map, 0)        
        if not np.allclose(reference_array, comparison_array, rtol=1e-5, atol=1e-5):
            
            reference_min = np.min(reference_array)
            reference_max = np.max(reference_array)
            reference_mean = np.mean(reference_array)
            reference_std = np.std(reference_array)
            reference_median = np.median(reference_array)
            reference_q25 = np.percentile(reference_array, 25)
            reference_q75 = np.percentile(reference_array, 75)
            print(f'\t> Reference min: {reference_min} max: {reference_max} mean: {reference_mean} std: {reference_std} median: {reference_median} q25: {reference_q25} q75: {reference_q75}')
            
            comparison_min = np.min(comparison_array)
            comparison_max = np.max(comparison_array)
            comparison_mean = np.mean(comparison_array)
            comparison_std = np.std(comparison_array)
            comparison_median = np.median(comparison_array)
            comparison_q25 = np.percentile(comparison_array, 25)
            comparison_q75 = np.percentile(comparison_array, 75)
            print(f'\t> Comparison min: {comparison_min} max: {comparison_max} mean: {comparison_mean} std: {comparison_std} median: {comparison_median} q25: {comparison_q25} q75: {comparison_q75}')        
            
            raise AssertionError(f'Array not equal')