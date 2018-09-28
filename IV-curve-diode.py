import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
import utils.matplotlib_my_utils as mplt
import utils.timestamp as tmstmp
import os
os.system('clear')
# Parameters ------------------------------------
AMPLITUDE = -1 # Amplitude of the signal between 0 and 1.
SIGNAL_FREQUENCY = 100 # In Hertz.
SIGNAL = 'sin' # 'sin', 'ramp', 'squ'
N_CYCLES = 100 # This must be "a great number" to overcome a strange transitory of the sound card...
SAMPLING_FREQUENCY = 48000 # Must be integer.
RANCIUS_CYCLES = N_CYCLES - 10
CALIBRATION_FACTOR = 1.22*np.sqrt(2)/0.8 # Volt/unidades de placa de sonido
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
sd.wait() #it waits and returns as the recording is finished.
recorded_samples = np.transpose(recorded_samples)
new_samples = [None]*2
new_samples[0] = recorded_samples[0][int(RANCIUS_CYCLES*SAMPLING_FREQUENCY/SIGNAL_FREQUENCY):]
new_samples[1] = recorded_samples[1][int(RANCIUS_CYCLES*SAMPLING_FREQUENCY/SIGNAL_FREQUENCY):]
new_time = np.linspace(0,N_CYCLES/SIGNAL_FREQUENCY,len(new_samples[0]))
# PLOT ------------------------------------------
f, axes = plt.subplots(3, sharex=True, figsize=(mplt.fig_width*mplt.fig_ratio[0]/25.4e-3, mplt.fig_width*mplt.fig_ratio[1]/25.4e-3)) # Create the figure for plotting.
f.subplots_adjust(hspace=0.3) # Fine-tune figure; make subplots close to each other and hide x ticks for all but bottom plot.
figs.append(f)
axes[0].plot(new_time, output_samples[-len(new_time):], color=mplt.colors[0], label='Output signal')
axes[1].plot(new_time, new_samples[0], color=mplt.colors[1], label='Recorded signal[0]')
axes[2].plot(new_time, new_samples[1], color=mplt.colors[2], label='Recorded signal[1]')
for k in range(len(axes)):
	mplt.beauty_grid(axes[k])
	axes[k].set_ylabel('Amplitude')
	axes[k].legend()
	axes[k].set_ylim(-1.05,1.05)
axes[-1].set_xlabel('Time (s)')
# PLOT ------------------------------------------
f, axes = plt.subplots(1, sharex=True, figsize=(mplt.fig_width*mplt.fig_ratio[0]/25.4e-3, mplt.fig_width*mplt.fig_ratio[1]/25.4e-3)) # Create the figure for plotting.
f.subplots_adjust(hspace=0.3) # Fine-tune figure; make subplots close to each other and hide x ticks for all but bottom plot.
figs.append(f)
axes.plot(new_samples[0]-new_samples[1], new_samples[1], color=mplt.colors[0])
mplt.beauty_grid(axes)
axes.set_ylabel('Corriente')
axes.set_xlabel('Tension')
# Save figures -----------------------------------
for k in range(len(figs)):
	figs[k].savefig(timestamp + '_' + str(k+1) + '.' + mplt.image_format, bbox_inches='tight', dpi=mplt.dpi_rasterization)
with open(timestamp + '.txt', 'a') as ofile:
	print('Time (s)\tCH1 (V)\tCH2 (V)', file=ofile) # Print header.
	for k in range(len(new_time)):
		print(str(new_time[k]) + '\t' + str(new_samples[0][k]) + '\t' + str(new_samples[1][k]), file=ofile)

plt.show()
