# Please follow the following steps to extract and preprocess the cmu-mosei data

## Raw data and Labels 

1. First download the raw cmu-mosei data from CMU-SDK
2. Then download the CSD files that consist of emotion labels and sentiments labels for mosei data set


## Extracting labels for video segments

1. Once array of the CSD file consist of name of the combined video and labels for each segment (start and end time is give).

2. First run the **explore_csd-sentiments.py** to extracts all details of examples to seperate csv files.

3. Then run **gen_labels_sentiments.py** to extract only the information related to labels from the above created csv files.

4. Finally run **decide_labels_sentiments.py** to assign an unique label to every examples

## Processing raw data

1. Use **cut_v-sentiments.py** to chunk full videos in the raw data to segments (these segments are decided by label CSD files)

2. The run **face_r.py** to capture faces from the each frame and save them as seperate mp4 files.

3. Then to get the .wav form run **Mp4toWav.py** to convert mp4 to wave. Also , by running **cut_audio.py** the wav chunks can be extracted directly from combined wavforms given in the raw data (this one is better).

4. Then run **process_transcript-senti.py** to extract text


## Ready to train

1. Finally run checker-senti.py to cross check the avaiability of all three modalities and allign them to feed in to a given dataloader. 