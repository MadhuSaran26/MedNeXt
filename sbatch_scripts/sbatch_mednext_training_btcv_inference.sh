#!/bin/bash

#SBATCH -N 1           # number of nodes
#SBATCH -c 20            # number of "tasks" (default: 1 core per task)
#SBATCH --mem=64G
#SBATCH -t 0-04:00:00   # time in d-hh:mm:ss
#SBATCH -p htc       # partition 
#SBATCH -q public       # QOS
#SBATCH -G a100:1  # number of GPUs
#SBATCH -o /scratch/msarava7/IAI/Results/Benchmarking_Runs/slurm.btcv.seg.mednext.%x.%j.out # file to save job's STDOUT (%j = JobId)
#SBATCH -e /scratch/msarava7/IAI/Results/Benchmarking_Runs/slurm.btcv.seg.mednext.%x.%j.err # file to save job's STDERR (%j = JobId)
#SBATCH --mail-type=ALL # Send an e-mail when a job starts, stops, or fails
#SBATCH --mail-user=msarava7@asu.edu # Mail-to address
#SBATCH --export=NONE   # Purge the job-submitting shell environment

# Load required modules for job's environment
module load mamba/latest

source activate transoar

export nnUNet_raw_data_base="/scratch/msarava7/Data/nnUNet_Base_Folder"
export nnUNet_preprocessed="/scratch/msarava7/Data/nnUNet_Preprocessed_Folder"
export RESULTS_FOLDER="/scratch/msarava7/Models/nnUNet_Results_Folder"

cd /scratch/msarava7/MedNeXt/

mednextv1_predict -i /scratch/msarava7/Data/nnUNet_Base_Folder/nnUNet_raw_data/Task017_AbdominalOrganSegmentation/imagesTs -o /scratch/msarava7/Data/nnUNet_Predictions/Task017_AbdominalOrganSegmentation -tr nnUNetTrainerV2_MedNeXt_B_kernel3 -ctr nnUNetTrainerV2CascadeFullRes -m 3d_fullres -p nnUNetPlansv2.1_trgSp_1x1x1 -t Task017_AbdominalOrganSegmentation


# E-mail diagnostic results to yourself using mailserver and a heredoc
mail -s "MedNeXt BTCV Inference MICCAI 2023" ${USER}@asu.edu << EOF
Hi,
Iteration is completed successfully.
EOF