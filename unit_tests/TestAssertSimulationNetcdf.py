import pathlib as pl
import netCDF4 as nc
import unittest
import shutil as sh

from assert_simulation_netcdf import assert_simulation_netcdf

from .HiddenPrints import HiddenPrints

class TestAssertSimulationNetcdf(unittest.TestCase):
    
    reference = None
    configuration = None
    reference_dir = None
    comparison_dir = None
    
    @classmethod
    def setUpClass(cls):
        if cls.comparison_dir.exists():
            raise FileExistsError(f"Directory {cls.comparison_dir} already exists")
        
        sh.copytree(cls.reference_dir / cls.reference / cls.configuration / "netcdf",
                    cls.comparison_dir / cls.configuration / "netcdf")
    
    @classmethod
    def tearDownClass(cls):
        if not cls.comparison_dir.exists():
            raise FileNotFoundError(f"Directory {cls.comparison_dir} does not exist")
        
        sh.rmtree(cls.comparison_dir)
    
    def setUp(self):
        self.reference_netcdf_dir = self.reference_dir / self.reference / self.configuration / "netcdf"
        self.comparison_netcdf_dir = self.comparison_dir / self.configuration / "netcdf"
    
    def test_correct(self):
        with HiddenPrints():
            assert_simulation_netcdf(reference_dir=self.reference_netcdf_dir,
                                    comparison_dir=self.comparison_netcdf_dir)
    
    def test_missing_file(self):
        reference_files = [f for f in self.reference_netcdf_dir.glob("*.nc") if f.is_file()]
        reference_file = reference_files[0]
        
        comparison_file = self.comparison_netcdf_dir / reference_file.name
        temporary_file = comparison_file.with_suffix(".tnc")
        
        sh.move(comparison_file, temporary_file)
        with self.assertRaises(AssertionError):
            with HiddenPrints():
                assert_simulation_netcdf(reference_dir=self.reference_netcdf_dir,
                                        comparison_dir=self.comparison_netcdf_dir)
        sh.move(temporary_file, comparison_file)
    
    def test_missing_variable(self):
        reference_files = [f for f in self.reference_netcdf_dir.glob("*.nc") if f.is_file()]
        reference_file = reference_files[0]
        
        comparison_file = self.comparison_netcdf_dir / reference_file.name
        with nc.Dataset(comparison_file, 'r') as comparison_nc:
            variable_name = [v for v in comparison_nc.variables.keys() if v.lower() not in ["lat", "latitude", "lon", "longitude", "time"]][0]
            temporary_name = f"{variable_name}_tmp"
            
        with nc.Dataset(comparison_file, 'a') as comparison_nc:
            comparison_nc.renameVariable(variable_name, temporary_name)
        with self.assertRaises(AssertionError):
            with HiddenPrints():
                assert_simulation_netcdf(reference_dir=self.reference_netcdf_dir,
                                        comparison_dir=self.comparison_netcdf_dir)
        with nc.Dataset(comparison_file, 'a') as comparison_nc:
            comparison_nc.renameVariable(temporary_name, variable_name)
        
            
    def test_different_data(self):
        reference_files = [f for f in self.reference_netcdf_dir.glob("*.nc") if f.is_file()]
        reference_file = reference_files[0]
        
        comparison_file = self.comparison_netcdf_dir / reference_file.name
        with nc.Dataset(comparison_file, 'r') as comparison_nc:
            variable_name = [v for v in comparison_nc.variables.keys() if v.lower() not in ["lat", "latitude", "lon", "longitude", "time"]][0]
            variable_data = comparison_nc[variable_name][:]
            temporary_data = variable_data + 1.0
        
        with nc.Dataset(comparison_file, 'a') as comparison_nc:
            comparison_nc[variable_name][:] = temporary_data
        with self.assertRaises(AssertionError):
            with HiddenPrints():
                assert_simulation_netcdf(reference_dir=self.reference_netcdf_dir,
                                        comparison_dir=self.comparison_netcdf_dir)
        with nc.Dataset(comparison_file, 'a') as comparison_nc:
            comparison_nc[variable_name][:] = variable_data
