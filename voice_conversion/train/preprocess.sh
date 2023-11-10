svc pre-resample -i dataset_raw/"$1" -o train_params/dataset/"$1"
svc pre-config -i train_params/dataset/"$1" -f train_params/filelist/"$1" -c train_params/configs/"$1".json
svc pre-hubert -i train_params/dataset/"$1" -c train_params/configs/"$1".json