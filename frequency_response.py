import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
import utils.matplotlib_my_utils as mplt
# Parameters ------------------------------------
SIGNAL_FREQUENCIES = np.logspace(np.log10(100),np.log10(1000),5) # In Hertz.
# -----------------------------------------------
figs = [] # Do not touch this, ja!

def frequency_response(frequencies, amplitude=1, measuring_cycles=100, rancius_time=0.5, sampling_frequency=48000):
	# Validations -----------------------------------
	if not isinstance(sampling_frequency, int):
		raise ValueError('sampling_frequency must be an integer number!')
	if amplitude > 1:
		raise ValueError('AMPLITUDE must be less than 1 because the output samples must lie between +-1')
	# Create the signal -----------------------------
	amplitudes = [None]*len(frequencies)
	for k in range(len(frequencies)):
		samples = np.sin(2*np.pi*np.arange(sampling_frequency/frequencies[k]*(rancius_time*frequencies[k] + measuring_cycles))*frequencies[k]/sampling_frequency)
		# Set the appropiate amplitude and offset -------
		samples -= np.min(samples)
		samples /= np.max(samples)
		samples -= 0.5
		samples *= 2*amplitude
		samples = samples.astype(np.float32)
		# Play and record samples -----------------------
		recorded_samples = sd.playrec(samples, sampling_frequency, channels=1)
		time.sleep(len(samples)/sampling_frequency)
		samples = samples[np.round(sampling_frequency*rancius_time):] # Discard rancius samples.
		amplitudes[k] = 2*np.sum(samples**2)/len(samples)
	return amplitudes

amplitudes = frequency_response(SIGNAL_FREQUENCIES)

# PLOT ------------------------------------------
f, axes = plt.subplots(1, sharex=True, figsize=(mplt.fig_width*mplt.fig_ratio[0]/25.4e-3, mplt.fig_width*mplt.fig_ratio[1]/25.4e-3)) # Create the figure for plotting.
f.subplots_adjust(hspace=0.3) # Fine-tune figure; make subplots close to each other and hide x ticks for all but bottom plot.
figs.append(f)
axes.plot(SIGNAL_FREQUENCIES, amplitudes, color=mplt.colors[1], marker='.')
mplt.beauty_grid(axes)
axes.set_ylabel('Amplitude')
axes.set_xscale('log')
axes.set_xlabel('Frequency (Hz)')
# Save figures -----------------------------------
for k in range(len(figs)):
	figs[k].savefig(str(k+1) + '.' + mplt.image_format, bbox_inches='tight', dpi=mplt.dpi_rasterization)

plt.show()
