import os
import csv
import glob
import numpy as np 
from moviepy.editor import *
import subprocess

from shutil import copyfile

my_base='/media/gsir059/Carrier/face_cropped-MELD/MELD.Raw/Test_Data/'

LABEL_CSV=my_base+'emo_index_test.csv'



video_path = my_base+'facevid'
audio_path = my_base+'audio'
text_path =  my_base+'text'


label_names = ['neutral', 'fear', 'surprise', 'anger', 'joy','disgust','sadness']


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
       
        if row[0]=='File_name':
            continue
        else:
            labeled_ex.append(row[0])
            #print(row[0])
            #emotion_scores=row[1:7]
            # combined_row=row[1:2]
            # writer_train.writerow(combined_row)


print("length of the labeld examples",len(labeled_ex))




#Checking the common number of examples 

for ele in vid_fn:
    if ele in aud_fn and ele in text_fn:
        cmn_files.append(ele)
    


header_label_final = ['FileName','Emotion']

label_train=open(my_base+'label_file_test'+'.csv', 'wt', newline ='')

writer_train = csv.writer(label_train, delimiter=',')
writer_train.writerow(i for i in header_label_final)



print("number of common files across modalities",len(cmn_files))

tsvfile_a=open(my_base+'test_a.tsv', 'w')
tsvfile_v=open(my_base+'test_v.tsv', 'w')
tsvfile_t=open(my_base+'test_t.tsv', 'w')


with open(LABEL_CSV) as f:
    cf = csv.reader(f)

    for row in cf:
       
        if row[0]=='File_name':
            continue
        elif row[0] in cmn_files :
        
            combined_row=row[0:2]
           
            writer_train.writerow(combined_row)
            tsvfile_a.writelines(row[0]+'.wav'+'\n')
            tsvfile_v.writelines(row[0]+'.mp4'+'\n')
            tsvfile_t.writelines(row[0]+'.txt'+'\n')




exit()