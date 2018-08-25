import pyaudio
import numpy as np
import matplotlib.pyplot as plt

SAMPLING_RATE = 44100
AUDIO_FREQ = 100

chunk_size = int(SAMPLING_RATE/AUDIO_FREQ)
samples = np.sin(2*np.pi*AUDIO_FREQ/SAMPLING_RATE*np.arange(chunk_size))
samples = samples.astype(np.float32)
plt.plot(samples)
plt.show()

p = pyaudio.PyAudio()
ostream = p.open(format=pyaudio.paFloat32, channels=2, rate=SAMPLING_RATE, output=True)
for k in range(60):
	ostream.write(samples)
ostream.stop_stream()
ostream.close()
p.terminate()
