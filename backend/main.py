from Fingerprint import Fingerprint
from FingerprintComparator import FingerprintComparator
from Video import Video
from utils import displayTimestamp, seconds

clarity1full = Video("C:/Users/ethan/OneDrive/Desktop/Programming/temp/clarity1full.mp4")
clarity2 = Video("C:/Users/ethan/OneDrive/Desktop/Programming/temp/clarity2.mp4")
v9291 = Video("C:/Users/ethan/OneDrive/Desktop/Programming/temp/IMG_9291.MP4")
v9245 = Video("C:/Users/ethan/OneDrive/Desktop/Programming/temp/IMG_9245.MP4")

fp1 = Fingerprint(clarity1full.getAudioPath(), clarity1full.duration)
fp2 = Fingerprint(clarity2.getAudioPath(), clarity2.duration)

fp3 = Fingerprint(v9291.getAudioPath(), v9291.duration)
fp4 = Fingerprint(v9245.getAudioPath(), v9245.duration)


clarity1full.extractAudio()
clarity2.extractAudio()

comparator = FingerprintComparator(fp1.fingerprints, fp2.fingerprints)
comparator1 = FingerprintComparator(fp3.fingerprints, fp4.fingerprints)

crossCor = comparator.crossCorrelate()
offsetSeconds = seconds(comparator.getBestScore(crossCor))
print("Max correlation: ", max(crossCor))
print(displayTimestamp(fp2, fp1, offsetSeconds))