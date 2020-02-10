import csv
import random

# create hashmap of annotate audio samples {id: [...filenames]}
eng_ids = set()
speaker_map = {}
with open('summary_85plus.csv') as inp:
    for row in csv.reader(inp):
        file = row[0]
        if len(file)==4:
            continue
        id = file[:7]
        eng_ids.add(id)
        if id in speaker_map:
            speaker_map[id].append(file)
        else:
            speaker_map[id] = [file]
eng_ids = list(sorted(eng_ids))

# remove id's where sample count is less than 5
to_del = list()
for key in speaker_map.keys():
    if len(speaker_map[key]) < 5:
        to_del.append(key)
for key in to_del:
    del speaker_map[key]

# create gender hashmap {id: m/f}
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
output = list()
for id in speaker_map.keys():
    for file in speaker_map[id]:
        row = [file]
        row += randomPair(file)
        row.append(gender_map[id])
        output.append(row)

# write csv rows into final output file
with open('speaker_detection_labels.csv','w') as inp:
    writer = csv.writer(inp)
    for row in output:
        writer.writerow(row)
        
