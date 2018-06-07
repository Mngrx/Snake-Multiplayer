import pygame
import random
import sys
import threading
import time
import pickle
import socket
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from pygame.locals import *

g = random.randint(0, 590)

class Snake:
	xs = [190, 190, 190, 190, 190] # Posição de cada pedaço da Snake no eixo X
	ys = [190, 170, 150, 130, 110] # Posição de cada pedaço da Snake no eixo Y 
	img = pygame.Surface((20, 20)) # Criando quadrado do sprite da Snake
	img.fill((255, 127, 127))			 # Cor da Snake
	dirs = 0 											 # Direção da Snake
	score = 0											 # Pontuação desta Snake

	def __init__(self, num):
		self.xs = [num, num, num, num, num]
		self.yx = [num, num-20, num-40, num-60, num-80]

	def getImg(self):
		return self.img

	def getDir(self):
		return self.dirs
	
	def setDir(self, dirs):
		self.dirs = dirs

	def getScore(self):
		return self.score

	def getLength(self):
		return len(self.xs)
	
	def increaseSize(self):
		self.xs.append(700)
		self.ys.append(700)

	def increaseScore(self):
		self.score += 1

	def getSize(self):
		return self.xs, self.ys

	def setSize(self, xs, ys):
		self.xs, self.ys = xs, ys

## Variáveis globais do jogo
pygame.init()
s = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')
f = pygame.font.SysFont('Arial', 20)
clock = pygame.time.Clock()
cobra = Snake(450)
cobra2 = Snake(290)
cobras = []
lock = threading.Lock()
HOST = ''              # Endereco IP do Servidor
PORT = 13000            # Porta que o Servidor esta

##Funções do servidor
def collide(x1, x2, y1, y2, w1, w2, h1, h2):
	if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:return True
	else:return False
def die(screen, score):
	f=pygame.font.SysFont('Arial', 30);
	t=f.render('Your score was: '+str(score), True, (0, 0, 0));
	screen.blit(t, (10, 270));
	pygame.display.update();
	pygame.time.wait(2000);
	sys.exit(0)

def listenNewSnake():
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	orig = (HOST, PORT)
	tcp.bind(orig)
	tcp.listen(1)
	con, cliente = tcp.accept()
	data = con.recv(1024)
	data = pickle.loads(data)
	print(data[0])	
	cobras[data[2]] = data[0]
	data = pickle.dumps(cobras)
	con.send(data)

def printGameScreen():
	while True:
		#print(threading.current_thread())
		clock.tick(30)
		s.fill((255, 255, 255))
		#lock.acquire()
		for c in cobras:	
			#printSnake(c) 	
		#lock.release()
		#time.sleep(0.01)
			t1 = threading.Thread(target=printSnake, args=([c]))
			t1.start()
			t1.join()
		pygame.display.update()
'''
def move():
	while True:
		#print(threading.current_thread())
		lock.acquire()
		for e in pygame.event.get():
			if e.type == QUIT:
				sys.exit(0)
			elif e.type == KEYDOWN:
				if e.key == K_UP and cobras[0].getDir() != 0:
						cobras[0].setDir(2)
						print(2)
				elif e.key == K_DOWN and cobras[0].getDir() != 2:
						cobras[0].setDir(0)
						print(0)
				elif e.key == K_LEFT and cobras[0].getDir() != 1:
						cobras[0].setDir(3)
				elif e.key == K_RIGHT and cobras[0].getDir() != 3:
						cobras[0].setDir(1)

		i = cobra.getLength()-1
		while i >= 1:
			cobras[0].xs[i] = cobras[0].xs[i-1]
			cobras[0].ys[i] = cobras[0].ys[i-1]
			i -= 1
		if cobras[0].getDir() == 0:
			cobras[0].ys[0] += 20
		elif cobras[0].getDir() == 1:
			cobras[0].xs[0] += 20
		elif cobras[0].getDir() == 2:
			cobras[0].ys[0] -= 20
		elif cobras[0].getDir() == 3:
			cobras[0].xs[0] -= 20
		lock.release()
		time.sleep(0.1)
'''
def printSnake(cb):
	lock.acquire()
	for i in range(0, cb.getLength()):
			s.blit(cb.getImg(), (cb.xs[i], cb.ys[i]))
	lock.release()
	time.sleep(0.1)


#xs = [290, 290, 290, 290, 290];
#ys = [290, 270, 250, 230, 210];




listenNewSnake()
t = threading.Thread(target=printGameScreen)
t2 = threading.Thread(target=move)
#t.setDaemon(True)
#t2.setDaemon(True)
t.start()
t2.start()

	
t2.join()
t.join()
