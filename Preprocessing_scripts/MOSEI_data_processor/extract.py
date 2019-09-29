import os
import csv

from moviepy.editor import *

LABEL_CSV=''

REAL_LABELS='output.csv'

TEXT_PATH='.transcriptions/'


video_path = 'Video/'
audio_path = 'Audio/'

import glob



########## Loading the label csv###################
with open(LABEL_CSV) as f:
    reader = csv.reader(f)

    ##### we create a new csv with example names########################
    with open(REAL_LABELS, 'w') as g: #Save it as output csv
        writer = csv.writer(g)
        for row in reader:
            new_row = ['_ '.join([row[0], row[1]])]
            writer.writerow(new_row)
#################################################################


#Load the new csv and save all the example names to a list #################################

with open(REAL_LABELS) as f:
    example_names = [line.split() for line in f]
###########################################################################



######## Go to the folder that has text transcriptions##################
full_text_files = []
for file in glob.glob("*.txt"):
    full_text_files.append(file)

########################################################################

################take each example and find the relevent text ##############

for example_name in example_names:
    if example_name.split("-") in full_text_files:
        print("example found")
        ###########
        #Extract the text
        #save as a new .txt file with example_name (should match with video name)
        ###########


########################################################################################


########### Converting the mp4 files in to .wav of 16000K######

video_list = os.listdir(video_path)

vid_names=[v.split('.')[0] for v in video_list]


for video_name in vid_names:
	video = VideoFileClip(video_name+'.mp4')
	audio = video.audio
	file_name = video_name
	audio.write_audiofile(audio_path + file_name + '.wav')



#Better check all 3 modalities##################
#### Checker function###################
#Check whether number of aud,vid and text are same
video_list = os.listdir(video_path)

audio_list = os.listdir(audio_path)

vid_name=[v.split('.')[0] for v in video_list]
aud_name=[a.split('.')[0] for a  in audio_list]

if len(vid_name) < len(aud_name):
    missing_vid_data=[x+".mp4" for x in aud_name if not x in vid_name]

#################################################################



