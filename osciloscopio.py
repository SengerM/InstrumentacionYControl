import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.signal as signal

# Parameters ------------------------------------
AMPLITUDE = 1.0 # Amplitude of the signal between 0 and 1.
SIGNAL_FREQUENCY = 1000 # In Hertz.
SIGNAL = 'ramp' # 'sin', 'ramp'
N_CYCLES = 10 # This must be "a great number" to overcome a strange transitory of the sound card...
SAMPLING_FREQUENCY = 48000 # Must be integer.
# -----------------------------------------------
if not isinstance(SAMPLING_FREQUENCY, int):
	raise ValueError('ERROR: SAMPLING_FRECUENCY must be an integer number!')

sd.default.samplerate = SIGNAL_FREQUENCY
sd.default.channels = 1

if SIGNAL == 'sin':
	samples = np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)
elif SIGNAL == 'ramp':
	samples = np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)
# Set the appropiate amplitude ---
samples -= np.min(samples)
samples /= np.max(samples)
samples -= 0.5
samples *= AMPLITUDE
samples = samples.astype(np.float32)
output_samples = samples
# Create the output samples -----
for k in range(N_CYCLES-1):
	output_samples = np.append(output_samples, samples)
# Play samples ------------------
sd.play(output_samples, SAMPLING_FREQUENCY)
time.sleep(N_CYCLES/SIGNAL_FREQUENCY)
