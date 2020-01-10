#import face_recognition
import cv2
import numpy as np
import os
import csv
from PIL import Image
import insightface

src_dir = './source/'
tgt_dir = './dest/'
error_dir = './dest/errors/'
error_csv = './mp4_errors.csv'
folder_depth = 2

videos_all = list()
completed = list()
error_fold = list()
errors = list()

for r,d,f in os.walk(src_dir):
    for vid in f:
      videos_all.append(os.path.join(r,vid))

for r,d,f in os.walk(error_dir):
    for vid in f:
      error_fold.append(os.path.join(r,vid))

for r,d,f in os.walk(tgt_dir):
    for vid in f:
        completed.append('/'.join(os.path.join(r,vid).split('/')[-folder_depth:]))
        
with open(error_csv, newline='') as csvfile:
    errors = [err[0]+'.mp4' if len(err) else err for err in csv.reader(csvfile)]
print('errors',errors)
print('/'.join(videos_all[1].split('/')[-folder_depth:]))
videos = [vid for vid in videos_all if '/'.join(vid.split('/')[-folder_depth:]) not in completed + errors]
print(videos)
total_count = len(videos_all)
error_fold_count = len(error_fold)
error_count = len(errors)
complete_count = len(completed) - error_fold_count
remaining_count = len(videos)

print('Total Videos:',total_count)
print('Errors on ',error_count,'videos.')
print('Completed ',complete_count,'videos.')
print('Remaining ',remaining_count,'videos.')

assert remaining_count + complete_count + error_count == total_count,'Assertion error, video count'

size = 0
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
count = remaining_count

model = insightface.model_zoo.get_model('retinaface_r50_v1')
model.prepare(ctx_id = 0, nms=0.4)

for video in videos: 
    filepath = video
    filename = os.path.basename(video)
    processed = False
    video_capture = cv2.VideoCapture(video)
    framecount = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    success, frame = video_capture.read()
    size = 0
    frame_list = []
    frame_index = 0

    while success:

        rgb_frame = frame[:, :, ::-1]
        bbox, landmark = model.detect(rgb_frame, threshold=0.5, scale=1.0)
        bbox=bbox.astype(int)

        if len(bbox) == 1:
            cropped = frame[max(bbox[0][1],0):bbox[0][3], max(bbox[0][0],0):bbox[0][2]]
            
            if cropped.shape[0] == 0:
                print(cropped)                
            frame_list.append(cropped)
            if size < max(cropped.shape):
                size = max(cropped.shape)

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
            cropped = frame[max(bbox[big_index][1],0):bbox[big_index][3], max(bbox[big_index][0],0):bbox[big_index][2]]

            frame_list.append(cropped)
    
            if size < max(cropped.shape):
                size = max(cropped.shape)
        success, frame = video_capture.read()
    video_capture.release()
    
    if len(frame_list) != 0:
        processed = True
        path = tgt_dir if len(frame_list)/framecount > 0.80 else error_dir 
        tgt_path = os.path.join(path,'/'.join(video.split('/')[-folder_depth:]))
        os.makedirs(os.path.dirname(tgt_path),exist_ok=True)
        video = cv2.VideoWriter(tgt_path, fourcc, fps, (size, size))
        for frame_index in range(len(frame_list)):

            if min(frame_list[frame_index].shape[0],frame_list[frame_index].shape[1])<=0:
                processed = False
                continue
    
            img = cv2.resize(frame_list[frame_index], (size,size), interpolation = cv2.INTER_CUBIC)
            video.write(img)

        video.release()
        new_framecount = cv2.VideoCapture(tgt_path).get(cv2.CAP_PROP_FRAME_COUNT)
        if new_framecount != framecount:
            processed = False
            print('Missing frames in',filename)

    if not processed:
        error_count += 1
        with open(error_csv,'a') as fd:
            writer = csv.writer(fd)
            writer.writerow(['/'.join(filepath[:-4].split('/')[-folder_depth:])])
    count -= 1
    print('Remaining:',count,'Complete:',round(100*(total_count-count)/total_count,2),'%','Errors:',error_count,round(100*(error_count/(total_count-count)),2),'%','File:', filename)
