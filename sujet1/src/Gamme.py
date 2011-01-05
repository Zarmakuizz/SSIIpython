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
		
	def jouerMusique(self):
		fr = []
		for i in xrange(13):
			fr.append( self.f0 * (2.0 ** (i/12.0)) )
		
		transition = self.cloche(fr[0])
		signal = []
		for j in xrange(33076):
			signal.append( int( (2.0 ** 15.0) * transition[j] ) )
		
		f = open('signal.txt','w')
		for k in xrange(len(signal)):
			f.write(str(transition[k])+'\n')
		f.close()
		
		wavfile.write('son.wav',self.fe,numpy.array(signal))
		self.wavplay(signal,self.fe)
		print signal[:24]
		#samples=toByte(signal); /* conversion en bytes */
		#play(samples);
	
	def cloche(self, fr): # t -> self.t // fe -> self.fe
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
		
		s = self.synthad(a,f)
		env = self.envelop(tBis,aBis)
		
		for i in xrange(len(s)):
			s[i] = s[i]*env[i];
		
		maximum = 0.
		for v in s:
			if abs(v) > maximum:
				maximum = abs(v)
			
		for i in xrange(33076):
			s[i]= (0.99 * s[i]) / maximum
		
		print 'max:',maximum
		return s
		
	def synthad(self, a, f):
		n = 33076
		dt = 1./self.fe
		
		s = [0.0] * n
		th = [i*dt for i in xrange(n)]
		
		for x in xrange(n):
			for i in xrange(len(f)):
				s[x] += a[i] * math.sin(2 * math.pi * f[i] * th[x])

		return s;
	
	def envelop(self,tBis, aBis): # fe -> self.fe
		temp = tBis[-1]
		n = 33076 # len(th)
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
			for m in xrange(h1-1,h2):
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

if __name__ == '__main__':
	gamme = Gamme()
	gamme.jouerMusique()
