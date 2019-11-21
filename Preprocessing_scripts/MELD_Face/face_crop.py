import face_recognition
import cv2
import numpy as np
import os
from PIL import Image

face_location = []
video_path = 'train_splits/'
video_list = os.listdir(video_path)
size = 0
fps = 24
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
count = 0

for video in video_list:
	Dialogue_ID = video.split('_')[0].split('dia')[-1]
	Utterance_ID = video.split('.')[0].split('utt')[-1]
	video_capture = cv2.VideoCapture(video_path + video)
	framecount = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
	success, frame = video_capture.read()
	size = 0
	frame_list = []
	frame_index = 0
	while success:
		rgb_frame = frame[:, :, ::-1]
		head_location = face_recognition.face_locations(rgb_frame)
		#####Only 1 face found#####
		if len(head_location) == 1:
			cropped = frame[head_location[0][0]:head_location[0][2], head_location[0][3]:head_location[0][1]]
			frame_list.append(cropped)
			if size < max(cropped.shape):
				size = max(cropped.shape)
		#####More than 1 face found#####
		#####Find the biggest face and crop#####
		elif len(head_location) > 1:
			big_size = 0
			big_index = 0
			for head_index in range(len(head_location)):
				head_width = head_location[head_index][2] - head_location[head_index][0]
				head_height = head_location[head_index][1] - head_location[head_index][3]
				head_size = head_width * head_height
				if big_size < head_size:
					big_size = head_size
					big_index = head_index
			cropped = frame[head_location[big_index][0]:head_location[big_index][2], head_location[big_index][3]:head_location[big_index][1]]
			frame_list.append(cropped)
			if size < max(cropped.shape):
				size = max(cropped.shape)
		#file_name = Dialogue_ID + '_' + Utterance_ID + '_' + str(index) + '.jpg'
		#cv2.imwrite(file_name, cropped)
		success, frame = video_capture.read()
	if len(frame_list) != 0:
		video = cv2.VideoWriter('FaceVideo/' + video, fourcc, fps, (size, size))
		for frame_index in range(len(frame_list)):
			img = cv2.resize(frame_list[frame_index], (size,size), interpolation = cv2.INTER_CUBIC)
			video.write(img)

		video.release()
	print(count)
	count += 1

