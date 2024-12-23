from pathlib import Path
import subprocess

class AudioFile:
    def __init__(self, filePath):
        self.filePath = filePath
        self.videoPath = None
        self.name = Path(filePath).name
        
