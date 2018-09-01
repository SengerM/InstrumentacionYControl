import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.signal as signal
import matplotlib_my_utils as mplt

# Parameters ------------------------------------
AMPLITUDE = 1.0 # Amplitude of the signal between 0 and 1.
SIGNAL_FREQUENCY = 800 # In Hertz.
SIGNAL = 'sin' # 'sin', 'ramp'
N_CYCLES = 1600 # This must be "a great number" to overcome a strange transitory of the sound card...
SAMPLING_FREQUENCY = 48000 # Must be integer.
# -----------------------------------------------
figs = [] # Do not touch this.
if not isinstance(SAMPLING_FREQUENCY, int):
	raise ValueError('ERROR: SAMPLING_FRECUENCY must be an integer number!')

sd.default.samplerate = SIGNAL_FREQUENCY
sd.default.channels = 1

if SIGNAL == 'sin':
    samples = np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)
# Set the appropiate amplitude ---
    samples -= np.min(samples)
    samples /= np.max(samples)
    samples -= 0.5
    samples *= 2*AMPLITUDE
    samples = samples.astype(np.float32)
    output_samples = samples
elif SIGNAL == 'ramp':
    samples = np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)
    # Set the appropiate amplitude ---
    samples -= np.min(samples)
    samples /= np.max(samples)
    samples -= 0.5
    samples *= 2*AMPLITUDE
    samples = samples.astype(np.float32)
    output_samples = samples

elif SIGNAL == 'rectangular':
    up=1   #coefficient between -1 and 1.
    down=0 #coefficient between -1 and 1.
    samples = np.linspace(up,up,int((SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)/2))
    samples = np.append(samples,np.linspace(down,down,int((SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)/2)))
    samples /= np.max(samples)-np.min(samples)
    samples *= AMPLITUDE
    samples = samples.astype(np.float32)
    output_samples = samples
# Create the output samples -----
for k in range(N_CYCLES-1):
	output_samples = np.append(output_samples, samples)
# Play and record samples -------
recorded_samples = sd.playrec(output_samples, SAMPLING_FREQUENCY)
time.sleep(N_CYCLES/SIGNAL_FREQUENCY)

# PLOT ----------------------------
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
# Save figures --------------------
for k in range(len(figs)):
	figs[k].savefig(str(k+1) + '.' + mplt.image_format, bbox_inches='tight', dpi=mplt.dpi_rasterization)

plt.show()
