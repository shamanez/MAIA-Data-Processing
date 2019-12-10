import h5py
from mmsdk import mmdatasdk
import csv


#This file is to explore the CSD files and convert them in to train , valid and test folders

num_files=[]

mydict={'Label':'./cmumosei/CMU_MOSEI_LabelsEmotions.csd'}
mydataset=mmdatasdk.mmdataset(mydict)

mydic=mydataset.computational_sequences['Label'].data

for key, value in mydic.items() :
    num_files.append(key)

print(len(num_files))

exit("-----------------------")

unq_list=list (set (num_files))

print(len(unq_list))

print("writing labels and durations to csv file for each full video")

header = ['segmentID','happy','sad','anger','surprise','disgust','fear','start_t','end_t']

my_segment_labels=mydataset.computational_sequences['Label'].data['-3g5yACwYnA']['features'][:]
my_segment_durations=mydataset.computational_sequences['Label'].data['-3g5yACwYnA']['intervals'][:]






for file_name in num_files:
    my_data=[]



    for index,(L,D) in enumerate(zip(mydataset.computational_sequences['Label'].data[file_name]['features'][:],\
        mydataset.computational_sequences['Label'].data[file_name]['intervals'][:])):
    
        combined= [index]+L.tolist() + D.tolist()
        my_data.append(combined)


    with open('SDK_L/'+file_name+'.csv', 'wt', newline ='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(i for i in header)
        for one_row in my_data:
            #print(one_row)
            writer.writerow(one_row)
    
    del my_data




