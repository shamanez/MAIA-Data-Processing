import os
import csv
import wave
import sys
import numpy as np
import pandas as pd
import glob
import array
import glob


branch='label_file_valid.csv'
score_csv='/home/1TB/Preprocessing_MOSEI_NEW/clean_label_files/csd_labels/CMU-MultimodalSDK/New_Chunked_Data/labels_CSV/' + branch
destination='/home/1TB/Preprocessing_MOSEI_NEW/clean_label_files/csd_labels/CMU-MultimodalSDK/New_Chunked_Data/labels_CSV/final_labels/'
no_label_des='/home/1TB/Preprocessing_MOSEI_NEW/clean_label_files/csd_labels/CMU-MultimodalSDK/New_Chunked_Data/labels_CSV/no_label/'

final_header_label = ['FileName','Emotion']

label_file=open(destination+branch, 'wt', newline ='')
writer_final = csv.writer(label_file, delimiter=',')
writer_final.writerow(i for i in final_header_label)

no_label_header=['FileName', 'happy', 'sad', 'anger', 'surprise', 'disgust', 'fear']

label_file_no_des=open(no_label_des+branch, 'wt', newline ='')
writer_no_des = csv.writer(label_file_no_des, delimiter=',')
writer_no_des.writerow(i for i in no_label_header)




def get_indexes_max_value(my_list):
    max_value = max(my_list)
    if my_list.count(max_value) > 1:
        return [i for i, x in enumerate(my_list) if x == max(my_list)]
    else:
        return [my_list.index(max(my_list))]






iter_f=0
with open(score_csv) as f:
    cf = csv.reader(f)
    for row in cf:
      
        if iter_f==0:
            
            label_names=row[1:7]
           
        
        if not iter_f==0:
            list_m=row[1:7]
            example_id=row[0]

          

            emotion_intensity = [float(i) for i in list_m] 
            indexes=get_indexes_max_value(emotion_intensity)

            combined_row_failed=[example_id]+list_m

            

            if len(indexes)>1:
                combined_row_failed=[example_id]+list_m
                writer_no_des.writerow(combined_row_failed)
            
            else:
                combined_row_final=[example_id]+[label_names[indexes[0]]]
                writer_final.writerow(combined_row_final)
               
        iter_f=iter_f+1
    