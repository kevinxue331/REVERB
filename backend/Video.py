from pathlib import Path
import subprocess
import json
import datetime
from cuid2 import Cuid

from Fingerprint import Fingerprint

class Video:
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileName = Path(self.filePath).name
        
        audioPath = self.filePath.replace("." + self.fileName.split('.')[-1], ".wav")
        self.__audioPath = audioPath if Path(audioPath).exists() else None
        self.fingerprint = None
        cuid2 = Cuid(length=24)
        self.id = cuid2.generate()
        self.metadata = self.extractMetadata()
        self.duration = float(self.metadata['format']['duration'])
        self.timestamp = datetime.datetime.fromisoformat(self.metadata['format']['tags']['creation_time'])
        
        
    def extractAudio(self):
        outputPath = self.filePath.replace("." + self.fileName.split('.')[-1], ".wav")
        if (Path(outputPath).exists()):
            print("Audio file already exists")
            return
            raise RuntimeError("Audio file already exists")
        try:
            subprocess.run(['ffmpeg', '-i', self.filePath, '-vn', '-hide_banner', '-loglevel', 'error', outputPath])
            self.setAudioPath(outputPath)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error splitting video to audio: {e}")
    
    def extractMetadata(self):
        try:
            command = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                self.filePath
            ]

            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return json.loads(result.stdout)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error running ffprobe: {e.stderr}")
    
    def generateFingerprint(self):
        print (self.__audioPath)
        if (self.__audioPath == None):
            raise RuntimeError("Audio has not been extracted or set")
        self.fingerprint = Fingerprint(self.__audioPath, self.duration)
            
    def outputMetadata(self, destination):
        with open(f'{destination}/{self.fileName}', 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=4)
    
    def getAudioPath(self):
        if (self.__audioPath == None):
            raise RuntimeError("Audio has not been extracted or set")
        return self.__audioPath

    def setAudioPath(self, audioPath):
        self.__audioPath = audioPath
