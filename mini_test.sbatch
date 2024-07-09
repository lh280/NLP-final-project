#!/usr/bin/env bash
# slurm template for serial jobs
# Set SLURM options
#SBATCH --job-name=mini_test # Job name
# Standard output and error log
#SBATCH --output=./out/mini_test-%j.out
# Where to send mail
#SBATCH --mail-user=cfridlington@middlebury.edu
# Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-type=ALL
# Job memory request 
#SBATCH --mem=1g
# Partition (queue) 
#SBATCH --partition=gpu-standard
# Time limit hrs:min:sec 
#SBATCH --time=1:00:00
# DELETE ?
# #SBATCH --cpus-per-task=1
# #SBATCH --gres=gpu:1

# print SLURM envirionment variables
echo "Job ID: ${SLURM_JOB_ID}"
echo "Node: ${SLURMD_NODENAME}" echo "Starting: "`date +"%D %T"` 
# Your calculations here 
python main.py mini_test ${SLURM_JOB_ID}
# End of job info 
echo "Ending: "`date +"%D %T"`