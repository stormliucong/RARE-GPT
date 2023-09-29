# delete empty files
find ./Experiment_004subset -maxdepth 1 -type f -empty -delete
mv ./Experiment_004subset/*.gpt.response ./Experiment_003subset/