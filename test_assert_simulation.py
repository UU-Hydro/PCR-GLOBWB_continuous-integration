import pathlib as pl
import unittest

from unit_tests.TestAssertSimulationNetcdf import TestAssertSimulationNetcdf
from unit_tests.TestAssertSimulationStates import TestAssertSimulationStates

reference = "latest_main"
reference_dir = pl.Path("./simulation/reference_output").absolute()
comparison_dir = pl.Path("./simulation/comparison_output").absolute()

if __name__ == '__main__':
    
    configurations = [d.stem for d in (reference_dir / reference).iterdir() if d.is_dir()]
    for configuration in configurations:
        print(f'configuration {configuration}')
    
        TestAssertSimulationNetcdf.reference = reference
        TestAssertSimulationNetcdf.configuration = configuration
        TestAssertSimulationNetcdf.reference_dir = reference_dir
        TestAssertSimulationNetcdf.comparison_dir = comparison_dir
        
        TestAssertSimulationStates.reference = reference
        TestAssertSimulationStates.configuration = configuration
        TestAssertSimulationStates.reference_dir = reference_dir
        TestAssertSimulationStates.comparison_dir = comparison_dir
        
        unittest.main(verbosity=2,
                      exit=False)