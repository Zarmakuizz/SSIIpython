# -*- coding:utf-8 -*-

class Gamme:

	def __init__(self):
		pass
		
	def envelop(self,t,a,Fe):
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
