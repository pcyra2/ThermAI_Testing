import sys
import pyscf
import gpu4pyscf
import gpu4pyscf.dft as dft
from dataclasses import dataclass
import time
import json

@dataclass
class GLOBAL_VARIABLES:
    basis_set: str = "def2-SVP"
    charge: int = 0
    spin: int  = 0
    memory: int = 10000
    method: str = "B3LYP"


def gen_mol(
        file: str,
        basis: str = "sto-3g",
        charge: int = 0,
        spin: int = 0,
        memory: int = 15000,
        method: str = "B3LYP"
        ) -> pyscf.gto.Mole:
    """Generates the pySCF molecule object that can be used for further calculations.

    Args:
        file (str): The name of the coordinate file that will be read in by pySCF. 
            This should be in `.xyz` format and contain the extention.
        basis (str): The basis set to use for the calculation. This should be understoof 
            by pySCF. Defaults to `sto-3g`.
        charge (int): The net charge of the system. Defaults to 0.
        spin (int): The net spin of the system. This should be 2S, not 2S+1. Defaults to 0.
        memory (int): The amount of memory in MB that will be allocated to the calculation.
        method (str): The QM method to use for file naming
    
    Returns:
        mol (pyscf.gto.Mole): The build molecule object. The output file defaults to `MOLECULE_METHOD_BASIS.out`.
    """
    mol = pyscf.gto.Mole(atom=file, unit="Ang")
    mol.output=f"{file.replace('.xyz','')}_{method}_{basis}.out"
    mol.basis = basis
    mol.charge = charge
    mol.spin = spin
    mol.symmetry = False # pySCF symmetry optimisations dont work very well...
    mol.verbose = 4
    mol.cart=False
    mol.max_memory=memory
    mol.build()
    return mol

def build_dft(mol: pyscf.gto.Mole, method: str) -> gpu4pyscf.dft.UKS:
    """Builds the mf kernel. Does not execute. Some basic optimisations have been made and 
    no dispersion correction is added at this time. 
    
    Args:
        mol (pyscf.gto.Mole): pySCF Molecule object containing the charge, spin, 
            basis set and io config. This must be built before parsing to this function.
        method (str): The DFT method to use. This must be understood by pySCF.
    
    Returns:
        mf (gpu4pyscf.dft.UKS): The mean field object. This is not executed, but can be used to 
            run the mean field calculation.
    """
    mf = dft.UKS(mol, method)
    mf.max_cycle = 200
    mf.conv_tol = 1e-7
    mf.level_shift = (1.2,0.2)
    return mf


def main() -> None:
    start = time.perf_counter()
    structure = sys.argv[1]
    for arg in sys.argv[2:]:
        if "-c" in arg:
            GLOBAL_VARIABLES.charge = int(arg.split("=")[1])
        if "-s" in arg:
            GLOBAL_VARIABLES.spin = int(arg.split("=")[1])
        if "-m=" in arg:
            GLOBAL_VARIABLES.method = str(arg.split("=")[1])
        if "-b" in arg:
            GLOBAL_VARIABLES.basis_set = str(arg.split("=")[1])

        if "-mem" in arg:
            GLOBAL_VARIABLES.memory = int(arg.split("=")[1])


    molecule = gen_mol(file=structure,
                    basis=GLOBAL_VARIABLES.basis_set,
                    charge=GLOBAL_VARIABLES.charge,
                    spin=GLOBAL_VARIABLES.spin,
                    memory=GLOBAL_VARIABLES.memory)
    mol_time = time.perf_counter()
    mf = build_dft(mol = molecule,
                method = GLOBAL_VARIABLES.method)
    mf_time = time.perf_counter()
    mf.kernel()
#    mf.newton().run()
    mf_exe_time = time.perf_counter()

    data = dict(mol_build_time = mol_time - start,
                mf_build_time=mf_time - mol_time,
                mf_run_time=mf_exe_time - mf_time,
                total_time = mf_exe_time - start,
                e_tot = mf.e_tot
                )
    data_file_name = f"{structure.replace('.xyz','')}_{GLOBAL_VARIABLES.method}_{GLOBAL_VARIABLES.basis_set}_summary.json"
    with open( file = data_file_name, mode = "w") as file:
        json.dump(obj = data, fp = file)
    


if __name__ == "__main__":
    main()
