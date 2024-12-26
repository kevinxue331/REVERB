import numpy
from utils import hashes
import statistics

class FingerprintComparator:
    MIN_OVERLAP = 20 # 7 offsets is 1 second
    STEP = 1  # checking every 0.14 seconds for correlation basically
    SIMILARITY_THRESHOLD = 0.7

    def __init__(self, fps1, fps2):
        """
        fps1 (array): array of 32 bit integers representing the fingerprints of longer audio file
        fps2 (array): array of 32 bit integers representing the fingerprints of the shorter audiofile
        MIN_OVERLAP (int): minimum overlap between two fingerprints to compare
        STEP (int): step size across span to check correlation
        span (int): span of the offsets to check correlation at
        """
        
        if (len(fps1) > len(fps2)):
            self.fps1 = fps1  # longer fingerprint
            self.fps2 = fps2 # shorter fingerprint
        else:
            self.fps2 = fps1
            self.fps1 = fps2
        self.span = len(self.fps2) - self.MIN_OVERLAP

    def correlate(self, list1=None, list2=None):
        """
        Correlates two audio files by comparing their fingerprints and returns similarity
        
        Parameters:
            list1 (array): array of 32 bit integers representing the fingerprints of the first audio file
            list2 (array): array of 32 bit integers representing the fingerprints of the first second file

        Returns:
            float: correlation of two files -> Max value is 1.0, Min value is 0.0
            note: realistically no two audio files will have a correlation of 1.0 or 0.0, anything above a 0.55 is a decent match

        Might be better to merge with offsetCorrelate()
        """        
        
        if (list1 == None and list2 == None):
            list1 = self.fps1
            list2 = self.fps2

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
        overlapFps1 = self.fps1
        overlapFps2 = self.fps2
         
        
        if (offset > 0):
            overlapFps1 = self.fps1[offset:] # 2-10 (example offset of 2, y is 2 ahead of x)
            overlapFps2 = self.fps2[:len(self.fps1)] # 0-8
        elif (offset < 0):
            offset = -offset
            overlapFps2 = self.fps2[offset:] # 2-10 (example offset of -2, y is 2 behind of x (or x is 2 ahead of y))
            overlapFps1 = self.fps1[:len(self.fps2)] # 0-8
            
        if (min(len(overlapFps1), len(overlapFps2)) < self.MIN_OVERLAP):
            print (f"Overlap is {min(len(overlapFps1), len(overlapFps2))} for offset {offset}")
            print(len(self.fps1))
            print(len(self.fps2))
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
        if (self.span > min(len(self.fps1), len(self.fps2))):
            raise Exception(f"Span is greater than the length of the shorter fingerprint. Shortest fingerprint is {min(len(self.fps1), len(self.fps2))}")
        crossCor = []
        upper = max(len(self.fps1), len(self.fps2))-self.MIN_OVERLAP
        for offset in  numpy.arange(-self.span, upper, self.STEP):
            crossCor.append(self.offsetCorrelate(offset))
        return crossCor
     
    def getBestOffset(self, crossCor):
        """
        Returns the best offset from a cross correlation array
        
        Parameters:
            crossCor (array): list of correlations at each offset
            
        Returns:
            int: max corrleation offset
        """
        maxCor = max(crossCor)
        maxIndex = crossCor.index(maxCor)
        return -self.span + maxIndex * self.STEP
    

    def getBestScore(self, crossCor):
        score = max(crossCor)
        scoreIndex = crossCor.index(score)
        
        # https://github.com/unmade/audiomatch/blob/master/src/audiomatch/fingerprints.py
        # useful methods for filtering out false positives
        # if (min(len(self.fps1), len(self.fps2)) > hashes(6)):
        if min(len(self.fps1), len(self.fps2)) < hashes(20):
            score *= 0.97
        
        sampleSpan = 5
        samples = crossCor[scoreIndex - sampleSpan : scoreIndex] + crossCor[scoreIndex + 1 : scoreIndex + sampleSpan + 1]
        if score-statistics.median(samples) > 0.04:
            return score
        return 0.0
        
            
        
    

