import csv
import random

# get all english speaker id's
print('getting speaker ids...')
eng_ids = set()
with open('summary_85plus.csv') as inp:
    for row in csv.reader(inp):
        file = row[0]
        if len(file)==4:
            continue
        id = file[:7]
        eng_ids.add(id)
eng_ids = list(sorted(eng_ids))

# create speaker map of all audio samples {id:[..filenames]}
print('creating speaker map...')
speaker_map = {}
for id in eng_ids:
    speaker_map[id] = list()
with open('aud2text_shuffled.csv') as inp:
    for row in csv.reader(inp):
        file = row[0][16:-4]
        id = file[:7]
        if id in speaker_map:
            speaker_map[id].append(file)

# create gender hashmap {id: m/f}
print('creating gender map...')
gender_map = {}
with open('vox2_meta.csv') as inp:
    for row in csv.reader(inp):
        id = row[0][:7]
        gender = row[2][0]
        gender_map[id] = gender

# predefined random pairs for dataloader
def randomPair(file):
    id = file[:7]
    if random.random() < 0.5:
        # random sample from same speaker
        samples = [s for s in speaker_map[id] if s != file]
        return [random.choice(samples),True]
    else:
        # random sample from random speaker
        keys = [key for key in speaker_map.keys() if key != id]
        random_id = random.choice(keys)
        return [random.choice(speaker_map[random_id]),False]

# create array of arrays for writing to csv [file1, file2, same?,gender]
print('generating results...')
output = list()
for id in speaker_map.keys():
    for file in speaker_map[id]:
        row = [file]
        row += randomPair(file)
        row.append(gender_map[id])
        output.append(row)

# write csv rows into final output file
print('writing results to csv...')
with open('speaker_detect_labels_all.csv','w') as inp:
    writer = csv.writer(inp)
    for row in output:
        writer.writerow(row)
        
