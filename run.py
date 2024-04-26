
# mapping for tumor seg:
# | Image type      | imageID |
# | ----------- | ----------- |
# | T2w-FLAIR      | 000       |
# | T1w   | 001        |
# | T1w post-contrast   | 002        |
# | T2w   | 003        |

import os
import shutil
from glob import glob

CaPTk_dir='/opt/captk/1.8.1/usr' # path to install (in Docker container)

unique_subs=[]
for im_file in glob("input/*.nii*"):
    im_file_name = im_file.split('/')[-1]
    if '_0000_ss_norm' in im_file_name:
        this_sub = im_file_name.split('_0000_ss_norm')[0]
        if this_sub not in unique_subs:
            unique_subs.append(this_sub)

print(f'{len(unique_subs)} subjects found for processing.')

# run pre-processing on each unique subID in the input dir
# then setup pre-processed files for input into nnUNet tumor seg model
for sub in unique_subs:
    # run the main pipeline
    fl_im = glob(f'input/{sub}_0000_ss_norm*')[0]
    t1_im = glob(f'input/{sub}_0001_ss_norm*')[0]
    t1ce_im = glob(f'input/{sub}_0002_ss_norm*')[0]
    t2_im = glob(f'input/{sub}_0003_ss_norm*')[0]
    seg_file = glob(f'input/{sub}_pred_brainTumorSeg*')[0]

    print(f" ========== Running CaPTk BraTSPipeline for subject ID {sub} ==========")

    # binarize the tumor segmentation ROI
    bin_roi_fn = f'{sub}_pred_brainTumorSeg.nii.gz'
    os.system(f'{CaPTk_dir}/bin/Utilities -i {seg_file} -o {bin_roi_fn} -cm')

    # run feature extraction
    feat_file = 'radiomic_feature_params_20230725.csv'
    os.system(f'{CaPTk_dir}/bin/FeatureExtraction \
        -n {sub} \
        -i {t1_im},{t1ce_im},{t2_im},{fl_im} \
        -t T1,T1Gd,T2,FLAIR \
        -m {bin_roi_fn} \
        -r 1 \
        -l "tumor_core" \
        -p {feat_file} \
        -o "output/"')

# merge all of the individual subject files into one output CSV
one_csv = glob(f'output/results_*.csv')[0]
os.system(f'cat {one_csv} | head -n1 > output/radiomic_features.csv')
os.system('for f in output/results_*.csv; do cat "`pwd`/$f" | tail -n +2 >> output/radiomic_features.csv; done ')

# delete the subject CSVs
for subj_csv in glob('output/results_*.csv'):
    os.remove(subj_csv)
