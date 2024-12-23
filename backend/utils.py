import subprocess
import json
from pathlib import Path
from AudioFile import AudioFile

def offsets(seconds):
    return round(seconds*7.0)

# no idea how well this works but looks good for the one tesst i did
def seconds(hashes):
    # frame size from https://oxygene.sk/2011/01/how-does-chromaprint-work/
    hashesPerSecond = (4096.0 / 3) / 11025.0  # ~0.1238 seconds per fingerprint
    return hashes * hashesPerSecond

def formatSeconds(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f"{minutes:02}:{seconds:02}.{milliseconds:03}"

#might be better to make a video class i'm not sure
def processVideo(filePath):
    audioPath = filePath.replace(".mp4", ".wav")
    name = Path(audioPath).name.replace(".wav", ".json")
    try:
        subprocess.run(['ffmpeg', '-i', filePath, '-vn', audioPath,]) # split
    except:
        print("Error splitting video to audio")
        return None

    try:
        command = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            filePath
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        f = open(f'./media/json/{name}', 'w')
        f.write(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e.stderr}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
