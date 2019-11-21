import os
import csv
import glob
import numpy as np 
from moviepy.editor import *
import subprocess




LABEL_CSV='/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/all_labels.csv'
REAL_LABELS='/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/formatted_labels.csv'
TEXT_PATH='/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/Transcript_N/Segmented/Combined'

video_path = '/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/Videos/Segmented/Combined/'
audio_path = '/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/FInal_data/audio/'
test_dir = '/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/FInal_data/text/'

label_names = ['angry', 'disgusted', 'afraid', 'happy', 'sad']
SENTIMENT_THRESHOLD = 1



# ############################# transcript #################################
with open(REAL_LABELS) as f:
    list_of_names = [row.split(',')[0] for row in f]




# print(list_of_names)
for filename in os.listdir(TEXT_PATH):

    try:
        print("try... - File : ", end='')
        print(filename)
        # print(filename, end='\tNumber of lines in file :')
        with open(TEXT_PATH + '/' + filename, 'r') as combined:
            # num_lines = sum(1 for line in combined)
            # print(num_lines)
            # # for line_number in range(num_lines):
            #     # line = combined.readline()
            # lines = combined.read().split('\n')
            # print(lines)
            # for line_index in range(len(lines)):
            #     line = lines[line_index]
            for line in combined:

            
       
                if '___' in line:
                    print("___ in line")
                    single_filename = '_'.join([line.split('___')[0], line.split('___')[1].split('___')[0]])
                    print(single_filename)
                    if single_filename in list_of_names:
                        print("found in list")
                        with open(test_dir + single_filename + ".txt", 'w') as out:
                            print(line.split('___')[4])
                            out.write(line.split('___')[4])
    except:
        print("except - File : ", end='')
        print(filename, end='\tNumber of lines in file :')
       
        with open(TEXT_PATH + '/' + filename, 'r', encoding="latin-1") as combined:
            # num_lines = sum(1 for line in combined)
            # print(num_lines)
            # # for line_number in range(num_lines):
            #     # line = combined.readline()
            # lines = combined.read().split('\n')
            # print(lines)
            # for line_index in range(len(lines)):
            #     line = lines[line_index]
            for line in combined:
                print(line)
                print("")
                if '___' in line:
                    print("___ in line")
                    single_filename = '_'.join([line.split('___')[0], line.split('___')[1].split('___')[0]])
                    print(single_filename)
                    if single_filename in list_of_names:
                        print("found in list")
                        with open(test_dir + single_filename + ".txt", 'w', encoding="latin-1") as out:
                            print(line.split('___')[4])
                            out.write(line.split('___')[4])
# ########################################################################################
