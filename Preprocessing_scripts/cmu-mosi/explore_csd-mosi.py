import h5py
from mmsdk import mmdatasdk
import csv
import os

from mosi_fold import *


#This file is to explore the CSD files and convert them in to train , valid and test folders
num_files=[]


#mydict={'Label':'./cmumosei/CMU_MOSEI_LabelsEmotions.csd'}
mydict={'Label':'./cmumosi/CMU_MOSI_Opinion_Labels.csd'}
mydataset=mmdatasdk.mmdataset(mydict)



raw_vid_path='./Video/Full/'
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

#header = ['segmentID','sentiment','start_t','end_t']

header = ['FileName','sentiment_score']

#my_segment_labels=mydataset.computational_sequences['Label'].data['0h-zjBukYpk']['features'][:]
#my_segment_durations=mydataset.computational_sequences['Label'].data['0h-zjBukYpk']['intervals'][:] #Seems like inverls are in order

train_csv=open('SDK_L_mosi/'+'train'+'.csv', 'wt', newline ='')
test_csv=open('SDK_L_mosi/'+'test'+'.csv', 'wt', newline ='')
valid_csv=open('SDK_L_mosi/'+'valid'+'.csv', 'wt', newline ='')

un_csv=open('SDK_L_mosi/'+'unknown'+'.csv', 'wt', newline ='')

writer_train = csv.writer(train_csv, delimiter=',')
writer_train.writerow(i for i in header)

writer_valid = csv.writer(valid_csv, delimiter=',')
writer_valid.writerow(i for i in header)


writer_test = csv.writer(test_csv, delimiter=',')
writer_test.writerow(i for i in header)

writer_un = csv.writer(un_csv, delimiter=',')
writer_un.writerow(i for i in header)


number_files=0


for file_name in num_files:
    my_data=[]

    
    for index,(L,D) in enumerate(zip(mydataset.computational_sequences['Label'].data[file_name]['features'][:],\
        mydataset.computational_sequences['Label'].data[file_name]['intervals'][:])):

        combined= [file_name+'_'+str(index)]+L.tolist() #+ D.tolist()
        my_data.append(combined)
        number_files=number_files+1

    

 
    for one_row in my_data:
        if file_name in standard_train_fold:
            writer_train.writerow(one_row)

        elif file_name in standard_test_fold:
            writer_test.writerow(one_row)

        elif file_name in standard_valid_fold:
            writer_valid.writerow(one_row)

        else:
            writer_un.writerow(one_row)

       

    # del my_data

print("number of files writen",number_files)

#number of files writen 23259