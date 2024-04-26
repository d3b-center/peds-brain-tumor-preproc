import os
import shutil
from glob import glob

CaPTk_dir='/opt/captk/1.8.1/usr' # path to install (in Docker container)

unique_subs=[]
for im_file in glob("input/*.nii*"):
    im_file_name = im_file.split('/')[-1]
    if '_FL' in im_file_name:
        this_sub = im_file_name.split('_FL')[0]
        if this_sub not in unique_subs:
            unique_subs.append(this_sub)

print(f'{len(unique_subs)} subjects found for processing.')

# run pre-processing on each unique subID in the input dir
# then setup pre-processed files for input into nnUNet tumor seg model
for sub in unique_subs:
    # make output directory for this subject
    output_dir=f'{sub}'
    os.makedirs(output_dir) 
    # run the main pipeline
    fl_im = glob(f'input/{sub}_FL*')[0]
    t1ce_im = glob(f'input/{sub}_T1CE*')[0]
    t2_im = glob(f'input/{sub}_T2*')[0]
    t1_im = glob(f'input/{sub}_T1*')[0]
    print(f" ========== Running CaPTk BraTSPipeline for subject ID {sub} ==========")
    os.system(f'{CaPTk_dir}/bin/BraTSPipeline \
                -t1 {t1_im} \
                -t1c {t1ce_im} \
                -t2 {t2_im} \
                -fl {fl_im} \
                --skullStrip 0 \
                --brainTumor 0 \
                --interFiles 0 \
                -o {sub}')
    # move result files to final output directory
    preproc_output_dir = 'preprocessed'
    if not os.path.exists(preproc_output_dir):
        os.makedirs(preproc_output_dir)
    shutil.move(f'{sub}/T1_to_SRI.nii.gz',f'{preproc_output_dir}/{sub}_T1_to_SRI.nii.gz')
    shutil.move(f'{sub}/T1CE_to_SRI.nii.gz',f'{preproc_output_dir}/{sub}_T1CE_to_SRI.nii.gz')
    shutil.move(f'{sub}/T2_to_SRI.nii.gz',f'{preproc_output_dir}/{sub}_T2_to_SRI.nii.gz')
    shutil.move(f'{sub}/FL_to_SRI.nii.gz',f'{preproc_output_dir}/{sub}_FL_to_SRI.nii.gz')

    # cleanup
    shutil.rmtree(f'{sub}')

# mapping for tumor seg:
# | Image type      | imageID |
# | ----------- | ----------- |
# | T2w-FLAIR      | 000       |
# | T1w   | 001        |
# | T1w post-contrast   | 002        |
# | T2w   | 003        |
