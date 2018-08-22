import pyaudio
import wave
import sys
import numpy as np
import matplotlib.pyplot as plt

SAMPLING_RATE = 44100
AUDIO_FREQ = 2000

samples = np.sin(2*np.pi*AUDIO_FREQ/SAMPLING_RATE*np.array(range(int(np.floor(SAMPLING_RATE/AUDIO_FREQ)))))
samples = samples.astype(np.float32)

plt.plot(samples)
plt.show()

p = pyaudio.PyAudio()

ostream = p.open(format=pyaudio.paFloat32, channels=2, rate=SAMPLING_RATE, output=True)

while True:
	ostream.write(samples)

ostream.stop_ostream()
ostream.close()

p.terminate()
