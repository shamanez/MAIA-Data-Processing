import os
import csv
import glob
import numpy as np 
from moviepy.editor import *
import subprocess

from shutil import copyfile

my_base='/home/1TB/Preprocessing_MOSEI_NEW/clean_label_files/csd_labels/CMU-MultimodalSDK/New_Chunked_Data/processed'

label_base=my_base + '/labels/final_labels/'

LABEL_CSV=label_base + 'label_file_valid.csv' # IF TRAIN

split_dir='/valid/'

video_path = my_base+'/facevid' + split_dir
audio_path = my_base+'/audio' + split_dir
text_path =  my_base+'/text' + split_dir



label_names = ['happy', 'sad', 'anger', 'surprise', 'disgust', 'fear']


text_fn=[]
aud_fn=[]
vid_fn=[]

labeled_ex=[]

cmn_files=[]

for filename in os.listdir(audio_path):
    if filename.endswith(".wav"):
        aud_fn.append(filename.split('.')[0])

print("number of wav files",len(aud_fn))




for filename in os.listdir(video_path):
    if filename.endswith(".mp4"):
    
        vid_fn.append(filename.split('.')[0])

print("Number of mp4 files",len(vid_fn))


for filename in os.listdir(text_path):
    if filename.endswith(".txt"):
    
        text_fn.append(filename.split('.')[0])

print("Number of text files",len(text_fn))



with open(LABEL_CSV) as f:
    cf = csv.reader(f)

    for row in cf:

       
        if row[0]=='FileName':
            continue
        else:


            labeled_ex.append(row[0])
            


print("length of the labeld examples",len(labeled_ex))




#Checking the common number of examples 

for ele in text_fn:
    if ele in aud_fn and ele in vid_fn:
        cmn_files.append(ele)
    


print("number of common files in three modalities",len(cmn_files))


header_label_final = ['FileName','Emotion']

label_check=open(my_base+'/label_file_valid'+'.csv', 'wt', newline ='')

writer_check = csv.writer(label_check, delimiter=',')
writer_check.writerow(i for i in header_label_final)




tsvfile_a=open(my_base+'/valid_a.tsv', 'w')
tsvfile_v=open(my_base+'/valid_v.tsv', 'w')
tsvfile_t=open(my_base+'/valid_t.tsv', 'w')


with open(LABEL_CSV) as f:
    cf = csv.reader(f)

    for row in cf:
        
        if row[0]=='FileName':
            continue
        elif row[0] in cmn_files :

            combined_row=row[0:2]
            
           
            writer_check.writerow(combined_row)
            tsvfile_a.writelines(row[0]+'.wav'+'\n')
            tsvfile_v.writelines(row[0]+'.mp4'+'\n')
            tsvfile_t.writelines(row[0]+'.txt'+'\n')
        
        else:
            continue

