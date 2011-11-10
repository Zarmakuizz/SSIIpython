# -*- coding:cp850 -*-

# http://matplotlib.sourceforge.net/
# http://docs.scipy.org/doc/scipy/reference/

import numpy as np
import scipy as sp
import scipy.fftpack as fftpack
import matplotlib as mpl
import matplotlib.pyplot as plt


from Sound import Sound

from Gamme import Gamme

if __name__ == '__main__':
	
	son = Sound('../ressources/NOTEguitare.wav')
	print son
	son.displaySpectrum()
	son.displaySpectrogram(title='Spectrogramme du signal original')
	son.saveSpectrum('spectre.png')
	son.saveSpectrogram('spectrogramme.png',title='Spectrogramme du signal original')
