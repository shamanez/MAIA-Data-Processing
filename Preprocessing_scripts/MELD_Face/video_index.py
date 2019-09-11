import os
import pandas
import datetime as dt

video_path = 'Video/train_splits/'
column_list = ['Video_path', 'Emotion', 'Duration']
video_index = []

video_namelist = os.listdir(video_path)
emo_file = pandas.read_csv('train_sent_emo.csv')

for video_name in video_namelist:
	Dialogue_ID = video_name.split('_')[0].split('dia')[-1]
	Utterance_ID = video_name.split('.')[0].split('utt')[-1]
	for index in range(emo_file.shape[0]):
		if emo_file['Dialogue_ID'][index] == int(Dialogue_ID) and emo_file['Utterance_ID'][index] == int(Utterance_ID):
			start = emo_file['StartTime'][index].replace(',','.')
			end = emo_file['EndTime'][index].replace(',','.')
			start_time = dt.datetime.strptime(start, '%H:%M:%S.%f')
			end_time = dt.datetime.strptime(end, '%H:%M:%S.%f')
			Duration = end_time - start_time
			Emotion = emo_file['Emotion'][index]
			video_index.append([video_path + video_name, Emotion, Duration])

video_index_data = pandas.DataFrame(video_index, columns=column_list)
video_index_data.to_csv('train_split_index.csv', index=False)
