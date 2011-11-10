# -*- coding:utf-8 -*-

import math
from scipy.io import wavfile
import numpy

from Instruments import Cloche,Flute

class SoundCreator:

	def __init__(self,fe=22050,t=1.5):
		
		self.instruments = {
			'cloche' : Cloche(),
			'flute' : Flute()
		}
		
		self.instrument = self.instruments['cloche']
		self.fe = fe
		self.f0 = 110
		self.t = t
		
		self.notes_names = ['la1','la#1','si1','do2','do#2','re2','re#2','mi2','fa2','fa#2','sol2','sol#2']
		self.notes_names.extend(['la2','la#2','si2','do3','do#3','re3','re#3','mi3','fa3','fa#3','sol3','sol#3'])
		self.notes_names.extend(['la3','la#3','si3','do4','do#4','re4','re#4','mi4','fa4','fa#4','sol4','sol#4'])
		
		self.duree_noire = 0.5
		self.durees = {}
		self.setDurees(self.duree_noire) # Une noire dure 0.5 secondes
		
		self.fr = []
		self.notes = {}
		for i in xrange(len(self.notes_names)):
			self.fr.append( self.f0 * (2.0 ** (i/12.0)) ) # Toutes les fréquences en ordre croissant dans une liste
			self.notes[self.notes_names[i]] = self.fr[i]  # Fréquences des notes, note par note (dans un dico)
	
	def setInstrument(self,nom):
			"""
			Change l'instrument utilisé en l'instrument "nom"
			"""
			if nom not in self.instruments.keys():
				print 'Cet instrument n\'existe pas !'
			else:
				self.instrument = self.instruments[nom]
				print 'Instrument changé avec succès !'
	
	def setDurees(self,noire=0.5):
		"""
		Définit les durées des notes : croche, noire...
		Une noire dure "noire" seconde(s)
		"""
		self.durees['noire'] = noire
		self.durees['blanche'] = 2 * self.durees['noire']
		self.durees['ronde'] = 2 * self.durees['blanche']
		self.durees['croche'] = self.durees['noire'] / 2.
		self.durees['doublecroche'] = self.durees['croche']/2.
		self.durees['crochepointee'] = self.durees['noire']*(3/4.)
	
	def lireAir(self,filename):
		"""
		Lit une mélodie stockée dans le fichier "filename" et
		retourne une liste de la forme :
		[('do4','noire'),('re#4',croche)...]
		"""
		f = open(filename)
		air = [tuple(line.strip().split()) for line in f]
		f.close()
		return air
	
	def jouerFreq(self,freq,fe=None,coeff=1.):
		"""
		Joue la note de fréquence "freq",
		à la fréquence d'échantillonnage "fe"
		et avec le coefficient de saturation/diminution "coeff"
		"""
		if fe == None:
			fe = self.fe
		signal = self.instrument.signal(freq,coeff=coeff)
		self.playOne(signal,fe)
		
	def jouerNote(self,nom,fe=None,coeff=1.):
		"""
		Joue la note de nom "nom",
		à la fréquence d'échantillonnage "fe"
		et avec le coefficient de saturation/diminution "coeff"
		"""
		self.jouerFreq(self.notes[nom],fe,coeff=coeff)
	
	def stockeSignal(self,signal,filename):
		"""
		Stocke le signal "signal" dans le fichier "filename"
		"""
		f = open(filename,'w')
		for k in xrange(len(signal)):
			f.write(str(signal[k])+'\n')
		f.close()
	
	def music(self, filename, duree_noire=None, coeff=1.):
		"""
		Créé et retourne le signal correspondant à la mélodie stockée dans
		le fichier "filename".
		La vitesse de lecture peut être réglée en précisant la durée d'une
		noire en secondes ("duree_noire").
		On peut aussi appliquer un coefficient de saturation/diminution "coeff".
		"""
		if duree_noire != None:
			self.setDurees(duree_noire)
		
		air_notes = self.lireAir('../ressources/scores/' + filename + '.txt')
		
		# On calcul les signaux à l'avance pour que la lecture soit fluide
		air_signals = [self.instrument.signal(self.notes[note],self.durees[duree],coeff=coeff) for (note,duree) in air_notes]
		
		self.setDurees(self.duree_noire)
		
		return air_signals
	
	def playMusic(self, filename = None, duree_noire=None, coeff=1.):
		"""
		Joue la mélodie stockée dans le fichier "filename".
		La vitesse de lecture peut être réglée en précisant la durée d'une
		noire en secondes ("duree_noire").
		On peut aussi appliquer un coefficient de saturation/diminution "coeff".
		"""
		air_signals = self.music(filename,duree_noire,coeff)
		self.play(air_signals,self.fe)
		
	def saveMusic(self, filename = None, duree_noire=None, coeff=1.):
		"""
		Enregistre la mélodie stockée dans le fichier "filename".
		La vitesse de lecture peut être réglée en précisant la durée d'une
		noire en secondes ("duree_noire").
		On peut aussi appliquer un coefficient de saturation/diminution "coeff".
		"""
		air_signals = self.music(filename,duree_noire,coeff)
		self.wavfilewrite('../ressources/generated/' + filename + '.wav',air_signals)
			
	def playOne(self,buff,fs,pan=0):
		"""
		Joue le son correspondant au signal "buff",
		à la fréquence d'échantillonnage "fs".
		"""
		import audiere
		from time import sleep
                print audiere.get_devices()
		d = audiere.open_device()
		s = d.open_array(buff,fs)
		s.pan = pan
		s.play()
		while s.playing:
			sleep(.01)
			
	def play(self,buffs,fs,pan=0):
		"""
		Joue successivement les sons correspondants aux signaux
		stockés dans la matrice "buffs",
		à la fréquence d'échantillonnage "fs".
		"""
		import audiere
		from time import sleep
                print audiere.get_devices()
		d = audiere.open_device()
		sons = [d.open_array(buff,fs) for buff in buffs]
		for son in sons:
			son.play()
			while son.playing:
				sleep(0.01)

	def wavfilewriteOne(self,filename,signal,display=False):
		"""
		Enregistre le son correspondant au signal "signal"
		dans le fichier "filename".
		Si "display" est mis à True, les informations sur le fichier Wave
		écrit sont affichées, ainsi que le spectre et le spectrogramme du
		signal.	Le spectre et le spectrogramme sont également enregistrés
		dans le dossier "generated".
		"""
		import wave
		from Sound import Sound
		# On va convertir le signal sous forme d'un flux binaire
		hexdata= ''
		for s in signal:
			hexdata += wave.struct.pack('h',int(s*self.fe)) # transformation

		# Écriture du fichier
		audio_file = wave.open(filename,'wb')
		audio_file.setparams((1,2,self.fe,len(signal),'NONE','noncompressed'))
		audio_file.writeframes(hexdata)
		audio_file.close()
		
		if display:
			self.afficheInfos(filename)
	
	def wavfilewrite(self,filename,signals,display=False):
		"""
		Enregistre le son correspondant au signaux contenus
		dans la matrice "signals" mis bout à bout 
		dans le fichier "filename".
		Si "display" est mis à True, les informations sur le fichier Wave
		écrit sont affichées, ainsi que le spectre et le spectrogramme du
		signal. Le spectre et le spectrogramme sont également enregistrés
		dans le dossier "generated".
		"""
		import wave
		from Sound import Sound
		# On va convertir le signal sous forme d'un flux binaire
		hexdata= ''
		for signal in signals:
			for s in signal:
				hexdata += wave.struct.pack('h',int(s*self.fe)) # transformation

		# Écriture du fichier
		audio_file = wave.open(filename,'wb')
		audio_file.setparams((1,2,self.fe,len(signal),'NONE','noncompressed'))
		audio_file.writeframes(hexdata)
		audio_file.close()
		
		if display:
			self.afficheInfos(filename)
		
	def afficheInfos(self,filename):
		"""
		Affiche les informations sur le fichier Wave "filename",
		ainsi que le spectre et le spectrogramme du	signal.
		Le spectre et le spectrogramme sont également enregistrés
		dans le même dossier que le fichier wave.
		ATTENTION : le fichier Wave doit bien avoir l'extension .wav
		(pourrait être amélioré)
		"""
		from Sound import Sound
		print '#####################################'
		print '# Informations sur le fichier écrit #'
		print '#####################################'
		sound = Sound(filename)
		print sound
		sound.displaySpectrum()
		sound.saveSpectrum(filename[:-4] + '_spectrum.png')
		sound.displaySpectrogram(title='Spectrogramme du signal')
		sound.saveSpectrogram(filename[:-4] + '_spectrogram.png',title='Spectrogramme du signal')

	def wavfileplay(self, filename):
		"""
		Cette méthode est censée jouer le fichier "filename" mais on ne s'en sert pas
		dans l'application et elle ne fonctionne pas si la commande "play" n'est pas installée.
		"""
		# Souci d'interopérabilité Windows & Linux, et mort aux OS X
		import platform, os
		if platform.platform().startswith('win'):
			from winsound import PlaySound, SND_FILENAME, SND_ASYNC
			audio_file=open(filename,'rb')
			PlaySound(audio_file, SND_FILENAME|SND_ASYNC)
		elif platform.platform().find('linux')>-1 or platform.platform().find('Linux')>-1:
			#os.system('exec play ' + filename)
			os.execl('play',filename)
