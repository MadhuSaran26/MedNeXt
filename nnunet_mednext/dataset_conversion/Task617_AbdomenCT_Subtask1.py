#    Copyright 2020 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


from collections import OrderedDict
from nnunet_mednext.paths import nnUNet_raw_data
from batchgenerators.utilities.file_and_folder_operations import *
import shutil


if __name__ == "__main__":
    base = "/scratch/msarava7/Data/AbdomenCT1K/"

    task_id = 617
    task_name = "AbdomenCT_subtask1"

    foldername = "Task%03.0d_%s" % (task_id, task_name)

    out_base = join(nnUNet_raw_data, foldername)
    imagestr = join(out_base, "imagesTr")
    imagests = join(out_base, "imagesTs")
    labelstr = join(out_base, "labelsTr")
    maybe_mkdir_p(imagestr)
    maybe_mkdir_p(imagests)
    maybe_mkdir_p(labelstr)

    train_folder = join(base, "Subtask1/TrainImage")
    label_folder = join(base, "Subtask1/TrainMask")
    test_folder = join(base, "TestImage")
    train_patient_names = []
    test_patient_names = []
    train_patients = subfiles(train_folder, join=False, suffix = 'nii.gz')
    for train_patient_name in train_patients:
        label_file_name = f'{train_patient_name[:10]}.nii.gz'
        label_file = join(label_folder, label_file_name)
        image_file = join(train_folder, train_patient_name)
        shutil.copy(image_file, join(imagestr, train_patient_name))
        shutil.copy(label_file, join(labelstr, label_file_name))
        train_patient_names.append(label_file_name)

    test_patients = subfiles(test_folder, join=False, suffix=".nii.gz")
    for test_patient_name in test_patients:
        image_file = join(test_folder, test_patient_name)
        shutil.copy(image_file, join(imagests, test_patient_name))
        test_patient_names.append(test_patient_name)

    json_dict = OrderedDict()
    json_dict['name'] = "AbdomenCT1K"
    json_dict['description'] = "AbdomenCT-1K: Fully Supervised Learning Benchmark"
    json_dict['tensorImageSize'] = "3D"
    json_dict['reference'] = "https://abdomenct-1k-fully-supervised-learning.grand-challenge.org/"
    json_dict['licence'] = "see challenge website"
    json_dict['release'] = "0.0"
    json_dict['modality'] = {
        "0": "CT",
    }
    json_dict['labels'] = OrderedDict({
        "0": "background",
        "1": "liver",
        "2": "kidney",
        "3": "spleen",
        "4": "pancreas"}
    )
    json_dict['numTraining'] = len(train_patient_names)
    json_dict['numTest'] = len(test_patient_names)
    json_dict['training'] = [{'image': "./imagesTr/%s" % train_patient_name, "label": "./labelsTr/%s" % train_patient_name} for i, train_patient_name in enumerate(train_patient_names)]
    json_dict['test'] = ["./imagesTs/%s" % test_patient_name for test_patient_name in test_patient_names]

    save_json(json_dict, os.path.join(out_base, "dataset.json"))
