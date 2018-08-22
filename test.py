import pyaudio
import wave
import sys
import numpy as np
import matplotlib.pyplot as plt

CHUNK_SIZE = 1024
SAMPLING_RATE = 44100
AUDIO_FREQ = 1000

samples = np.sin(2*np.pi*AUDIO_FREQ/SAMPLING_RATE*np.array(range(CHUNK_SIZE)))
samples = samples.astype(np.float32)

plt.plot(samples)

p = pyaudio.PyAudio()

ostream = p.open(format=pyaudio.paFloat32, channels=2, rate=SAMPLING_RATE, output=True)

while True:
	ostream.write(samples)

ostream.stop_ostream()
ostream.close()

p.terminate()
