#import face_recognition
import cv2
import numpy as np
import os
from PIL import Image
import insightface

def facer(video_path,output_path):
    model = insightface.model_zoo.get_model('retinaface_r50_v1')
    model.prepare(ctx_id =0 , nms=0.4)
    
    face_location = []
    os.makedirs(output_path,exist_ok=True)
    video_list = os.listdir(video_path)
    
    size = 0
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    count = 0
    faces_dir = os.listdir(output_path) 
    for video in video_list:
        if video in faces_dir:
            count += 1
            continue
        video_capture = cv2.VideoCapture(os.path.join(video_path,video))
        framecount = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        success, frame = video_capture.read()
        size = 0
        frame_list = []
        frame_index = 0
        f_c=0
        while success:
            rgb_frame = frame[:, :, ::-1]
            bbox, landmark = model.detect(rgb_frame, threshold=0.5, scale=1.0)
            bbox=bbox.astype(int)
            
            #####Only 1 face found#####
            if len(bbox) == 1:
                cropped = frame[bbox[0][1]:bbox[0][3], bbox[0][0]:bbox[0][2]]
                frame_list.append(cropped)
                if size < max(cropped.shape):
                    size = max(cropped.shape)
    
            #####More than 1 face found#####
            #####Find the biggest face and crop#####
            #elif len(head_location) > 1:
            elif len(bbox) > 1:
           
                big_size = 0
                big_index = 0
                for head_index in range(len(bbox)):
                    head_width = bbox[head_index][3] - bbox[head_index][1]
                    head_height = bbox[head_index][2] - bbox[head_index][0]
                    head_size = head_width * head_height
                    if big_size < head_size:
                        big_size = head_size
                        big_index = head_index
              
                cropped = frame[bbox[big_index][1]:bbox[big_index][3], bbox[big_index][0]:bbox[big_index][2]]
    
                frame_list.append(cropped)
         
                if size < max(cropped.shape):
                    size = max(cropped.shape)
            success, frame = video_capture.read()
            f_c=f_c+1
    
        if len(frame_list) != 0:
            print("writing",count)
            video = cv2.VideoWriter(os.path.join(output_path,video), fourcc, fps, (size, size))
            
            for frame_index in range(len(frame_list)):
    
                if min(frame_list[frame_index].shape[0],frame_list[frame_index].shape[1])<=0:
                    continue
                img = cv2.resize(frame_list[frame_index], (size,size), interpolation = cv2.INTER_CUBIC)
                video.write(img)
            video.release()
        print('finished videos-',count)
        count += 1
