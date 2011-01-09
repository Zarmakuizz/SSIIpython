# -*- coding:utf-8 -*-

import numpy as np
import scipy as sp
import scipy.fftpack as fftpack
import matplotlib as mpl
import matplotlib.pyplot as plt

from scipy.io import wavfile
import wave, struct

class Sound:
	
	def __init__(self,filename=None,signal=None):
		
		if filename != None:
			self.filename = filename
			wav = wave.open(self.filename,'rb')
			(self.nb_channels, self.sample_width, self.framerate, self.nb_frames, self.compression_type, self.compression_name) = wav.getparams()
				
			(framerate2,values) = wavfile.read(self.filename)
			
			self.signal = [2*float(value)/(2**(8*self.sample_width)) for value in values]
			
			self.processSpectrum()
	
	def extractSignal(self):
		"""
		Extrait le signal discret du fichier "self.filename".
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
		"""
		Stocke le signal dans le fichier "filename" afin qu'il puisse
		être tracé avec Gnuplot.
		[[[ Méthode non implémentée pour le moment. ]]]
		"""
		pass
	
	def processSpectrum(self,N=4096):
		"""
		Calcule le spectre (avec N points) du signal.
		"""
		self.frequency_range = [v*(float(self.framerate)/N) for v in xrange(N)]
		self.spectrum = abs(fftpack.fft(self.signal,N)) / N
	
	#########################
	# Fonctions d'affichage #
	#   et de sauvegarde    #
	#########################
	
	#         #
	# Spectre #
	#         #
	
	def plot(self,signal,N=4096,title='',xlabel='',ylabel='',saveas='',display=False):
		"""
		Affiche (si "display" est à True) et/ou enregistre (si "saveas" est précisé)
		le signal "signal".
		
		N : le nombre de points à utiliser pour tracer la courbe (plus cette valeur
		est élevée, plus le tracé sera précis)
		
		title : le titre à donner au graphique
		xlabel : la légende à apposer sur l'axe des abscisses
		ylabel : la légende à apposer sur l'axe des ordonnées
		
		L'enregistrement peut être fait dans n'importe quel format supporté par la 
		backend utilisée par Matplotlib. Le format d'enregistrement est 
		déterminé à partir de l'extension du fichier.
		"""
		plt.clf()
		plt.plot(signal)
		plt.grid(True)
		plt.title(title)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		if display:
			plt.show()
		if saveas != '':
			plt.savefig(saveas)
	
	def plotSpectrum(self,N=4096,title=None):
		"""
		Crée le spectre du signal.
		
		N : le nombre de points à utiliser pour tracer la courbe (plus cette valeur
		est élevée, plus le tracé sera précis)
		
		title : le titre à donner au graphique
		"""
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
		"""
		Affiche le spectre du signal.
		
		N : le nombre de points à utiliser pour tracer la courbe (plus cette valeur
		est élevée, plus le tracé sera précis)
		
		title : le titre à donner au graphique
		"""
		self.plotSpectrum(N,title)
		plt.show()
	
	def saveSpectrum(self,filename,N=4096,title=None):
		"""
		Enregistre le spectre du signal.
		
		N : le nombre de points à utiliser pour tracer la courbe (plus cette valeur
		est élevée, plus le tracé sera précis)
		
		title : le titre à donner au graphique
		"""
		self.plotSpectrum(N,title)
		plt.savefig(filename)
	
	#               #
	# Spectrogramme #
	#               #
	
	def plotSpectrogram(self,N=4096,title='Spectrogramme'):
		"""
		Crée le spectrogramme du signal.
		
		N : le nombre de points à utiliser pour tracer la courbe (plus cette valeur
		est élevée, plus le tracé sera précis)
		
		title : le titre à donner au graphique
		"""
		plt.clf()
		plt.specgram(self.signal,N,self.framerate)
		plt.colorbar()
		plt.xlabel('Temps (en secondes)')
		plt.ylabel('Frequence (en Hz)')
		plt.title(title + ', Fe=' + str(self.framerate) + ' (' + str(N) + ' points)')
		
	def displaySpectrogram(self,N=4096,title='Spectrogramme'):
		"""
		Affiche le spectrogramme du signal.
		
		N : le nombre de points à utiliser pour tracer la courbe (plus cette valeur
		est élevée, plus le tracé sera précis)
		
		title : le titre à donner au graphique
		"""
		self.plotSpectrogram(N,title)
		plt.show()
		
	def saveSpectrogram(self,filename,N=4096,title='Spectrogramme'):
		"""
		Enregistre le spectre du signal.
		
		N : le nombre de points à utiliser pour tracer la courbe (plus cette valeur
		est élevée, plus le tracé sera précis)
		
		title : le titre à donner au graphique
		"""
		self.plotSpectrogram(N,title)
		plt.savefig(filename)
		

	########################
	# Méthodes surchargées #
	########################
	
	def __str__(self):
		"""
		Affiche les informations du fichier Wave :
		- nombre de canaux
		- fréquence d'échantillonnage
		- Nombre d'échantillons
		- place occupée par un échantillon en mémoire
		"""
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
