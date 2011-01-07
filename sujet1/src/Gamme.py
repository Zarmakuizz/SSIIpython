# -*- coding:utf-8 -*-

import math
from scipy.io import wavfile
import numpy

class Gamme:

	def __init__(self,fe=22050,f0=440,t=1.5):
		self.notes = 'azertyuiopqsd'
		self.fe = fe
		self.f0 = f0
		self.t = t
		
		self.notes_names = ['la','la#','si','do','do#','re','re#','mi','fa','fa#','sol','sol#']
		
		self.durees = {}
		self.setDurees(0.5) # Une noire dure 0.5 secondes
		
		self.fr = []
		self.notes = {}
		for i in xrange(len(self.notes_names)):
			self.fr.append( self.f0 * (2.0 ** (i/12.0)) ) # Toutes les fréquences en ordre croissant dans une liste
			self.notes[self.notes_names[i]] = self.fr[i]  # Fréquences des notes, note par note (dans un dico)
	
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
	
	def jouerMusique(self,filename = None):
		
		# Enregistre le signal d'un la 440 dans le fichier signal
		transition = self.cloche(self.notes['la'])
		f = open('signal.txt','w')
		for k in xrange(len(transition)):
			f.write(str(transition[k])+'\n')
		f.close()
		#import sys
		#sys.exit(0)
		
		if filename == None:
			air_notes = [ # au clair de la lune
				('do','noire'),
				('do','noire'),
				('do','noire'),
				('re','noire'),
				('mi','blanche'),
				('re','blanche'),
				('do','noire'),
				('mi','noire'),
				('re','noire'),
				('re','noire'),
				('do','noire')
			]
		else:
			air_notes = self.lireAir(filename)
		
		# On calcul les signaux à l'avance pour que la lecture soit fluide
		air_signals = [self.cloche(self.notes[note],self.durees[duree]) for (note,duree) in air_notes]
		self.play(air_signals,self.fe)
		
		wavfile.write('son.wav',self.fe,numpy.array([int(v * 2**15) for v in transition]))
		self.wavplay(transition,self.fe)
		
		tfe,tdata = wavfile.read('../ressources/NOTEguitare.wav')
		tdata2 = [v / 10000. for v in tdata]
		self.wavplay(tdata2,tfe)
	
	def cloche(self, fr, t=None):
		if t != None:
			self.t,t = t,self.t
			
		h = 1./self.fe
		taille = int(self.t*self.fe)
		tBis = [0.0, .1, .2, .4, .6, .9, 1.0]
		aBis = [0.0,  .6, 1.0, .4, .2, .1, 0.0]
		f = [0.5, 1.0, 1.188, 1.530, 2.00, 2.47, 2.61, 2.65, 2.99, 3.37, 4.14, 4.49, 4.83, 5.38, 5.86, 6.71, 8.08, 8.55, 9.02, 9.53, 11.03, 12.39]
		a = [350, 950, 500, 150, 700, 100, 250, 370, 1000, 180, 300, 100,  150,  300,  100,   100,  50,   20,   10,   35,   5,   15]

		print 'temps:',self.t,', taille: ',taille,' fe:',self.fe,', h:',h
		
		th = [h*i for i in xrange(taille)]
		f = [v*fr for v in f]
		tBis = [v*self.t for v in tBis]
		
		s = self.synthad(a,f,taille)
		env = self.envelop(tBis,aBis, taille)
		
		for i in xrange(len(s)):
			s[i] = s[i]*env[i];
		
		maximum = 0.
		for v in s:
			if abs(v) > maximum:
				maximum = abs(v)
			
		for i in xrange(taille): # 33076
			s[i]= (0.99 * s[i]) / maximum
		
		print 'max:',maximum
		
		# On redonne sa valeur par défaut à self.t si on l'avait modifiée
		if t != None:
			self.t = t
			
		return s
		
	def synthad(self, a, f, taille):
		n = taille # 33076
		dt = 1./self.fe
		
		s = [0.0] * n
		th = [i*dt for i in xrange(n)]
		
		for x in xrange(n):
			for i in xrange(len(f)):
				s[x] += a[i] * math.sin(2 * math.pi * f[i] * th[x])

		return s;
	
	def envelop(self,tBis, aBis, taille): # fe -> self.fe
		temp = tBis[-1]
		n = taille #33076 # len(th)
		dt = 1./self.fe

		th = [i*dt for i in xrange(n)]
		
		if tBis[0] >= temp:
			print 't incompatible dans envelop'
		
		if len(tBis) != len(aBis):
			print 't et a de longueur differente dans envelop'
		
		for i in xrange(1,len(tBis)-2):
			if tBis[i] <= tBis[i-1] or tBis[i] >= temp:
				tBis[i] = (tBis[i-1]+temp)/2
		
		ni = len(tBis)-1
		
		env = [0.00 for i in xrange(n)]
		
		h2 = 0
		for i in xrange(ni):
			h1 = h2 + 1
			h2 = int( 1 + float(tBis[i+1]/dt) )
			c = (aBis[i]-aBis[i+1])/(tBis[i]-tBis[i+1]); 
			b = ((tBis[i]*aBis[i+1])-(tBis[i+1]*aBis[i]))/(tBis[i]-tBis[i+1]);
			for m in xrange(h1-1,h2-1): # h2 -> h2-1
				env[m] = c*th[m]+b
				
		fw = open('env.txt','w')
		for k in xrange(len(env)):
			fw.write(str(env[k]) + '\n')
		fw.close()
		return env;
	
	def envelopZ(self,t,a,Fe):
		# enveloppe parametree par t et a = env(t) 
		# t contient une liste d'instants t_k
		# a contient la liste des amplitudes a_k aux instants t_k
		# env est le son echantillonne a la frequence Fe, 
		# affine par morceaux, tel que env(t_k) = a_k
		
		T = t[-1]       # Dernière case de t
		h = 1./Fe
		th = range(0,T,h)
		
		# Test validité de t
		if t[0] >= T:
			print 't incompatible dans envelop'
		
		# Test compatibilité t et a
		if length(t) != length(a):
			print 't et a de longueur differente dans envelop'
		
		# Au cas où on ne serait pas strictement croissant
		for k in xrange(1,):
			pass
			
	def wavplay(self,buff,fs,pan=0):
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
				
if __name__ == '__main__':
	gamme = Gamme(fe=8000)
	gamme.jouerMusique('lune.txt')
