import os
import csv
import glob
import numpy as np 
from moviepy.editor import *
import subprocess

from shutil import copyfile


LABEL_CSV='/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/all_labels.csv'
REAL_LABELS='/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/formatted_labels.csv'
TEXT_PATH='/home/gsir059/Videos/Transcript_N/Segmented/Combined'


video_path = '/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/Videos/Segmented/Combined/'
audio_path = '/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/FInal_data/audio/'
text_path = '/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/FInal_data/text/'


label_names = ['angry', 'disgusted', 'afraid', 'happy', 'sad']
SENTIMENT_THRESHOLD = 1


text_fn=[]
aud_fn=[]
vid_fn=[]


for filename in os.listdir(audio_path):
    if filename.endswith(".wav"):
        aud_fn.append(filename.split('.')[0])

print("number of wav files",len(aud_fn))


for filename in os.listdir(video_path):
    if filename.endswith(".mp4"):
    
        vid_fn.append(filename.split('.')[0])

print("Number of mp4 files",len(vid_fn))


#complete_av = open("complete_av.txt", "w")

complete_av_names=[]


Index=0
for ele in vid_fn:
  
    if ele in aud_fn:
        
        #complete_av.writelines(ele + "\n")
        complete_av_names.append(ele.split("_")[0])
        Index=Index+1


print("Number of complete aud_mp4",Index)





for filename in os.listdir(TEXT_PATH):
   
   
    if filename.endswith(".txt"):
        text_fn.append(filename)



# print(list_of_names)
for filename in os.listdir(TEXT_PATH):


    with open(TEXT_PATH + '/' + filename, 'r') as combined:

        for line in combined:

            if '___' in line:
                single_filename = '_'.join([line.split('___')[0], line.split('___')[1].split('___')[0]])
                with open(text_path + single_filename + ".txt", 'w') as out:
                    print(line.split('___')[4])
                    out.write(line.split('___')[4])


