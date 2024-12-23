import subprocess
from pathlib import Path

class Fingerprint:
    def __init__(self, filePath: str, length: int=30):
        self.filePath = filePath
        self.name = Path(filePath).name
        self.length = length
        self.fingerprints = self.__generateFingerprints(self.filePath, self.length)
    
    def __generateFingerprints(self, filePath: str, length: int=30)->list:
        """
        Generates fingerprints of an audio file using the fpcalc command line tool

        Parameters:
            filePath (str)  path to audio file 
            length (int, optional) length of the audio file to fingerprint

        Returns:
            array (32bit ints): list of fingerprints of the audio file
        """
        rawOutput = subprocess.getoutput('fpcalc -raw -rate 11025 -length %i %s' % (length, filePath)) # gives a string with duration and fingerprint
        fingerprint_index = rawOutput.find('FINGERPRINT=') + 12 # to skip to the actual fingerprint
        fingerprints = list(map(int, rawOutput[fingerprint_index:].split(','))) # converts the string to a list of integers starting from the index
        return fingerprints