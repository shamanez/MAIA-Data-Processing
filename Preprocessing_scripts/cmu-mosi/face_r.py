#import face_recognition
import cv2
import numpy as np
import os
from PIL import Image


import insightface

model = insightface.model_zoo.get_model('retinaface_r50_v1')
model.prepare(ctx_id = -1, nms=0.4)

face_location = []
video_path = '/home/arei826/CMU-MultimodalSDK/cmu-mosi/raw/Video/Segmented/'
video_list = os.listdir(video_path)
size = 0
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
count = 0

for video in video_list:


   
    #Dialogue_ID = video.split('_')[0].split('dia')[-1]
    #Utterance_ID = video.split('.')[0].split('utt')[-1]
    video_capture = cv2.VideoCapture(video_path + video)

    framecount = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)



    success, frame = video_capture.read()
    size = 0
    frame_list = []
    frame_index = 0

    f_c=0

    
    while success:
        rgb_frame = frame[:, :, ::-1]

        # cv2.imshow('IMG_me',rgb_frame)
        # cv2.waitKey()
               
        #head_location = face_recognition.face_locations(rgb_frame)
        bbox, landmark = model.detect(rgb_frame, threshold=0.5, scale=1.0)

    
        bbox=bbox.astype(int)
      
   
        #print(head_location[0][0],head_location[0][2],head_location[0][3],head_location[0][1])
        #print(bbox[0][1],bbox[0][3],bbox[0][0],bbox[0][2])

      
        
        
        #####Only 1 face found#####
        #if len(head_location) == 1:

       

        if len(bbox) == 1:
            # print("only one frame")
            #cropped = frame[head_location[0][0]:head_location[0][2], head_location[0][3]:head_location[0][1]]
            cropped = frame[bbox[0][1]:bbox[0][3], bbox[0][0]:bbox[0][2]]

            # cv2.imshow('IMG_me',cropped)
            # cv2.waitKey()
        
            frame_list.append(cropped)
            if size < max(cropped.shape):
                size = max(cropped.shape)


        #####More than 1 face found#####
        #####Find the biggest face and crop#####
        #elif len(head_location) > 1:
        elif len(bbox) > 1:
       
            big_size = 0
            big_index = 0
            #for head_index in range(len(head_location)):
            for head_index in range(len(bbox)):
                #head_width = head_location[head_index][2] - head_location[head_index][0]
                head_width = bbox[head_index][3] - bbox[head_index][1]

                #head_height = head_location[head_index][1] - head_location[head_index][3]
                head_height = bbox[head_index][2] - bbox[head_index][0]

                head_size = head_width * head_height
                if big_size < head_size:
                    big_size = head_size
                    big_index = head_index
            #cropped = frame[head_location[big_index][0]:head_location[big_index][2], head_location[big_index][3]:head_location[big_index][1]]
          
            cropped = frame[bbox[big_index][1]:bbox[big_index][3], bbox[big_index][0]:bbox[big_index][2]]
            #cropped = frame[bbox[big_index+1][1]:bbox[big_index+1][3], bbox[big_index+1][0]:bbox[big_index+1][2]]

              

            frame_list.append(cropped)
     
            if size < max(cropped.shape):
                size = max(cropped.shape)
        #file_name = Dialogue_ID + '_' + Utterance_ID + '_' + str(index) + '.jpg'
        #cv2.imwrite(file_name, cropped)
        success, frame = video_capture.read()
        f_c=f_c+1
        #print('frame--',f_c,len(frame_list))


    if len(frame_list) != 0:
        print("writing",count)
        video = cv2.VideoWriter('/home/arei826/CMU-MultimodalSDK/cmu-mosi/raw/Video/Segmented/' + video, fourcc, fps, (size, size))
        for frame_index in range(len(frame_list)):
            # if count==5:
            #     print("------------------")
            #     print(frame_list[frame_index],size)
            #     print(frame_list[frame_index].shape)

            if min(frame_list[frame_index].shape[0],frame_list[frame_index].shape[1])<=0:
                #exit()
                continue

    
            img = cv2.resize(frame_list[frame_index], (size,size), interpolation = cv2.INTER_CUBIC)
            video.write(img)

        video.release()
    print('finished videos-',count)
    count += 1
