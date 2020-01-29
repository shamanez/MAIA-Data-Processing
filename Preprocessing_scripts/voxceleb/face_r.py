import cv2
import numpy as np
import os
import csv
from PIL import Image
import insightface

src_dir = './video/dev/mp4/'
shuffled_list = './face_r_shuffled.csv'
tgt_dir = './faces/dev/'
error_dir = './faces/errors/'
error_csv = './mp4_errors.csv'
frameloss_csv = './face_r_results.csv'
folder_depth = 3 

videos_all = list()
completed = list()
error_fold = list()
errors = list()

# for r,d,f in os.walk(src_dir):
#     for vid in f:
#       videos_all.append(os.path.join(r,vid))
print('Checking shuffled csv...')

last = './video/dev/mp4/id03213/1teBxPnEm7Y/00001.mp4'
#28jan, 11am

count=0
with open(shuffled_list) as shuffled:
    readCSV = csv.reader(shuffled, delimiter=',')
    add=False
    for vid in readCSV:
        count+=1
        if vid[0] == last:
            add = True
        if add:
            videos_all += vid 
# print(len(videos_all))
# exit()

print('Checking error folder...')
for r,d,f in os.walk(error_dir):
    for vid in f:
      error_fold.append(os.path.join(r,vid))
 
# print('Checking completed folder...')
# for r,d,f in os.walk(tgt_dir):
#     for vid in f:
#         completed.append('/'.join(os.path.join(r,vid).split('/')[-folder_depth:]))
#         
# with open(error_csv, newline='') as csvfile:
#     errors = [err[0]+'.mp4' if len(err) else err for err in csv.reader(csvfile)]
# 
# print('Filtering list for incompolete videos...')
# videos = [vid for vid in videos_all if '/'.join(vid.split('/')[-folder_depth:]) not in set(completed + errors)]

total_count = len(videos_all)
error_fold_count = len(error_fold)
error_count = len(errors)
#complete_count = len(completed) - error_fold_count
#remaining_count = len(videos)

# print('Total Videos:',total_count)
# print('Errors on ',error_count,'videos.')
# print('Completed ',complete_count,'videos.')
# print('Remaining ',remaining_count,'videos.')

# assert remaining_count + complete_count + error_count == total_count,'Assertion error, video count'

size = 0
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
count = len(videos_all) 

model = insightface.model_zoo.get_model('retinaface_r50_v1')
model.prepare(ctx_id = 0, nms=0.4)

for video in videos_all: 
    filepath = video
    logging_name = '/'.join(video.split('/')[-folder_depth:])
    filename = os.path.basename(video)
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
    framelist_len = len(frame_list) 
    if framelist_len != 0:
        with open(frameloss_csv,'a') as fd:
            writer = csv.writer(fd)
            writer.writerow(filepath[:-4].split('/')[-folder_depth:] + [framelist_len,framecount,framelist_len/framecount])
        path = tgt_dir if framelist_len/framecount > 0 else error_dir 
        tgt_path = os.path.join(path,'/'.join(video.split('/')[-folder_depth:]))
        os.makedirs(os.path.dirname(tgt_path),exist_ok=True)
        video = cv2.VideoWriter(tgt_path, fourcc, fps, (size, size))
        for frame_index in range(framelist_len):

            img = cv2.resize(frame_list[frame_index], (size,size), interpolation = cv2.INTER_CUBIC)
            video.write(img)

        video.release()
        new_framecount = cv2.VideoCapture(tgt_path).get(cv2.CAP_PROP_FRAME_COUNT)
    else:
        error_count += 1
        with open(error_csv,'a') as fd:
            writer = csv.writer(fd)
            writer.writerow(['/'.join(filepath[:-4].split('/')[-folder_depth:])])
    count -= 1
    print('Remaining:',count,'Complete:',round(100*(total_count-count)/total_count,2),'%','Errors:',error_count,round(100*(error_count/(total_count-count)),2),'%','File:', logging_name)
