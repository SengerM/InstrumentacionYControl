import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib_my_utils as mplt
import utils.timestamp as tmstmp
import os
os.system('cls')
# Parameters ------------------------------------
AMPLITUDE = 1 # Amplitude of the signal between 0 and 1.
SIGNAL_FREQUENCY = 100 # In Hertz.
SIGNAL = 'sin' # 'sin', 'ramp', 'squ'
N_CYCLES = 500 # This must be "a great number" to overcome a strange transitory of the sound card...
SAMPLING_FREQUENCY = 48000 # Must be integer.
rancius_time=0.5 #time for start rec
# -----------------------------------------------
timestamp = tmstmp.get()
figs = [] # Do not touch this, ja!
available_signals = ['sin','ramp','squ']
# Validations -----------------------------------
if not isinstance(SAMPLING_FREQUENCY, int):
	raise ValueError('SAMPLING_FRECUENCY must be an integer number!')
if AMPLITUDE > 1:
	raise ValueError('AMPLITUDE must be less than 1 because the output samples must lie between +-1')
if available_signals.count(SIGNAL) == 0:
	raise ValueError('Invalid type of signal. Parameter "SIGNAL" must be one of the following ' + str(available_signals))
# Create the signal -----------------------------
if SIGNAL == 'sin':
	samples = np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)
elif SIGNAL == 'ramp':
	samples = np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)
elif SIGNAL == 'squ':
	samples = np.linspace(1,1,int((SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)/2))
	samples = np.append(samples,np.linspace(0,0,int((SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)/2)))
# Set the appropiate amplitude and offset -------
samples -= np.min(samples)
samples /= np.max(samples)
samples -= 0.5
samples *= 2*AMPLITUDE
samples = samples.astype(np.float32)
# Create the output samples ---------------------
output_samples = samples
for k in range(N_CYCLES-1):
	output_samples = np.append(output_samples, samples)
# Play and record samples -----------------------
recorded_samples = sd.playrec(output_samples, SAMPLING_FREQUENCY, channels=2)
time.sleep(N_CYCLES/SIGNAL_FREQUENCY)
recorded_samples = np.transpose(recorded_samples)
samples = [None]*2
samples[0] = recorded_samples[0][int(rancius_time*SAMPLING_FREQUENCY):]
samples[1] = recorded_samples[1][int(rancius_time*SAMPLING_FREQUENCY):]
# PLOT ------------------------------------------
f, axes = plt.subplots(1, sharex=True, figsize=(mplt.fig_width*mplt.fig_ratio[0]/25.4e-3, mplt.fig_width*mplt.fig_ratio[1]/25.4e-3)) # Create the figure for plotting.
f.subplots_adjust(hspace=0.3) # Fine-tune figure; make subplots close to each other and hide x ticks for all but bottom plot.
figs.append(f)
axes.plot(samples[0], samples[1] - samples[0], color=mplt.colors[0])
mplt.beauty_grid(axes)
axes.set_ylabel('Current')
axes.set_xlabel('Voltage')
# Save figures -----------------------------------
for k in range(len(figs)):
	figs[k].savefig(timestamp + '_' + str(k+1) + '.' + mplt.image_format, bbox_inches='tight', dpi=mplt.dpi_rasterization)

plt.show()