import numpy
from utils import seconds, formatSeconds

class FingerprintComparator:
    MIN_OVERLAP = 20 # 7 offsets is 1 second
    STEP = 1  # checking every 0.14 seconds for correlation basically

    def __init__(self, fps1, fps2):
        """
        fps1 (array): array of 32 bit integers representing the fingerprints of the first audio file
        fps2 (array): array of 32 bit integers representing the fingerprints of the first second file
        MIN_OVERLAP (int): minimum overlap between two fingerprints to compare
        STEP (int): step size across span to check correlation
        span (int): span of the offsets to check correlation at
        """

        self.fps1 = max(fps1, fps2, key=lambda x: len(x.fingerprints)) # longer fingerprint
        self.fps2 = min(fps1, fps2, key=lambda x: len(x.fingerprints)) # shorter fingerprint
        self.span = min(len(self.fps1.fingerprints), len(self.fps2.fingerprints)) - self.MIN_OVERLAP

    def correlate(self, list1=None, list2=None):
        if (list1 == None and list2 == None):
            list1 = self.fps1.fingerprints
            list2 = self.fps2.fingerprints

        """
        Correlates two audio files by comparing their fingerprints and returns similarity
        
        Parameters:
            list1 (array): array of 32 bit integers representing the fingerprints of the first audio file
            list2 (array): array of 32 bit integers representing the fingerprints of the first second file

        Returns:
            float: correlation of two files -> Max value is 1.0, Min value is 0.0
            note: realistically no two audio files will have a correlation of 1.0 or 0.0, anything above a 0.55 is a decent match

        To Do:
            Merge with offsetCorrelate
        """
        variance = 0.0 # the number of bits that are the same, lowkey a confusing name can rename later
        for fp1, fp2 in zip(list1, list2): # zip uses smaller fingerprint
            variance += 32-bin((fp1^fp2)).count('1')
            # compares each 32 bit int in each fingerprint by xoring and counting the number of bits that are 1
            # this counts the number of bits that are different between the two files, subtracts it by 32 to get the number of same bits
        variance /= float(min(len(list1), len(list2)))
        return variance/32 # returns the percentage of similar bits, # of same bits / # of total bits (32 * length of shorter fingerprint)

    def offsetCorrelate(self, offset):
        """
        Generates a correlation between two audio files by comparing their fingerprints with an offset

        Parameters:
            offset (int): offset to compare the two fingerprints at. Offsets fps2 the amount from fps1

        Returns:
        float: correlation of two files -> Max value is 1.0, Min value is 0.0
        note: same return as correlate()
        """
        # offsetting y in front or behind of x and truncating so same size
        overlapFps1 = self.fps1.fingerprints
        overlapFps2 = self.fps2.fingerprints

        if (offset > 0):
            overlapFps1 = self.fps1.fingerprints[offset:] # 2-10 (example offset of 2, y is 2 ahead of x)
            overlapFps2 = self.fps2.fingerprints[:len(self.fps1.fingerprints)] # 0-8
        elif (offset < 0):
            offset = -offset
            overlapFps2 = self.fps2.fingerprints[offset:] # 2-10 (example offset of -2, y is 2 behind of x (or x is 2 ahead of y))
            overlapFps1 = self.fps1.fingerprints[:len(self.fps2.fingerprints)] # 0-8
        if (min(len(overlapFps1), len(overlapFps2)) < self.MIN_OVERLAP):
            raise Exception("Not enough overlap between two fingerprints to compare")
        return self.correlate(overlapFps1, overlapFps2)

    def crossCorrelate(self):
        """ 
        Cross correlates two audio files by comparing their fingerprints at different offsets across a span. 

        Parameters:
            None

        Returns:
            array (floats): list of correlations at each offset
        """

        # TO DO - use stats to reduce false positives
        if (self.span > min(len(self.fps1.fingerprints), len(self.fps2.fingerprints))):
            raise Exception(f"Span is greater than the length of the shorter fingerprint. Shortest fingerprint is {min(len(self.fps1.fingerprints), len(self.fps2.fingerprints))}")
        crossCor = []
        upper = max(len(self.fps1.fingerprints), len(self.fps2.fingerprints))-self.MIN_OVERLAP
        for offset in  numpy.arange(-self.span, upper, self.STEP):
            crossCor.append(self.offsetCorrelate(offset))
        return crossCor
     
    def offsetToSeconds(self, crossCor):
        maxCor = max(crossCor)
        maxIndex = crossCor.index(maxCor)
        offset = -self.span + maxIndex * self.STEP

        return seconds(offset)
    
    def displayTimestamp(self, offsetSeconds):
        if (offsetSeconds > 0):
            return f"{self.fps2.name} occurs at {formatSeconds(offsetSeconds)} in {self.fps1.name}"
        elif (offsetSeconds < 0):
            return f"{self.fps1.name} occurs at {formatSeconds(-offsetSeconds)} before {self.fps2.name}"
        else:
            return "The two files are aligned"
