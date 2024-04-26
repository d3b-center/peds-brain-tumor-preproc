# run feature extraction (CaPTk version 1.8.1)

FROM cbica/captk:2021.03.29 

COPY run.py run.py
COPY radiomic_feature_params_20230725.csv radiomic_feature_params_20230725.csv
ENTRYPOINT [ "python3", "run.py" ]
