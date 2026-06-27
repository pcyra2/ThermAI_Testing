# ThermAI Workload tests. 
---

This repo is made as a quick test to find how well GPU jobs work on the ThermAI interface.
The Molecules contained within the `Data` directory are owned and created by Ross Amory however are not commercially significant.

The `Code` directory contains a quick python script that interfaces with pySCF, and gpu4pyscf in order to perform a single point qm calculation on a given `.xyz` file using a GPU. The Dockerfile can be modified to change the number of CPU cores that are given to a calculation. This is currently set at 6 and I am unsure how the job will scale. I dont expect the calculation to actually need more that one or two, but it is currently untested at any value other than 6. The Code is setup to use ~15GB of memory, this can be altered using the `-mem=XXXX` where `XXXX` is given in MB. Always give the calculation less memory than what is available as pySCF tends to have some extra overheads.

## Building the docker container:
There are example build and run sripts in `/Code/Scripts/DockerBuild.sh` and `/Code/Scripts/DockerRun.sh`.

## Running a single job:

```docker run --privileged --runtime=nvidia -it -v $PWD:/app/data  amory-quantum:latest sp H2O.xyz -c=-1 -m=B3LYP -b=def2-SVP```

- `sp` = Runs the single point job (This will allow for future experiments in the same docker container.)
- `H2O.xyz` = The `.xyz` file you want to calculate the energy for
- `-c=-1` = The net charge of the system. (Do not need if 0)
- `-s=0` = The spin of the system. (Do not need if 0)
- `-m=B3LYP` = The QM method to use. If you want a faster job, use `PBE`, if you want a slower job, use `wB997X`.
- `-b=def2-SVP` = The basis set to use. If you want a faster job, use `sto-3g`, if you want a slower job, use `def2-DVP`.
- `-mem=1000` = The ammount of memory to give the job (in MB). This does not include standard python memory etc so give less than the total available memory.   
