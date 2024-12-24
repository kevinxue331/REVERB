import subprocess
import json
from pathlib import Path

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

def displayTimestamp(fps1, fps2, offsetSeconds):
    if (offsetSeconds > 0):
        return f"{fps2.name} occurs at {formatSeconds(offsetSeconds)} in {fps1.name}"
    elif (offsetSeconds < 0):
        return f"{fps1.name} occurs at {formatSeconds(-offsetSeconds)} in {fps2.name}"
    else:
        return "The two files are aligned"