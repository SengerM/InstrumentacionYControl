import pyaudio
import wave
import sys
import numpy as np

CHUNK_SIZE = 1024
SAMPLING_RATE = 44100
AUDIO_FREQ = 1e3

samples = np.sin(2*np.pi*AUDIO_FREQ/SAMPLING_RATE*range(CHUNK_SIZE))
samples = samples.astype(pyaudio.paInt16)

p = pyaudio.PyAudio()

ostream = p.open(format=pyaudio.paInt16, channels=2, rate=SAMPLING_RATE, output=True)

while True:
	ostream.write(samples)
# data = wave_file.readframes(CHUNK)
# while data != '':
    # ostream.write(data)
    # data = wave_file.readframes(CHUNK)

ostream.stop_ostream()
ostream.close()

p.terminate()
