# -*- coding:utf-8 -*-

from Gamme import Gamme

class Sujet2:
	def __init__(self,gamme):
		self.gamme = gamme
			
	def jouerFreq(self):
		while True:
			freq = str(raw_input('Fréquence ("quit" pour quitter, "menu" pour revenir au menu principal) : '))
			if freq == 'quit':
				self.stop()
			elif freq == 'menu':
				break
			freq = int(freq)
			c = self.askForCoeff()
			self.gamme.jouerFreq(freq,coeff=c)

	def jouerNom(self):
		while True:
			nom = str(raw_input('Nom ("quit" pour quitter, "menu" pour revenir au menu principal) : '))
			if nom == 'quit':
				self.stop()
			elif nom == 'menu':
				break
			c = self.askForCoeff()
			self.gamme.jouerNote(nom,coeff=c)

	def jouerMusique(self):
		print 'Jouer une musique déjà écrite...'
		filename = str(raw_input('Nom de la musique (nom du fichier dans lequel elle est stockée sans l\'extension) (defaut : sweetdreams) : '))
		if filename == '':
			filename = 'sweetdreams'
		filename+='.txt'
			
		noirestr = str(raw_input('Durée d\'une noire (en secondes) (defaut : 0.5) : '))
		if noirestr == '':
			noirestr = '0.5'
		noire = float(noirestr)
		
		freq_ech_str = str(raw_input('Fréquence d\'échantillonnage (defaut : 8000) : '))
		if freq_ech_str == '':
			freq_ech_str = self.gamme.fe
		freq_ech = int(freq_ech_str)
		
		c = self.askForCoeff()
		
		fe,self.gamme.fe = self.gamme.fe,freq_ech
		self.gamme.jouerMusique(filename,noire,coeff=c)
		self.gamme.fe = fe

	def askForCoeff(self):
		c = str(raw_input('Coefficient de saturation (ex 5.3, defaut 1.) : '))
		if c == '':
			return 1.
		return float(c)

	def notesCmd(self):
		
		menu = {
			'1' : self.jouerFreq,
			'2' : self.jouerNom,
			'3' : self.stop
		}
		
		print 'Jouer des notes en ligne de commande...'
		print "1. Par fréquence (440, 520...)"
		print "2. Par nom (la3, do#3...)"
		print "3. Quitter"
		
		n = str(raw_input('Choix : '))
		menu.get(n,self.default)()

	def notesGraphical(self):
		import Tkinter as tk
		
		piano = ['la2','la#2','si2','do3','do#3','re3','re#3','mi3','fa3','fa#3','sol3','sol#3',
		'la3','la#3','si3','do4','do#4','re4','re#4','mi4','fa4','fa#4','sol4','sol#4']
		
		N = len(piano)
		
		window = tk.Tk()
		window.title('Clavier virtuel')
		
		#~ nb_cols = N/2 # 2 = nb_lines
		#~ for i in xrange(N):
			#~ button = tk.Button(window,text=lowercase[i],command=None)
			#~ button.grid(row=i/nb_cols,column=i%nb_cols)
			
		note = None
		diese = None
		liste_dieses = []
		col = 0
		for i in xrange(N-1):
			if '#' in piano[i]:
				diese = tk.Button(window,text=piano[i][:len(piano[i])-1]+'\n'+piano[i][len(piano[i])-1],command= lambda nom=piano[i]:self.gamme.jouerNote(nom),background='black',foreground='white',height=15,width=2)
				diese.grid(sticky=tk.N,row=0,column=col-1,columnspan=2)
				liste_dieses.append(diese)
			else:
				note = tk.Button(window,text=piano[i],command=lambda nom=piano[i]:self.gamme.jouerNote(nom),background='white',foreground='black',height=20,width=4)
				note.grid(row=0,column=col,rowspan=2,columnspan=4)
				col += 4
		
		for diese in liste_dieses:
			diese.lift()
		#window.geometry(str((col/4)*note.winfo_reqwidth())+'x'+str(note.winfo_reqheight()))
			
		window.mainloop()
		#~ b = Button(fen1,text=string.lowercase[i],command=None,background='black',foreground='white',height=15,width=2,padx=5,pady=5)
		#~ b = Button(fen1,text=string.lowercase[i],command=None,background='white',foreground='black',height=20,width=4,padx=5,pady=5)

	def default(self):
		print 'L\'option choisie n\'existe pas.'

	def stop(self):
		import sys
		sys.exit(0)

	def changeInstrument(self):
		print 'Choisissez l\'instrument parmi :'
		for instrument in self.gamme.instruments.keys():
			print '\t- '+instrument
		nom = str(raw_input('Choix : '))
		self.gamme.setInstrument(nom)

	def display_menu(self):
		
		menu = {
			'1' : self.jouerMusique,
			'2' : self.notesCmd,
			'3' : self.notesGraphical,
			'4' : self.changeInstrument,
			'5' : self.stop
		}
		
		print "################"
		print "##### MENU #####"
		print "################"
		print
		print "1. Jouer une musique écrite"
		print "2. Jouer des notes en ligne de commande"
		print "3. Jouer des notes sur un clavier graphique"
		print "4. Changer d'instrument"
		print "5. Quitter"
		print
		
		n = str(raw_input('Choix : '))
		menu.get(n,self.default)()

if __name__ == '__main__':
	
	# Enregistre le signal d'un la 440 dans le fichier signal.txt
	gamme = Gamme(8000)
	sujet1 = Sujet2(gamme)
	
	transition = gamme.instrument.signal(gamme.notes['la3'])
	gamme.stockeSignal(transition,'signal.txt')
	
	while True:
		 sujet1.display_menu()
	
	
	#gamme.jouerMusique('sweetdreams.txt',0.1)
	#gamme.jouerMusique('lune.txt')
	
	#gamme.wavplay(gamme.cloche(gamme.notes['la3']),gamme.fe)
