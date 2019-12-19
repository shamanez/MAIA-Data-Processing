CMU-MOSI Dataset

1. git clone https://github.com/A2Zadeh/CMU-MultimodalSDK
2. copy all files into the above folder
3. pip3 install -r requirements.txt
4. python3 cmumosi_setup.py

This will download all raw files
Pre-process audio/text/video

- currently ctx_ID in cropFace.py is set to 0, i.e. using first GPU available. set it to <0 if youd like to use CPU
- 
