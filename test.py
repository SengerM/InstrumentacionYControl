"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys

CHUNK_SIZE = 1024
SAMPLING_RATE = 44.1e3

p = pyaudio.PyAudio()

stream = p.open(format=paInt16,
                channels=wave_file.getnchannels(),
                rate=wave_file.getframerate(), # Sampling rate
                output=True)
print(wave_file.getframerate())
data = wave_file.readframes(CHUNK)
while data != '':
    stream.write(data)
    data = wave_file.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()
