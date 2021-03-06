# -*- coding:utf-8 -*-

import math
from scipy.io import wavfile
import numpy

from Instruments import Cloche,Flute

class Gamme:

	def __init__(self,fe=22050,f0=220,t=1.5):
		
		self.instruments = {
			'cloche' : Cloche(),
			'flute' : Flute()
		}
		
		self.instrument = self.instruments['cloche']
		self.fe = fe
		self.f0 = f0
		self.t = t
		
		self.notes_names = ['la2','la#2','si2','do3','do#3','re3','re#3','mi3','fa3','fa#3','sol3','sol#3']
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
			if nom not in self.instruments.keys():
				print 'Cet instrument n\'existe pas !'
			else:
				self.instrument = self.instruments[nom]
				print 'Instrument changé avec succès !'
	
	def setDurees(self,noire=0.5):
		self.durees['noire'] = noire
		self.durees['blanche'] = 2 * self.durees['noire']
		self.durees['ronde'] = 2 * self.durees['blanche']
		self.durees['croche'] = self.durees['noire'] / 2.
		self.durees['doublecroche'] = self.durees['croche']/2.
	
	def lireAir(self,filename):
		f = open(filename)
		air = [tuple(line.strip().split()) for line in f]
		f.close()
		return air
	
	def jouerFreq(self,freq,fe=None,coeff=1.):
		if fe == None:
			fe = self.fe
		signal = self.instrument.signal(freq,coeff=coeff)
		self.wavplay(signal,fe)
		
	def jouerNote(self,nom,fe=None,coeff=1.):
		self.jouerFreq(self.notes[nom],fe,coeff=coeff)
	
	def stockeSignal(self,signal,filename):
		f = open(filename,'w')
		for k in xrange(len(signal)):
			f.write(str(signal[k])+'\n')
		f.close()
	
	def jouerMusique(self, filename = None, duree_noire=None, coeff=1.):
		
		if duree_noire != None:
			self.setDurees(duree_noire)
		
		if filename == None:
			air_notes = [ # au clair de la lune
				('do3','noire'),
				('do3','noire'),
				('do3','noire'),
				('re3','noire'),
				('mi3','blanche'),
				('re3','blanche'),
				('do3','noire'),
				('mi3','noire'),
				('re3','noire'),
				('re3','noire'),
				('do3','noire')
			]
		else:
			air_notes = self.lireAir(filename)
		
		# On calcul les signaux à l'avance pour que la lecture soit fluide
		air_signals = [self.instrument.signal(self.notes[note],self.durees[duree],coeff=coeff) for (note,duree) in air_notes]
		self.wavfilewrite('son.wav',air_signals)
		self.play(air_signals,self.fe)
		
		#~ wavfile.write('son.wav',self.fe,numpy.array([int(v * 2**15) for v in transition]))
		#~ self.wavplay(transition,self.fe)
		
		#~ tfe,tdata = wavfile.read('../ressources/NOTEguitare.wav')
		#~ tdata2 = [v / 10000. for v in tdata]
		#~ self.wavplay(tdata2,tfe)
		
		self.setDurees(self.duree_noire)
			
	def playOne(self,buff,fs,pan=0):
		'''Plays a sound buffer with blocking, matlab-style
		'''
		import audiere
		from time import sleep
		d = audiere.open_device()
		s = d.open_array(buff,fs)
		s.pan = pan
		s.play()
		while s.playing:
			sleep(.01)
			
	def play(self,buffs,fs,pan=0):
		'''Plays a sound buffer with blocking, matlab-style
		'''
		import audiere
		from time import sleep
		d = audiere.open_device()
		sons = [d.open_array(buff,fs) for buff in buffs]
		for son in sons:
			son.play()
			while son.playing:
				sleep(0.01)

	def wavfilewriteOne(self,filename,signal):
		import wave
		# On va convertir le signal sous forme d'un flux binaire
		hexdata= ''
		for s in signal:
			hexdata += wave.struct.pack('h',int(s*self.fe)) # transformation

		# Écriture du fichier
		audio_file = wave.open(filename,'wb')
		audio_file.setparams((1,2,self.fe,len(signal),'NONE','noncompressed'))
		audio_file.writeframes(hexdata)
		audio_file.close()
		
	def wavfilewrite(self,filename,signals):
		import wave
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

	def wavfileplay(self, filename):
		# Souci d'interopérabilité Windows & Linux, et mort aux OS X
		import platform, os
		if platform.platform().startswith('win'):
			from winsound import PlaySound, SND_FILENAME, SND_ASYNC
			audio_file=open(filename,'rb')
			PlaySound(audio_file, SND_FILENAME|SND_ASYNC)
		elif platform.platform().find('linux')>-1 or platform.platform().find('Linux')>-1:
			#os.system('exec play ' + filename)
			os.execl('play',filename)
	
if __name__ == '__main__':
	gamme = Gamme(fe=8000)
	gamme.wavfilewriteOne('truc.wav',gamme.instrument.signal(gamme.notes['la3']))
	#gamme.wavplay(gamme.instrument.signal(gamme.notes['la3']),gamme.fe)
	gamme.instrument = Flute()
	gamme.playOne(gamme.instrument.signal(gamme.notes['la3']),gamme.fe)
	gamme.instrument = Cloche()
	
	#gamme.jouerMusique('sweetdreams.txt',0.1)
	#gamme.jouerMusique('lune.txt')
	
	gamme.jouerMusique('jeuxinterdits.txt',0.5)
	#print '====='
	#gamme.wavfileplay('son.wav')
