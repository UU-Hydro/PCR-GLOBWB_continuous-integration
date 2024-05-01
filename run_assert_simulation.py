import pathlib as pl

from assert_simulation_netcdf import assert_simulation_netcdf
from assert_simulation_states import assert_simulation_states

reference = "latest_main"
reference_dir = pl.Path("./simulation/reference_output").absolute()
comparison_dir = pl.Path("./simulation/output").absolute()

if __name__ == '__main__':
    configurations = [d.stem for d in (reference_dir / reference).iterdir() if d.is_dir()]
    assert_any = False

    for configuration in configurations:
        print(f'configuration {configuration}')
        
        configuration_reference_dir = reference_dir / reference / configuration
        configuration_comparison_dir = comparison_dir / configuration
        
        if not configuration_reference_dir.exists():
            print(f"WARNING: Directory {configuration_reference_dir} does not exist.")
            continue

        assert_any = True
        assert_simulation_netcdf(reference_dir = configuration_reference_dir / "netcdf",
                                comparison_dir = configuration_comparison_dir / "netcdf")
        assert_simulation_states(reference_dir = configuration_reference_dir / "states",
                                comparison_dir = configuration_comparison_dir / "states")
        
    if not assert_any:
        raise FileNotFoundError("ERROR: No directories to assert.")
