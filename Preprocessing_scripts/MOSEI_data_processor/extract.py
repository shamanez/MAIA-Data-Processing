import os
import csv
import glob
import numpy as np 
from moviepy.editor import *
import subprocess




LABEL_CSV='/media/gsir059/Transcend/CMU-MOSEI-FULL-DATA-SET/all_labels.csv'
REAL_LABELS='/media/gsir059/Transcend/CMU-MOSEI-FULL-DATA-SET/formatted_labels.csv'
TEXT_PATH='/media/gsir059/Transcend/CMU-MOSEI-FULL-DATA-SET/Transcript/Segmented/Combined'

video_path = '/media/gsir059/Transcend/CMU-MOSEI-FULL-DATA-SET/Videos/Segmented/Combined/'
audio_path = '/media/gsir059/Transcend/CMU-MOSEI-FULL-DATA-SET/FInal_data/audio/'
test_dir = '/media/gsir059/Transcend/CMU-MOSEI-FULL-DATA-SET/FInal_data/text/'

label_names = ['angry', 'disgusted', 'afraid', 'happy', 'sad']
SENTIMENT_THRESHOLD = 1


# ########## Loading the label csv###################
# with open(LABEL_CSV) as in_file:
#     reader = csv.DictReader(in_file, delimiter=',')

#     ##### we create a new csv with example names########################
#     with open(REAL_LABELS, 'w') as out_file: #Save it as output csv
#         writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         row_count = 0 
#         for row in reader:
#             row_count = row_count + 2
#             if row['Input.VIDEO_ID']:
#                 print("\nyes\t", end='')
#                 label_name = []
#                 if row['Answer.anger']:
#                     label_name.append(int(float(row['Answer.anger'])))
#                 else:
#                     label_name.append(int(0))
#                 if row['Answer.disgust']:
#                     label_name.append(int(float(row['Answer.disgust'])))
#                 else:
#                     label_name.append(int(0))
#                 if row['Answer.fear']:
#                     label_name.append(int(float(row['Answer.fear'])))
#                 else:
#                     label_name.append(int(0))
#                 if row['Answer.happiness']:
#                     label_name.append(int(float(row['Answer.happiness'])))
#                 else:
#                     label_name.append(int(0))
#                 if row['Answer.sadness']:
#                     label_name.append(int(float(row['Answer.sadness'])))
#                 else:
#                     label_name.append(int(0))
#                 VIDEO_ID = '_'.join([row['Input.VIDEO_ID'], row['Input.CLIP']])
#                 if(np.amax(np.asarray(label_name)) >= SENTIMENT_THRESHOLD):
#                     LABEL = label_names[np.argmax(np.asarray(label_name))]
#                     writer.writerow([VIDEO_ID, LABEL])
#                     print([VIDEO_ID, LABEL], end='')
#                     print("\t\tprocessing row " + str(row_count), end='')
#                 label_name.clear()
#             else:
#                 print("No")
# #################################################################


# ############################# transcript #################################
# with open(REAL_LABELS) as f:
#     list_of_names = [row.split(',')[0] for row in f]
# # print(list_of_names)
# for filename in os.listdir(TEXT_PATH):
#     try:
#         print("try... - File : ", end='')
#         print(filename)
#         # print(filename, end='\tNumber of lines in file :')
#         with open(TEXT_PATH + '/' + filename, 'r') as combined:
#             # num_lines = sum(1 for line in combined)
#             # print(num_lines)
#             # # for line_number in range(num_lines):
#             #     # line = combined.readline()
#             # lines = combined.read().split('\n')
#             # print(lines)
#             # for line_index in range(len(lines)):
#             #     line = lines[line_index]
#             for line in combined:
#                 print(line)
#                 print("")
#                 if '___' in line:
#                     print("___ in line")
#                     single_filename = '_'.join([line.split('___')[0], line.split('___')[1].split('___')[0]])
#                     print(single_filename)
#                     if single_filename in list_of_names:
#                         print("found in list")
#                         with open(test_dir + single_filename + ".txt", 'w') as out:
#                             print(line.split('___')[4])
#                             out.write(line.split('___')[4])
#     except:
#         print("except - File : ", end='')
#         print(filename, end='\tNumber of lines in file :')
#         with open(TEXT_PATH + '/' + filename, 'r', encoding="latin-1") as combined:
#             # num_lines = sum(1 for line in combined)
#             # print(num_lines)
#             # # for line_number in range(num_lines):
#             #     # line = combined.readline()
#             # lines = combined.read().split('\n')
#             # print(lines)
#             # for line_index in range(len(lines)):
#             #     line = lines[line_index]
#             for line in combined:
#                 print(line)
#                 print("")
#                 if '___' in line:
#                     print("___ in line")
#                     single_filename = '_'.join([line.split('___')[0], line.split('___')[1].split('___')[0]])
#                     print(single_filename)
#                     if single_filename in list_of_names:
#                         print("found in list")
#                         with open(test_dir + single_filename + ".txt", 'w', encoding="latin-1") as out:
#                             print(line.split('___')[4])
#                             out.write(line.split('___')[4])
# ########################################################################################


########### Converting the mp4 files in to .wav of 16000K######
# video_list = os.listdir(video_path)
# vid_names=[v.split('.m')[0] for v in video_list]
# for video_name in vid_names:
#     video_filename = video_path + video_name +'.mp4'
#     audio_filename = audio_path + video_name +'.wav'
#     command = "ffmpeg -i " + video_filename + " -ab 160k -ac 2 -ar 44100 -vn " + audio_filename
#     subprocess.call(command, shell=True)
# 	# video = VideoFileClip(video_path + video_name +'.mp4')
# 	# audio = video.audio
# 	# file_name = video_name
# 	# audio.write_audiofile(audio_path + file_name + '.wav')
# ########################################################################################

# #Better check all 3 modalities##################
# #### Checker function###################
# #Check whether number of aud,vid and text are same
# video_list = os.listdir(video_path)

# audio_list = os.listdir(audio_path)

# vid_name=[v.split('.')[0] for v in video_list]
# aud_name=[a.split('.')[0] for a  in audio_list]

# if len(vid_name) < len(aud_name):
#     missing_vid_data=[x+".mp4" for x in aud_name if not x in vid_name]

# #################################################################
