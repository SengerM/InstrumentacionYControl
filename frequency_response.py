import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
import utils.matplotlib_my_utils as mplt
# Parameters ------------------------------------
AMPLITUDE = .5 # Amplitude of the signal between 0 and 1.
SIGNAL_FREQUENCY = [100, 1000] # In Hertz.
RANCIUS_TRANSITORY = 
SAMPLING_FREQUENCY = 48000 # Must be integer.
# -----------------------------------------------
figs = [] # Do not touch this, ja!
# Validations -----------------------------------
if not isinstance(SAMPLING_FREQUENCY, int):
	raise ValueError('SAMPLING_FRECUENCY must be an integer number!')
if AMPLITUDE > 1:
	raise ValueError('AMPLITUDE must be less than 1 because the output samples must lie between +-1')
# Create the signal -----------------------------
if SIGNAL == 'sin':
	samples = np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)
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
sd.default.samplerate = SAMPLING_FREQUENCY
sd.default.channels = 1
recorded_samples = sd.playrec(output_samples, SAMPLING_FREQUENCY)
time.sleep(N_CYCLES/SIGNAL_FREQUENCY)
# PLOT ------------------------------------------
f, axes = plt.subplots(2, sharex=True, figsize=(mplt.fig_width*mplt.fig_ratio[0]/25.4e-3, mplt.fig_width*mplt.fig_ratio[1]/25.4e-3)) # Create the figure for plotting.
f.subplots_adjust(hspace=0.3) # Fine-tune figure; make subplots close to each other and hide x ticks for all but bottom plot.
figs.append(f)
axes[1].plot(np.linspace(0,N_CYCLES/SIGNAL_FREQUENCY,len(output_samples)), recorded_samples, color=mplt.colors[0], label='Recorded signal')
axes[0].plot(np.linspace(0,N_CYCLES/SIGNAL_FREQUENCY,len(output_samples)), output_samples, color=mplt.colors[1], label='Output signal')
for k in range(len(axes)):
	mplt.beauty_grid(axes[k])
	axes[k].set_ylabel('Amplitude')
	axes[k].legend()
axes[-1].set_xlabel('Time (s)')
axes[0].set_ylim(-1.05,1.05)
# Save figures -----------------------------------
for k in range(len(figs)):
	figs[k].savefig(str(k+1) + '.' + mplt.image_format, bbox_inches='tight', dpi=mplt.dpi_rasterization)

plt.show()
