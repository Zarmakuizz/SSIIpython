# -*- coding:utf-8 -*-

import numpy as np
import scipy as sp
import scipy.fftpack as fftpack
import matplotlib as mpl
import matplotlib.pyplot as plt

from scipy.io import wavfile
import wave, struct

class Sound:
	
	def __init__(self,filename):
		self.filename = filename
		wav = wave.open(self.filename,'rb')
		(self.nb_channels, self.sample_width, self.framerate, self.nb_frames, self.compression_type, self.compression_name) = wav.getparams()
			
		(framerate2,values) = wavfile.read(self.filename)
		
		self.signal = [2*float(value)/(2**(8*self.sample_width)) for value in values]
		
		self.processSpectrum()
	
	def extractSignal(self):
		"""
		Cette fonction n'est pas utilisée dans l'application car la fonction read
		de scipy.io.wavfile (présente depuis la version 0.7 de scipy) retourne déjà
		un tableau contenant les valeurs des échantillons du signal.
		"""
		wav = wave.open(self.filename,'rb')
		self.frames = wav.readframes(self.nb_frames)
		self.signal = None
		if self.sample_width == 1:
			# 8 bit : unsigned char
			self.signal = struct.unpack('%sB' % (self.nb_frames * self.nb_channels), self.frames)
		elif self.sample_width == 2:
			# 16 bits : signed short
			self.signal = struct.unpack('%sh' % (self.nb_frames * self.nb_channels), self.frames)
	
	def storeForGNUPlot(self,filename):
		pass
	
	def processSpectrum(self,N=4096):
		self.frequency_range = [v*(float(self.framerate)/N) for v in xrange(N)]
		self.spectrum = abs(fftpack.fft(self.signal,N)) / N
	
	#########################
	# Fonctions d'affichage #
	#   et de sauvegarde    #
	#########################
	
	#         #
	# Spectre #
	#         #
	
	def plotSpectrum(self,N=4096,title=None):
		if title == None:
			title = 'Spectre ' + str(N) + ' points'
		self.processSpectrum(N)
		plt.clf()
		#plt.figure()
		plt.plot(self.frequency_range,self.spectrum[:N])
		plt.grid(True)
		plt.title(title)
		plt.xlabel('Frequence (en Hz)')
		plt.ylabel('Spectre d\'amplitude')
		#plt.suptitle('Blabla')
		
	def displaySpectrum(self,N=4096,title=None):
		self.plotSpectrum(N,title)
		plt.show()
	
	def saveSpectrum(self,filename,N=4096,title=None):
		self.plotSpectrum(N,title)
		plt.savefig(filename)
	
	#               #
	# Spectrogramme #
	#               #
	
	def plotSpectrogram(self,N=4096,title='Spectrogramme'):
		plt.clf()
		plt.specgram(self.signal,N,self.framerate)
		plt.colorbar()
		plt.xlabel('Temps (en secondes)')
		plt.ylabel('Frequence (en Hz)')
		plt.title(title + ', Fe=' + str(self.framerate) + ' (' + str(N) + ' points)')
		
	def displaySpectrogram(self,N=4096,title='Spectrogramme'):
		self.plotSpectrogram(N,title)
		plt.show()
		
	def saveSpectrogram(self,filename,N=4096,title='Spectrogramme'):
		self.plotSpectrogram(N,title)
		plt.savefig(filename)
		

	########################
	# Méthodes surchargées #
	########################
	
	def __str__(self):
		mode = ''
		if self.nb_channels == 1:
			mode = '(mono)'
		elif self.nb_channels == 2:
			mode = '(stereo)'
			
		str = 'Nombre de canaux : %s %s\n' % (self.nb_channels , mode)
		str += 'Frequence d\'echantillonnage : %s Hz\n' % self.framerate
		str += 'Nombre d\'echantillons : %s\n' % self.nb_frames
		str += 'Largeur d\'un echantillon : %s octets (%s bits)\n' % (self.sample_width,8*self.sample_width)
		str += 'Largeur totale du tableau des echantillons : %s\n' % (self.nb_frames * self.sample_width)
		#str += 'Largeur totale du tableau des echantillons : %s\n' % len(self.frames)
		str += 'Type de compression : %s\n' % self.compression_type
		str += 'Compression : %s\n' % self.compression_name
		return str
