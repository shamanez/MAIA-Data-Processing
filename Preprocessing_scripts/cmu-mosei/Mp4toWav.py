import os
from moviepy.editor import *

video_path = '/home/1TB/Preprocessing_MOSEI_NEW/clean_label_files/csd_labels/CMU-MultimodalSDK/New_Chunked_Data/test/'
audio_path = '/home/1TB/Preprocessing_MOSEI_NEW/clean_label_files/csd_labels/CMU-MultimodalSDK/New_Chunked_Data/Audio/test/'
face_cropped='/home/1TB/Preprocessing_MOSEI_NEW/clean_label_files/csd_labels/CMU-MultimodalSDK/New_Chunked_Data/FaceVideo/test/'

video_list = os.listdir(video_path)

audio_list = os.listdir(audio_path)

face_list= os.listdir(face_cropped)

already_avaiable_aud=os.listdir(audio_path)


vid_f_name=[v.split('.')[0] for v in face_list]
aud_name=[a.split('.')[0] for a  in already_avaiable_aud]





for video_name in video_list:

	file_name = video_name.split('.')[0]

	

	# if file_name in ['94ULum9MYX0_3','3aIQUQgawaI_0']:
	# 	continue

	if file_name in aud_name:
		continue
	if file_name not in vid_f_name:
		continue

	try:
		video = VideoFileClip(video_path + video_name)
		audio = video.audio	
		audio.write_audiofile(audio_path + file_name + '.wav')
	except IndexError:
		print(video_name)
		continue
	
	
	

# for video_name in dif:
# 	video = VideoFileClip('train_splits/' + video_name+'.mp4')
# 	audio = video.audio
# 	file_name = video_name
# 	audio.write_audiofile('AudioData_new/' + file_name + '.wav')