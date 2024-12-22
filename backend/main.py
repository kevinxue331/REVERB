import subprocess
import numpy

MIN_OVERLAP = 20 # 7 offsets is 1 second
STEP = 1  # checking every 0.14 seconds for correlation basically

def generateFingerprints(filePath: str, length: int=30)->list:
    """
    Generates fingerprints of an audio file using the fpcalc command line tool

    Parameters:
        filePath (str)  path to audio file 
        length (int, optional) length of the audio file to fingerprint

    Returns:
        array (32bit ints): list of fingerprints of the audio file
    """
    rawOutput = subprocess.getoutput('fpcalc -raw -length %i %s' % (length, filePath)) # gives a string with duration and fingerprint
    fingerprint_index = rawOutput.find('FINGERPRINT=') + 12 # to skip to the actual fingerprint
    fingerprints = list(map(int, rawOutput[fingerprint_index:].split(','))) # converts the string to a list of integers starting from the index
    return fingerprints

def correlate(fps1, fps2):
    """
    Correlates two audio files by comparing their fingerprints and returns similarity
    
    Parameters:
        fps1 (array): array of 32 bit integers representing the fingerprints of the first audio file
        fps2 (array): array of 32 bit integers representing the fingerprints of the first second file

    Returns:
       float: correlation of two files -> Max value is 1.0, Min value is 0.0
       note: realistically no two audio files will have a correlation of 1.0 or 0.0, anything above a 0.55 is a decent match

    """
    variance = 0.0 # the number of bits that are the same, lowkey a confusing name can rename later
    for fp1, fp2 in zip(fps1, fps2): # zip uses smaller fingerprint
        variance += 32-bin((fp1^fp2)).count('1')
        # compares each 32 bit int in each fingerprint by xoring and counting the number of bits that are 1
        # this counts the number of bits that are different between the two files, subtracts it by 32 to get the number of same bits
    variance /= float(min(len(fps1), len(fps2)))
    return variance/32 # returns the percentage of similar bits, # of same bits / # of total bits (32 * length of shorter fingerprint)

def offsetCorrelate(fps1, fps2, offset):
    """
    Generates a correlation between two audio files by comparing their fingerprints with an offset

    Parameters:
        fps1 (array): array of 32 bit integers representing the fingerprints of the first audio file
        fps2 (array): array of 32 bit integers representing the fingerprints of the first second file
        offset (int): offset to compare the two fingerprints at. Offsets fps2 the amount from fps1

    Returns:
       float: correlation of two files -> Max value is 1.0, Min value is 0.0
       note: same return as correlate()
    """
    # offsetting y in front or behind of x and truncating so same size
    if (offset > 0):
        fps1 = fps1[offset:] # 2-10 (example offset of 2, y is 2 ahead of x)
        fps2 = fps2[:len(fps1)] # 0-8
    elif (offset < 0):
        offset = -offset
        fps2 = fps2[offset:] # 2-10 (example offset of -2, y is 2 behind of x (or x is 2 ahead of y))
        fps1 = fps1[:len(fps2)] # 0-8
    if (min(len(fps1), len(fps2)) < MIN_OVERLAP):
        raise Exception("Not enough overlap between two fingerprints to compare")
    return correlate(fps1, fps2)

def crossCorrelate(fps1, fps2, step):
    """
    Cross correlates two audio files by comparing their fingerprints at different offsets across a span. 

    Parameters:
        fps1 (array): array of 32 bit integers representing the fingerprints of the first audio file
        fps2 (array): array of 32 bit integers representing the fingerprints of the first second file
        step (int): step size across span to check correlation at

    Returns:
       array (floats): list of correlations at each offset
    """

    # TO DO - use stats to reduce false positives

    span = min(len(fps1), len(fps2)) - MIN_OVERLAP
    if (span > min(len(fps1), len(fps2))):
        raise Exception(f"Span is greater than the length of the shorter fingerprint. Shortest fingerprint is {min(len(fps1), len(fps2))}")
    crossCor = []
    for offset in  numpy.arange(-span, span+1, step):
        crossCor.append(offsetCorrelate(fps1, fps2, offset))
    return crossCor

def generateTimestamp(fps1, fps2, crossCor):
    """
    Generates a timestamp of when the second audio file starts in relation to the first audio file

    Parameters:
        fps1 (array): array of 32 bit integers representing the fingerprints of the first audio file
        fps2 (array): array of 32 bit integers representing the fingerprints of the first second file
        crossCor (array): array of floats representing the correlation at each offset

    Returns:
       float: how many seconds the second audio file is behind/ahead relative to the first audio file (negative means behind)
    """
    maxCor = max(crossCor)
    maxIndex = crossCor.index(maxCor)
    span = min(len(fps1), len(fps2)) - MIN_OVERLAP
    offset = -span + maxIndex
    return seconds(offset)


# helper functions offsets->seconds and seconds->offsets
def offsets(seconds):
    return round(seconds*7.0)

def seconds(offset):
    return offset/7.0
    

# TEST CASES

clarity1 = generateFingerprints("./media/clarity1.wav")
clarity2 = generateFingerprints("./media/clarity2.wav")
clarity1trim = generateFingerprints("./media/clarity1trim.wav")
clarity2trim = generateFingerprints("./media/clarity2trim.wav")
stay = generateFingerprints("./media/stay.wav")
lebron = generateFingerprints("./media/lebron.wav")

crossCor = crossCorrelate(clarity1, clarity2, STEP)

# Benchmarks

print("Comparisons:")
print("\n")
print("Same song, different recordings, not aligned")
print(correlate(clarity1, clarity2))
print("\n")
print("Same song, different recordings, manually aligned")
print(correlate(clarity1trim, clarity2trim))
print("\n")
print("Same song, different recordings, cross correlation aligned")
print(max(crossCorrelate(clarity1, clarity2, STEP)))
print(f"clarity2 is {generateTimestamp(clarity1, clarity2, crossCor)} seconds away from clarity1")
print("\n")
print("Same songs")
print(correlate(clarity1, clarity1))
print("\n")
print("Different songs") 
print(correlate(clarity1, stay))
print(correlate(clarity2, stay))   
print("\n")
print("Lebron James")
print(correlate(lebron, clarity1))
print(correlate(lebron, clarity2))
print(correlate(lebron, stay))
