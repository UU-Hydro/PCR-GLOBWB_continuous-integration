import pathlib as pl
import unittest

from unit_tests.TestAssertSimulationNetcdf import TestAssertSimulationNetcdf
from unit_tests.TestAssertSimulationStates import TestAssertSimulationStates

reference = "release_v2.4.0_alpha"
configuration = "RhineMeuse_30min_natural"
reference_dir = pl.Path("./simulation/reference_output").absolute()
comparison_dir = pl.Path("./simulation/comparison_output").absolute()

if __name__ == '__main__':
    TestAssertSimulationNetcdf.reference = reference
    TestAssertSimulationNetcdf.configuration = configuration
    TestAssertSimulationNetcdf.reference_dir = reference_dir
    TestAssertSimulationNetcdf.comparison_dir = comparison_dir
    
    TestAssertSimulationStates.reference = reference
    TestAssertSimulationStates.configuration = configuration
    TestAssertSimulationStates.reference_dir = reference_dir
    TestAssertSimulationStates.comparison_dir = comparison_dir
    
    unittest.main(verbosity=2)