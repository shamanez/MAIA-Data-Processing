import os 
from moviepy.editor import *
import csv
from shutil import copyfile

#anger, excitement (happiness), neutral and sadness IEMOCAP

LABEL_CSV='/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/all_labels.csv'
REAL_LABELS='/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/formatted_labels.csv'
TEXT_PATH='/home/gsir059/Videos/Transcript_N/Segmented/Combined'


video_path = '/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/Videos/Segmented/Combined/'

mosi_video_path = '/home/gsir059/Videos/Data-CMU-MOSI/Raw/Video/Segmented'

audio_path = '/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/FInal_data/audio/'
text_path = '/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/FInal_data/text/'

label_names = ['angry', 'disgusted', 'afraid', 'happy', 'sad']


text_fn=[]
aud_fn=[]
vid_fn=[]

vid_fn_mosi=[]

all_ex=[]

labeled_ex=[]


final_training_data=[]

corrupted_vid=[]

THE_FINAL=[]

final_labels =  open("L.txt")

for row_l in final_labels:
   
    THE_FINAL.append(row_l.split(",")[0])





for filename in os.listdir(audio_path):
  
    if filename.endswith(".wav"):
        if filename.split('.')[0] in THE_FINAL:
            copyfile('/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/FInal_data/audio/'+filename, "/home/gsir059/Documents/Paper Evaluation/MAIA-Data-Processing/Preprocessing_scripts/MOSEI_data_processor/audio/"+filename)
           
        aud_fn.append(filename.split('.')[0])

print("number of wav files",len(aud_fn))


for filename in os.listdir(video_path):
    if filename.endswith(".mp4"):
        if filename.split('.')[0] in THE_FINAL:
            copyfile('/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/Videos/Segmented/Combined/'  +filename, '/home/gsir059/Documents/Paper Evaluation/MAIA-Data-Processing/Preprocessing_scripts/MOSEI_data_processor/video/'+filename)
    
        vid_fn.append(filename.split('.')[0])

print("Number of mp4 files",len(vid_fn))


for filename in os.listdir(mosi_video_path):
    if filename.endswith(".mp4"):
    
        vid_fn_mosi.append(filename.split('.')[0])

print("Number of mp4-mosi files",len(vid_fn_mosi))



# missing_t = open("missing.txt", "w")

# R=0

for file_n in vid_fn:
    if not file_n in aud_fn:
        corrupted_vid.append(file_n)




    
#         # video = VideoFileClip(video_path + video_name+'.mp4')
#         # exit()
#         # audio = video.audio
#         # file_name = video_name
#         # audio.write_audiofile('AudioData_new/' + file_name + '.wav')
#         file_n=file_n+".mp4"
#         missing_t.writelines(file_n + "\n")
#         R=R+1




for filename in os.listdir(text_path):
    if filename.endswith(".txt"):
        if filename.split('.')[0] in THE_FINAL:
            copyfile('/home/gsir059/Documents/PhD/CMU-MOSEI-FULL-DATA-SET/FInal_data/text/' +filename, '/home/gsir059/Documents/Paper Evaluation/MAIA-Data-Processing/Preprocessing_scripts/MOSEI_data_processor/text/'+filename)
    
        text_fn.append(filename.split('.')[0])

print("Number of text files",len(text_fn))

exit()
for element in vid_fn:

    if (element in text_fn) and (element in aud_fn):
        all_ex.append(element)

print("--------------------------------------------------------")

print("all the examples",len(all_ex))

print("--------------------------------------------------------")

with open(REAL_LABELS) as f:
    for row in f:
        labeled_ex.append(row.split(",")[0])


print("Number of labeled examples",len(labeled_ex))

print()


for element_z in all_ex:
    if element_z in labeled_ex:
        final_training_data.append(element_z)


print("final number avaiable of training data",len(final_training_data))

print("------------------------------------------------------------------------------------------------")
print("Saving only the effective labeles")
X=0

f =  open("L.txt", "w")

F_lab = open(REAL_LABELS)

for row in F_lab:


    if row.split(",")[0] in final_training_data:
        print(row.split(",")[1])
        f.writelines(row+"\n")
        X=X+1

exit()

with open(REAL_LABELS) as f:
    for row in f:
        if row.split(",")[0] in final_training_data:
            print(row.split(",")[1])
            # f.writelines(row.split(",")[0] +"\n")
            X=X+1



print(X)


exit("----------------------======")






















print("Checkiing the missing Labeled DATA")
z=0
G=0
for my_lable in labeled_ex:
    if not my_lable in final_training_data:
        z=z+1

        if my_lable in vid_fn_mosi:
            print(my_lable)
            G=G+1
        # if my_lable not in corrupted_vid:
        #     #print(my_lable)
            


print("Number of labeled data missing",G)

