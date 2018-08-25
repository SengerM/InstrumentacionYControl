"""PyAudio Example: Play a WAVE file."""

import pyaudio
import numpy as np
import matplotlib.pyplot as plt

p = pyaudio.PyAudio()

volume = 0.5     # rango en que se mueve [0.0, 1.0]
fs = 44100       # sampling rate, Hz, debe ser entero
duration = 10   # en segundos, debe ser float
f = 100.0  
chunk=1024

# generate samples, note conversion to float32 array
data = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=fs,
                output=True,
                input=True,
                frames_per_buffer = chunk)

stream.write(volume*data)

#esto graba
for i in range(0, 44100 / chunk * duration):
    grabacion = stream.read(chunk)

plt.plot(np.linspace(0,duration,len(grabacion)),grabacion)


stream.stop_stream()
stream.close()

p.terminate()

