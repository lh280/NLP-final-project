#!/usr/bin/env bash
# slurm template for serial jobs
# Set SLURM options
#SBATCH --job-name=main # Job name
# Standard output and error log
#SBATCH --output=./out/main-%j.out
# Where to send mail
#SBATCH --mail-user=cfridlington@middlebury.edu
# Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-type=ALL
# Job memory request 
#SBATCH --mem=1g
# Partition (queue) 
#SBATCH --partition=gpu-standard
# Time limit hrs:min:sec 
#SBATCH --time=24:00:00
# DELETE ?
# #SBATCH --cpus-per-task=2
# #SBATCH --gres=gpu:1

# print SLURM envirionment variables
echo "Job ID: ${SLURM_JOB_ID}"
echo "Node: ${SLURMD_NODENAME}" echo "Starting: "`date +"%D %T"` 
# Your calculations here 
python main.py all ${SLURM_JOB_ID}
# End of job info 
echo "Ending: "`date +"%D %T"`