# -*- coding:utf-8 -*-

#~ Flute :
#~ tBis = [0, 0.1, 0.2, 0.9, 1]
#~ aBis = [0, 0.8, 1, 0.8, 0]
#~ a = [1000, 50 , 80, 10, 5, 2, 0.1, 1]
#~ f = [i for i in xrange(1,len(a))]

#~ Cloche :
#~ tBis = [0.0, .1, .2, .4, .6, .9, 1.0]
#~ aBis = [0.0,  .6, 1.0, .4, .2, .1, 0.0]
#~ f = [0.5, 1.0, 1.188, 1.530, 2.00, 2.47, 2.61, 2.65, 2.99, 3.37, 4.14, 4.49, 4.83, 5.38, 5.86, 6.71, 8.08, 8.55, 9.02, 9.53, 11.03, 12.39]
#~ a = [350, 950, 500, 150, 700, 100, 250, 370, 1000, 180, 300, 100,  150,  300,  100,   100,  50,   20,   10,   35,   5,   15]

class Instrument:
	"""
	Crée un instrument avec une enveloppe temporelle et une
	composition fréquentielle données.
	"""
	def __init__(self,a,f,aBis,tBis,name):
		"""
		tBis/aBis : pour enveloppe
		a/f : pour synthad
		"""
		self.name = name
		self.a = a
		self.f = f
		self.aBis = aBis
		self.tBis = tBis
		
		self.synth = None
		self.env = None
	
	def synthad(self, a, f, taille, fe):
		"""
		Synthèse additive. Créé un son composé des partiels f(n) d'amplitude a(n).
		
		fe : fréquence d'échantillonnage.
		
		Retourne la composition fréquentielle obtenue à partir des tableaux
		a et f.
		"""
		from math import pi,sin
		s = [0.0] * taille
		th = [i*(1./fe) for i in xrange(taille)] # Création du vecteur temps discret
		
		# Création du son.
		# Boucle pour ajouter une à une les composantes fréquentielles.
		for x in xrange(taille):
			for i in xrange(len(f)):
				s[x] += a[i] * sin(2 * pi * f[i] * th[x])
				
		return s
		
	def envelop(self,tBis, aBis, taille, fe):
		"""
		Retourne l'enveloppe temporelle paramétrée par les tableaux
		tBis et aBis : le son échantillonné à la fréquence fe,
		affine par morceaux.
		
		tBis : liste d'instants t_k
		aBis : liste des amplitudes a_k aux instants t_k
		"""
		temp = tBis[-1]
		dt = 1./fe

		th = [i*dt for i in xrange(taille)]
		
		if tBis[0] >= temp:
			print 't incompatible dans envelop'
		
		if len(tBis) != len(aBis):
			print 't et a de longueur differente dans envelop'
		
		for i in xrange(1,len(tBis)-2):
			if tBis[i] <= tBis[i-1] or tBis[i] >= temp:
				tBis[i] = (tBis[i-1]+temp)/2
		
		ni = len(tBis)-1
		
		env = [0.00] * taille
		
		h2 = 0
		for i in xrange(ni):
			h1 = h2 + 1
			h2 = int( 1 + float(tBis[i+1]/dt) )
			c = (aBis[i]-aBis[i+1])/(tBis[i]-tBis[i+1]); 
			b = ((tBis[i]*aBis[i+1])-(tBis[i+1]*aBis[i]))/(tBis[i]-tBis[i+1])
			for m in xrange(h1-1,h2-1):
				env[m] = c*th[m]+b
		
		## HS ##
		fw = open('../ressources/generated/enveloppe_' + self.name + '.txt','w')
		for k in xrange(len(env)):
			fw.write(str(env[k]) + '\n')
		fw.close()
		##    ##
		
		return env
	
	def signal(self,fr,t=1.5, fe=8000, coeff=1.):
		"""
		Multiplie l'enveloppe temporelle et la composition fréquentielle
		et retourne le signal obtenu.
		
		fr : la fréquence de la note à créer.
		t : la durée du signal à créer
		fe : fréquence d'échantillonnage
		
		coeff: ce coefficient permet
			- de diminuer le volume du son si il est compris entre 0 et 1
			- d'appliquer une saturation au son si il est supérieur à 1
		"""
		coeff = float(coeff)
		
		taille = int(t * fe)
		
		print 'temps:',t,', taille: ',taille,' fe:',fe,', h:',1./fe
		
		a = self.a
		f = [v*fr for v in self.f]
		aBis = self.aBis
		tBis = [v*t for v in self.tBis]
		
		s = self.synthad(a,f,taille,fe)
		env = self.envelop(tBis,aBis, taille,fe)
		
		self.synth = s
		self.env = env

		for i in xrange(len(s)):
			s[i] = s[i]*env[i];

		# Calcul du maximum
		maximum = max([abs(v) for v in s])
		
		print 'max:',maximum
		
		# Normalisation si coeff=1
		# Saturation si coeff > 1
		# Diminution du volume si coeff entre 0 et 1
		for i in xrange(taille):
			s[i]= (coeff * s[i]) / maximum
			if s[i] > 1:
				s[i] = 1
			elif s[i] < -1:
				s[i] = -1
		
		return s

class Cloche(Instrument):
	"""
	Créé un instrument qui produit des sons de cloche.
	"""
	def __init__(self):
		tBis = [0.0, .1, .2, .4, .6, .9, 1.0]
		aBis = [0.0,  .6, 1.0, .4, .2, .1, 0.0]
		f = [0.5, 1.0, 1.188, 1.530, 2.00, 2.47, 2.61, 2.65, 2.99, 3.37, 4.14, 4.49, 4.83, 5.38, 5.86, 6.71, 8.08, 8.55, 9.02, 9.53, 11.03, 12.39]
		a = [350, 950, 500, 150, 700, 100, 250, 370, 1000, 180, 300, 100,  150,  300,  100,   100,  50,   20,   10,   35,   5,   15]
		Instrument.__init__(self,a,f,aBis,tBis,'cloche')

class Flute(Instrument):
	"""
	Créé un instrument qui produit des sons de flute.
	"""
	def __init__(self):
		tBis = [0, 0.1, 0.2, 0.9, 1]
		aBis = [0, 0.8, 1, 0.8, 0]
		a = [1000, 50 , 80, 10, 5, 2, 0.1, 1]
		f = [i for i in xrange(1,len(a))]
		Instrument.__init__(self,a,f,aBis,tBis,'flute')
