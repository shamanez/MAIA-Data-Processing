import h5py
from mmsdk import mmdatasdk
import csv


# TODO: This file is to explore the CSD files and convert them in to train , valid and test folders

# This file converts a .csd file and creates individual csv files for each segment+score

# Define input .csd and output .csv
input_dir = '/home/arei826/CMU-MultimodalSDK/cmu-mosei-labels/CMU_MOSEI_LabelsEmotions.csd'
output_dir = '/home/arei826/CMU-MultimodalSDK/Labels/'
csv_prefix = 'LabelsEmotions'

# Load dictionary of .csd files into dictionary
mydataset=mmdatasdk.mmdataset({0:input_dir})
mydic = mydataset.computational_sequences[0].data

print('Loaded Computational Sequence Data (.csd) into dictionary...')

# List data id's in num_files
num_files=[]
for key, value in mydic.items() :
    num_files.append(key)

# Shape and length check
print('Total file number: ',len(num_files))
print('Contains duplicates: ',len(num_files)==len(set(num_files)))
print('Features shape: ',mydic['22689']['features'][:].shape)
print('Intervals shape: ',mydic['22689']['intervals'][:].shape)
print('Finished loading features and intervals')

# Create headers
print("Writing labels and durations to csv file for each full video..")
header = ['segmentid','happy','sad','anger','surprise','disgust','fear','start_t','end_t']

# Zip intervals & features, append to my_data, write data to individual .csv
for file_name in num_files:
    my_data=[]

    for index,(l,d) in enumerate(zip(mydic[file_name]['features'][:], mydic[file_name]['intervals'][:])):
        combined= [index]+l.tolist() + d.tolist()
        my_data.append(combined)

    with open(output_dir + csv_prefix + '_'+file_name+'.csv', 'wt', newline ='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(i for i in header)
        for one_row in my_data:
            #print(one_row)
            writer.writerow(one_row)

    del my_data
