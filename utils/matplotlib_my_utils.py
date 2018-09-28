import numpy as np

dpi_rasterization = 200 # Resolution for png format.
image_format = 'pdf'
colors = [(255, 102, 0), (51, 153, 255), (51, 102, 0), (255, 0, 255)]
colors = np.array(colors)/255
fig_width = 160e-3 # Figure width in meters (size of the chart+axis_ticks, not counting legend, title, etc.).
fig_ratio = [1, 0.8] # XY ratio aspect of figures.

def beauty_grid(ax):
	ax.grid(b=True, which='major', color='#000000', alpha=0.3, linestyle='-', linewidth=0.5)
	ax.grid(b=True, which='minor', color='#000000', alpha=0.15, linestyle='-', linewidth=0.25)
	ax.minorticks_on() # Enables minor ticks without text, only the ticks.
