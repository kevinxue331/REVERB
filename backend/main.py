from Fingerprint import Fingerprint
from FingerprintComparator import FingerprintComparator
from Video import Video
from utils import displayTimestamp, seconds

clarity1full = Video("C:/Users/ethan/OneDrive/Desktop/Programming/temp/clarity1full.mp4")
clarity2 = Video("C:/Users/ethan/OneDrive/Desktop/Programming/temp/clarity2.mp4")
v9291 = Video("C:/Users/ethan/OneDrive/Desktop/Programming/temp/IMG_9291.MP4")


fp1 = Fingerprint(clarity1full.getAudioPath(), clarity1full.duration)
fp2 = Fingerprint(clarity2.getAudioPath(), clarity2.duration)



# clarity1full.extractAudio()
# clarity2.extractAudio()

comparator = FingerprintComparator(fp1.fingerprints, fp2.fingerprints)

crossCor = comparator.crossCorrelate()
offsetSeconds = seconds(comparator.getBestOffset(crossCor))
print(displayTimestamp(fp2, fp1, offsetSeconds))