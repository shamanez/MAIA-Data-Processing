import os
import cv2

filelist = os.listdir('../Video/')

fps = 12

file_path = 'test.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

video = cv2.VideoWriter(file_path, fourcc, fps, (150, 150))

for item in filelist:
	if item.endswith('.jpg'):
		print(item)
		img = cv2.imread(item)
		img = cv2.resize(img, (150,150), interpolation = cv2.INTER_CUBIC)
		video.write(img)

video.release()