import subprocess

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

def correlate(fingerprints1, fingerprints2):
    """
    Correlates two audio files by comparing their fingerprints and returns similarity
    
    Parameters:
        fingerprints1 (array): array of 32 bit integers representing the fingerprints of the first audio file
        fingerprints2 (array): array of 32 bit integers representing the fingerprints of the first second file

    Returns:
       float: correlation of two files -> Max value is 1.0, Min value is 0.0
       note: realistically no two audio files will have a correlation of 1.0 or 0.0, anything above a 0.55 is a decent match

    """
    variance = 0.0 # the number of bits that are the same, lowkey a confusing name can rename later
    for fp1, fp2 in zip(fingerprints1, fingerprints2): # zip uses smaller fingerprint
        variance += 32-bin((fp1^fp2)).count('1')
        # compares each 32 bit int in each fingerprint by xoring and counting the number of bits that are 1
        # this counts the number of bits that are different between the two files, subtracts it by 32 to get the number of same bits
    variance /= float(min(len(fingerprints1), len(fingerprints2)))
    return variance/32 # returns the percentage of similar bits, # of same bits / # of total bits (32 * length of shorter fingerprint)

clarity1 = generateFingerprints("./media/clarity1.wav")
clarity2 = generateFingerprints("./media/clarity2.wav")
clarity1trim = generateFingerprints("./media/clarity1trim.wav")
clarity2trim = generateFingerprints("./media/clarity2trim.wav")
stay = generateFingerprints("./media/stay.wav")
lebron = generateFingerprints("./media/lebron.wav")

print("Comparisons:")
print("Same song, different recordings, not aligned")
print(correlate(clarity1, clarity2))
print("Same song, different recordings, aligned")
print(correlate(clarity1trim, clarity2trim))
print("Same songs")
print(correlate(clarity1, clarity1))
print("Different songs") 
print(correlate(clarity1, stay))
print(correlate(clarity2, stay))   
print("Lebron James")
print(correlate(lebron, clarity1))
print(correlate(lebron, clarity2))
print(correlate(lebron, stay))
