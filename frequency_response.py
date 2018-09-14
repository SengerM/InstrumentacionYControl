import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib_my_utils as mplt
import timestamp as tmstmp
import scipy.optimize as opt
import os
os.system('cls')
# Parameters ------------------------------------
SIGNAL_FREQUENCIES = np.logspace(np.log10(100),np.log10(10e3),20) # In Hertz.
# -----------------------------------------------
timestamp = tmstmp.get()
figs = [] # Do not touch this, ja!

def frequency_response(frequencies, amplitude=1, measuring_cycles=100, rancius_time=0.5, sampling_frequency=48000):
	# Validations -----------------------------------
	if not isinstance(sampling_frequency, int):
		raise ValueError('sampling_frequency must be an integer number!')
	if amplitude > 1:
		raise ValueError('AMPLITUDE must be less than 1 because the output samples must lie between +-1')
	
	amplitudes = [None]*len(frequencies)
	phase = [None]*len(frequencies)
	for k in range(len(frequencies)):
		samples = np.sin(2*np.pi*np.arange(sampling_frequency/frequencies[k]*(rancius_time*frequencies[k] + measuring_cycles))*frequencies[k]/sampling_frequency)
		samples -= np.min(samples)
		samples /= np.max(samples)
		samples -= 0.5
		samples *= 2*amplitude
		samples = samples.astype(np.float32)
		# Play and record samples -----------------------

		recorded_samples = sd.playrec(samples, sampling_frequency, channels=2)
		sd.wait() #it waits and returns as the recording is finished.
		recorded_samples = np.transpose(recorded_samples)
		recorded_samples_fixed = [None]*2
		params = [None]*2
		for l in range(2): # Left and right channels.
			recorded_samples_fixed[l] = recorded_samples[l][np.int(sampling_frequency*rancius_time):] # Discard rancius samples.
			# Fit sine to data:
			funcSin = lambda params,x : params[0]*np.sin(params[1]*x + params[2])
			func = funcSin
			ErrorFunc = lambda params,x,y: func(params,x)-y # ErrorFunc is the diference between the func and the y "experimental" data
			params0 = (1.0,frequencies[k]/sampling_frequency*2*np.pi,0) # "First guess" of the parameters.
			params[l],success = opt.leastsq(ErrorFunc,params0[:],args=(np.arange(len(recorded_samples_fixed[l])),recorded_samples_fixed[l]))
		
		# f, axes = plt.subplots(2, sharex=True, figsize=(mplt.fig_width*mplt.fig_ratio[0]/25.4e-3, mplt.fig_width*mplt.fig_ratio[1]/25.4e-3)) # Create the figure for plotting.
		# f.subplots_adjust(hspace=0.3) # Fine-tune figure; make subplots close to each other and hide x ticks for all but bottom plot.
		# figs.append(f)
		# axes[0].plot(recorded_samples_fixed[0], color=mplt.colors[0], label='Data left')
		# axes[0].plot(func(params[0],np.arange(len(recorded_samples_fixed[0]))), color=mplt.colors[1], label='Fit left')
		# axes[1].plot(recorded_samples_fixed[1], color=mplt.colors[2], label='Data right')
		# axes[1].plot(func(params[1],np.arange(len(recorded_samples_fixed[1]))), color=mplt.colors[3], label='Fit right')
			
		amplitudes[k] = np.max(recorded_samples_fixed[0])/np.max(recorded_samples_fixed[1])
		phase[k] = (params[0][2] - params[1][2])*180/np.pi # Phase difference.
		if phase[k]<-90: #so there are no phase breaks
			phase[k]=180+phase[k]
		if phase[k]<-90:
			phase[k]=180+phase[k]
            
	return np.array(amplitudes), np.array(phase)


amplitude, phase = frequency_response(SIGNAL_FREQUENCIES)

# PLOT ------------------------------------------
f, axes = plt.subplots(2, sharex=True, figsize=(mplt.fig_width*mplt.fig_ratio[0]/25.4e-3, mplt.fig_width*mplt.fig_ratio[1]/25.4e-3)) # Create the figure for plotting.
f.subplots_adjust(hspace=0.3) # Fine-tune figure; make subplots close to each other and hide x ticks for all but bottom plot.
figs.append(f)
axes[0].plot(SIGNAL_FREQUENCIES, amplitude, color=mplt.colors[0], label='Amplitude', marker='.')
axes[1].plot(SIGNAL_FREQUENCIES, phase, color=mplt.colors[1], label='Phase', marker='.')
for k in range(len(axes)):
	mplt.beauty_grid(axes[k])
axes[0].set_ylabel('Amplitude')
axes[1].set_ylabel('Phase (deg)')
axes[-1].set_xlabel('Time (s)')
axes[-1].set_xscale('log')
axes[-1].set_xlabel('Frequency (Hz)')
# Save figures -----------------------------------
for k in range(len(figs)):
	figs[k].savefig(timestamp + '_' + str(k+1) + '.' + mplt.image_format, bbox_inches='tight', dpi=mplt.dpi_rasterization)

plt.show()
