from pathlib import Path
import subprocess
import json

class Video:
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileName = Path(self.filePath).name
        self.__audioPath = None
        self.metadata = None
        
    def extractAudio(self):
        outputPath = self.filePath.replace(self.fileName.split('.')[-1], ".wav")
        if (Path(outputPath).exists()):
            raise RuntimeError("Audio file already exists")
        try:
            subprocess.run(['ffmpeg', '-i', self.filePath, '-vn', outputPath,]) # split
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
            self.metadata = json.loads(result.stdout)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error running ffprobe: {e.stderr}")
    
    def outputMetadata(self, destination):
        with open(f'{destination}/{self.fileName}', 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=4)
    
    def getAudioPath(self):
        if (self.__audioPath == None):
            raise RuntimeError("Audio has not been extracted or set")
        return self.__audioPath

    def setAudioPath(self, audioPath):
        self.__audioPath = audioPath
