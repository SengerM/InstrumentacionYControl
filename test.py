"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys

CHUNK_SIZE = 1024
SAMPLING_RATE = 44100

p = pyaudio.PyAudio()

ostream = p.open(format=pyaudio.paInt16, channels=2, rate=SAMPLING_RATE, output=True)

# data = wave_file.readframes(CHUNK)
# while data != '':
    # ostream.write(data)
    # data = wave_file.readframes(CHUNK)

ostream.stop_ostream()
ostream.close()

p.terminate()
