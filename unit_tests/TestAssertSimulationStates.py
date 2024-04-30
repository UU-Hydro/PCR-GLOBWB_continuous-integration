import pathlib as pl
import pcraster as pcr
import unittest
import shutil as sh

from assert_simulation_states import assert_simulation_states

from .HiddenPrints import HiddenPrints

class TestAssertSimulationStates(unittest.TestCase):
    
    reference = None
    configuration = None
    reference_dir = None
    comparison_dir = None
    
    @classmethod
    def setUpClass(cls):
        if cls.comparison_dir.exists():
            raise FileExistsError(f"Directory {cls.comparison_dir} already exists")
        
        sh.copytree(cls.reference_dir / cls.reference / cls.configuration / "states",
                    cls.comparison_dir / cls.configuration / "states")
    
    @classmethod
    def tearDownClass(cls):
        if not cls.comparison_dir.exists():
            raise FileNotFoundError(f"Directory {cls.comparison_dir} does not exist")
        
        sh.rmtree(cls.comparison_dir)
    
    def setUp(self):
        self.reference_netcdf_dir = self.reference_dir / self.reference / self.configuration / "states"
        self.comparison_netcdf_dir = self.comparison_dir / self.configuration / "states"
    
    def test_correct(self):
        with HiddenPrints():
            assert_simulation_states(reference_dir=self.reference_netcdf_dir,
                                    comparison_dir=self.comparison_netcdf_dir)
    
    def test_missing_file(self):
        reference_files = [f for f in self.reference_netcdf_dir.glob("*.map") if f.is_file() and "avg" not in f.stem]
        reference_file = reference_files[0]
        
        comparison_file = self.comparison_netcdf_dir / reference_file.name
        temporary_file = comparison_file.with_suffix(".tmap")
        
        sh.move(comparison_file, temporary_file)
        with self.assertRaises(AssertionError):
            with HiddenPrints():
                assert_simulation_states(reference_dir=self.reference_netcdf_dir,
                                        comparison_dir=self.comparison_netcdf_dir)
        sh.move(temporary_file, comparison_file)
    
    def test_different_data(self):
        reference_files = [f for f in self.reference_netcdf_dir.glob("*.map") if f.is_file() and "avg" not in f.stem]
        reference_file = reference_files[0]
        
        comparison_file = self.comparison_netcdf_dir / reference_file.name
        pcr.setclone(str(comparison_file))
        variable_data = pcr.readmap(str(comparison_file))
        temporary_data = variable_data + 1.0
        
        pcr.report(temporary_data, str(comparison_file))
        with self.assertRaises(AssertionError):
            with HiddenPrints():
                assert_simulation_states(reference_dir=self.reference_netcdf_dir,
                                        comparison_dir=self.comparison_netcdf_dir)
        pcr.report(variable_data, str(comparison_file))
