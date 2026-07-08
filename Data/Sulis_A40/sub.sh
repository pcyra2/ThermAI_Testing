#!/bin/bash
#SBATCH --time=1:00:00
#SBATCH --partition=gpu
#SBATCH --ntasks-per-node=12
#SBATCH --job-name=ThermAI
#SBATCH --mem=10GB
#SBATCH --account=su006-101-gpu
#SBATCH --gres=gpu:lovelace_l40:1
#SBATCH --array=1-21

container=/home/b/brara83/docker_containers/ThermAI.sif
module load CUDA/12.8.0
module list
echo pes.$SLURM_ARRAY_TASK_ID.xyz

singularity run --nv --bind ./:/app/data/ $container sp pes.$SLURM_ARRAY_TASK_ID.xyz -c=-1 -b=def2-SVP
