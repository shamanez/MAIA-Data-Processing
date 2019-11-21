import os

video_path = 'FaceVideo/'
audio_path = 'Audio/'

video_list = os.listdir(video_path)

audio_list = os.listdir(audio_path)

vid_name=[v.split('.')[0] for v in video_list]
aud_name=[a.split('.')[0] for a  in audio_list]


missing_vid_data=[x+".mp4" for x in aud_name if not x in vid_name]

	



CUDA_VISIBLE_DEVICES=0
import face_recognition
import cv2
import numpy as np
import os
from PIL import Image

face_location = []
video_path = 'Video/'#'train_splits/'
video_list = missing_vid_data

size = 0
fps = 24#24 (For the MELD)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
count = 0


for video in video_list:
	print("start")
	# Dialogue_ID = video.split('_')[0].split('dia')[-1]
	# Utterance_ID = video.split('.')[0].split('utt')[-1]
	Utterance_ID=video.split('_')[0]
	emotion_l=video.split('_')[1].split('.')[0]
	video_capture = cv2.VideoCapture(video_path + video)
	framecount = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
	success, frame = video_capture.read()

	size = 0
	frame_list = []
	frame_list_2 = []
	frame_index = 0
	
	while success:
		width = len(frame[0,:,0])
		rgb_frame= frame[:, : width//2, ::-1]
		#rgb_frame= frame[:, : width, ::-1]
		# cv2.imshow('IMG_me',rgb_frame)
		# cv2.waitKey()
		# exit("---==")
		head_location = face_recognition.face_locations(rgb_frame)

	

		if len(head_location) < 1:
			print("Warning :Cannot find the face in this fraeme")
			success, frame = video_capture.read()
			continue

	

		cropped = frame[head_location[0][0]:head_location[0][2], head_location[0][3]:head_location[0][1]]
		size=max(cropped.shape)
		frame_list.append(cropped)

		success, frame = video_capture.read()

	video = cv2.VideoWriter('missed_vid/' + video, fourcc, fps, (size, size))


	for frame_index in range(len(frame_list)):
		img = cv2.resize(frame_list[frame_index], (size,size), interpolation = cv2.INTER_CUBIC)
		video.write(img)
	video.release()


	print(count)
	
	count += 1

