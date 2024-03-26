
import pathlib as pl
import pcraster as pcr
import numpy as np
import sys

if len(sys.argv) < 2:
    raise ValueError('Please provide the reference directory as argument')
if len(sys.argv) < 3:
    raise ValueError('Please provide the comparison directory as argument')

reference_dir = pl.Path(sys.argv[1])
comparison_dir = pl.Path(sys.argv[2])

reference_files = [f for f in reference_dir.glob('*.map') if f.is_file()]

reference_file = reference_files[0]
for reference_file in reference_files:
    print(f'Assert file {reference_file.stem}')
    
    comparison_file = comparison_dir / reference_file.name
    assert comparison_file.exists()
    
    pcr.setclone(str(reference_file))
    reference_map = pcr.readmap(str(reference_file))
    comparison_map = pcr.readmap(str(comparison_file))
    
    reference_array = pcr.pcr2numpy(reference_map, 0)
    comparison_array = pcr.pcr2numpy(comparison_map, 0)
    assert np.allclose(reference_array, comparison_array, rtol=1e-5, atol=1e-5)