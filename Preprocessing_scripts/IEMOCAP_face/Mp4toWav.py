import os
from moviepy.editor import *

video_path = 'FaceVideo/'
audio_path = 'AudioData/'

video_list = os.listdir(video_path)

audio_list = os.listdir(audio_path)

vid_name=[v.split('.')[0] for v in video_list]
aud_name=[a.split('.')[0] for a  in audio_list]





# for video_name in video_list:
# 	video = VideoFileClip('train_splits/' + video_name)
# 	audio = video.audio
# 	file_name = video_name.split('.')[0]
# 	audio.write_audiofile('AudioData/' + file_name + '.wav')

for video_name in dif:
	video = VideoFileClip('train_splits/' + video_name+'.mp4')
	audio = video.audio
	file_name = video_name
	audio.write_audiofile('AudioData_new/' + file_name + '.wav')