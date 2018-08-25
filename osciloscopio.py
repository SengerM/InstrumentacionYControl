# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 20:42:30 2018

@author: admin
"""

import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy.signal as signal

volumen = 1.0       # rango en que se mueve [0.0, 1.0]
fs = 48000          # sampling rate, Hz, debe ser entero
f = 200.0           # frecuencia
duracion = 2        # en segundos, duracion de la muestra
#chunk=1024         por ahora no lo vamos a usar
sd.default.samplerate = fs
sd.default.channels = 1 
funcion='cc'        
#tipo de funcion con que vamos a exitar: sinusoideal,triangular,cc

if funcion == 'sinusoideal':
    #funcion sinusoideal de frecuencia f 
    data = (np.sin(2*np.pi*np.arange(fs*duracion)*f/fs)).astype(np.float32)
if funcion == 'triangular':
    #funcion triangular de frecuencia f
    simetria=0.5 #0.5 es simetrica de ambos lados
    t= np.linspace(0,1,int(fs*duracion))
    data = (signal.sawtooth(2 * np.pi * f * t,simetria)).astype(np.float32)
if funcion == 'cc':
    #funcion continua
    data = np.linspace(volumen,volumen,int(fs*duracion))
 
#corre y graba la funcion data
grabacion = sd.playrec(data*volumen)

#esperamos a que termine
time.sleep(duracion)

#ploteamos la tension de entrada en funcion del tiempo
t=np.linspace(0,duracion,int(fs*duracion))
plt.plot(t,grabacion[:,0])

#ploteamos la tension de entrada en funcion de la tension de salida
plt.plot(data,grabacion[:,0])

t=np.linspace(0,duracion,int(fs*duracion))
plt.plot(t,data)