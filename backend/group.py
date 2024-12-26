from unionfind import UnionFind 
from Video import Video
import random
from os import listdir
from collections import defaultdict
from FingerprintComparator import FingerprintComparator

# pull down a hashmap of ids with fingerprint and group
# also pull a hashmap of group id to audoi files
# ids = {audio_id: [fingerprint, group]}
# groups = {group_id: [audio_id1, audio_id2, ...]}

# input each fingerprint into DSU
# run pairwise similarity on every id
# if similar union 2 ids in dsu
# if you union 2 ids, use the hashmap to change the group id of the smaller group to the larger group
# might be more efficient to find the group id of largest group in that group, then use merge all others to that
# if no group id, then generate new ones


# ids = {
#     "a1": [random.sample(range(1, 2), 1), "1"],
#     "a2": [random.sample(range(1, 2), 1), "1"],
#     "a3": [random.sample(range(1, 3), 2), "2"],
#     "a4": [random.sample(range(1, 3), 2), "2"],
#     "a5": [random.sample(range(1, 4), 3), "3"],
#     "a6": [random.sample(range(1, 5), 4), "4"],
#     "a7": [random.sample(range(1, 5), 4), "4"],
#     "a8": [random.sample(range(1, 3), 2), "2"],
# }

# groups = {"1": ["a1", "a2"], "2": ["a3", "a4", "a8"], "3": ["a5"], "4": ["a6", "a7"]}
# toAdd = {"a9":[1,2,3,4,1], "a10":[1,2,3], "a11":[1,2,3,4,5], "a12":[1,2], "a13":[1]}

## for testing ^^^

ids = {}
toAdd = {}


path = r"C:\Users\ethan\OneDrive\Desktop\Programming\temp"
for filename in listdir(path):  # iterates over all the files in 'path'
    if filename.endswith(".mp4") or filename.endswith(".MP4"):
        video = Video(path+"\\"+filename)
        video.extractAudio()
        video.generateFingerprint()
        toAdd[video.fileName] = video.fingerprint.fingerprints


# form existing groups
uf = UnionFind()
# for (groupId, audioFiles) in groups.items():
#     for audioFile in audioFiles:
#         uf.add(audioFile)
#         uf.union(groups[groupId][0], audioFile)

# add new audio files
for (audioFile, fingerprint) in toAdd.items():
    uf.add(audioFile)
    for (audioFile2, fingerprint2) in ids.items():
        fc = FingerprintComparator(fingerprint, fingerprint2)
        print (audioFile, " ", audioFile2)
        print (len(fingerprint), " ", len(fingerprint2))
        if (fc.getBestScore(fc.crossCorrelate()) >= 0.7):
            uf.union(audioFile, audioFile2)
    ids[audioFile] = fingerprint

print(uf.components())