import pandas as pd
import os
# first step
# file_path = 'Labels/pom_extra_sqa_mono_results.csv'

# label = pd.read_csv(file_path)
# true_label = label[['Input.VIDEO_ID', 'Input.CLIP', 'Answer.anger', 'Answer.disgust', 'Answer.fear', 'Answer.happiness', 
#                     'Answer.sadness', 'Answer.surprise', 'Answer.sentiment']]
# new_csv = true_label.groupby(['Input.VIDEO_ID', 'Input.CLIP']).sum().reset_index()

# new_csv.to_csv('new_pom_extra_sqa_mono_results.csv')

# scond step
file_path = 'New_Labels/'
file_list = os.listdir(file_path)
index = 0

for file in file_list:
    if index == 0:
        df = pd.read_csv('New_Labels/' + file)
        df.to_csv('all_labels.csv', encoding="utf_8_sig", index=False)
        index += 1
    else:
        df = pd.read_csv('New_Labels/' + file)
        df.to_csv('all_labels.csv', encoding="utf_8_sig", index=False, header=False, mode='a+')
