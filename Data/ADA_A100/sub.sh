#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --partition=ampereq
#SBATCH --ntasks-per-node=12
#SBATCH --job-name=ThermAI
#SBATCH --mem=10GB
#SBATCH --gres=gpu:A100-full:1
#SBATCH --array=1-21

container=/gpfs01/home/brara83/SingularityContainers/ThermAI.sif
module load cuda-uoneasy/12.6.0
module load singularity/3.8.5
module list
echo pes.$SLURM_ARRAY_TASK_ID.xyz

singularity run --nv --bind ./:/app/data/ $container sp pes.$SLURM_ARRAY_TASK_ID.xyz -c=-1 -b=def2-SVP
