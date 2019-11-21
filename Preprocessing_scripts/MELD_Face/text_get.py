import pandas as pd
import os

index_path = '../train_sent_emo.csv'
video_path = 'FaceVideo/'
emo_index = []
column_list = ['File_Name']
columns_to_get = ['Emotion','Sentiment','Utterance']
column_list.extend(columns_to_get)

index_file = pd.read_csv(index_path,index_col=['Dialogue_ID','Utterance_ID'])
video_list = os.listdir(video_path)
count = 0
for video_name in video_list:
    Dialogue_ID = int(video_name.split('_')[0].split('dia')[-1])
    Utterance_ID = int(video_name.split('.')[0].split('utt')[-1])
    
    get_row = index_file.loc[(Dialogue_ID,Utterance_ID),columns_to_get]
    
    one_line = []
    file_name = video_name.split('.')[0]
    one_line.append(file_name)
    one_line.extend(get_row.values)
    emo_index.append(one_line)

    with open('TextData/'+file_name+'.txt','w') as f:
    	
    	f.writelines(get_row[-1].encode("ascii", errors="ignore").decode())
    
video_index_data = pd.DataFrame(emo_index, columns=column_list)
video_index_data.to_csv('emo_index_9k_new.csv', index=False)
    



# import pandas as pd
# import os

# index_path = '../train_sent_emo.csv'
# video_path = 'FaceVideo/'
# emo_index = []
# column_list = ['File_Name', 'Emotion']

# index_file = pd.read_csv(index_path)
# video_list = os.listdir(video_path)

# for video_name in video_list:
# 	Dialogue_ID = video_name.split('_')[0].split('dia')[-1]
# 	Utterance_ID = video_name.split('.')[0].split('utt')[-1]
# 	for index in range(index_file.shape[0]):
# 		if index_file['Dialogue_ID'][index] == int(Dialogue_ID) and index_file['Utterance_ID'][index] == int(Utterance_ID):
# 			file_name = video_name.split('.')[0]
# 			emo_index.append([file_name, index_file['Emotion'][index]])

# video_index_data = pd.DataFrame(emo_index, columns=column_list)
# video_index_data.to_csv('emo_index_9k.csv', index=False)