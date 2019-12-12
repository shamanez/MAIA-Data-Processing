import h5py
from mmsdk import mmdatasdk
import csv
import os


#This file is to explore the CSD files and convert them in to train , valid and test folders
num_files=[]

#mydict={'Label':'./cmumosei/CMU_MOSEI_LabelsEmotions.csd'}
mydict={'Label':'./cmumosei/CMU_MOSEI_LabelsSentiment.csd'}
mydataset=mmdatasdk.mmdataset(mydict)

raw_vid_path='/media/gsir059/Transcend/Raw_Data/CMU-MOSEI-raw-original/Raw/Videos/Full/Combined/'
raw_vid_files=[]



for filename in os.listdir(raw_vid_path):
    if filename.endswith(".mp4"):
        raw_vid_files.append(filename.split('.')[0])

print('number of raw full video files',len(raw_vid_files))

mydic=mydataset.computational_sequences['Label'].data


for key, value in mydic.items() :
    
    num_files.append(key)

print('number of annotated raw full video files',len(num_files))

unq_list=list (set (num_files))

#writing the missing lebels for given raw video in a text file
# my_missing=open("examples_with_missing_labels.txt", "w")
# 
# 
# for ele in raw_vid_files:
    # if ele not in unq_list:
        # print(ele)
        # my_missing.write(ele+'\n')


print("writing labels and durations to csv file for each full video")

header = ['segmentID','sentiment','start_t','end_t']

#my_segment_labels=mydataset.computational_sequences['Label'].data['-3g5yACwYnA']['features'][:]
#my_segment_durations=mydataset.computational_sequences['Label'].data['-3g5yACwYnA']['intervals'][:]



number_files=0


for file_name in num_files:
    my_data=[]

    
    for index,(L,D) in enumerate(zip(mydataset.computational_sequences['Label'].data[file_name]['features'][:],\
        mydataset.computational_sequences['Label'].data[file_name]['intervals'][:])):

        combined= [index]+L.tolist() + D.tolist()
        my_data.append(combined)
        number_files=number_files+1

    with open('SDK_L_senti/'+file_name+'.csv', 'wt', newline ='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(i for i in header)
        for one_row in my_data:
            #print(one_row)
            writer.writerow(one_row)
    
    # del my_data

print("number of files writen",number_files)

#number of files writen 23259