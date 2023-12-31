# !/bin/bash -e

export nnUNet_raw_data_base="/workspace"
export RESULTS_FOLDER="/workspace/datasets/"

echo  "\e[91m start predict using MedNext... \e[0m"

mednextv1_predict -i /workspace/inputs/ -o /workspace/outputs/ -tr nnUNetTrainerV2_MedNeXt_B_kernel3 -m 3d_fullres -p nnUNetPlansv2.1_trgSp_1x1x1 -t Task617_AbdomenCT_subtask1 -f all --disable_tta
