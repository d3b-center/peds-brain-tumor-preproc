# run pre-processing (CaPTk version 1.8.1)
#   outputs:
#       [subID]_T1_to_SRI.nii.gz
#       [subID]_T1CE_to_SRI.nii.gz
#       [subID]_T2_to_SRI.nii.gz
#       [subID]_FL_to_SRI.nii.gz
FROM cbica/captk:2021.03.29 AS preproc 

COPY run.py run.py
ENTRYPOINT [ "python3", "run.py" ]
