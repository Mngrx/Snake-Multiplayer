import pygame
import random
from random import randint
import sys
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import socket, pickle, threading, time
from pygame.locals import *



class Snake:
  xs = [190, 190, 190, 190, 190] # Posição de cada pedaço da Snake no eixo X
  ys = [190, 170, 150, 130, 110] # Posição de cada pedaço da Snake no eixo Y 
  img = pygame.Surface((20, 20)) # Criando quadrado do sprite da Snake
  img.fill((randint(0,255), randint(0,255), randint(0,255))) # Cor da Snake
  dirs = 0 											 # Direção da Snake
  score = 0											 # Pontuação desta Snake

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
##FAZER O SERVIDOR RECEBER APENAS 3 JOGADORES, PARA NÃO COMPROMETER O DESEMPENHO DO JOGO
##CLIENTE SOLICITA CONEXÃO E O SERVIDOR RESPONDE COM UMA POSIÇÃO VAZIA, PARA QUE A COBRA DO-
##CLIENTE SEJA CRIADA NESSA POSIÇÃO.
##CASO O CLIENTE MORRA, DEVE APARECER PARA O CLIENTE UMA OPÇÃO DE RECONECT.


## Variáveis globais do jogo
pygame.init()
s = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')
f = pygame.font.SysFont('Arial', 20)
clock = pygame.time.Clock()
cobra = ""
cobras = []
#cobra2 = Snake(290)
lock = threading.Lock()

#print(cobra.__sizeof__()) ##??

HOST = 'localhost'
PORT = 13000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Criação do Socket



##TODO-DAR PARA O JOGADOR A OPÇÃO DE SE CONECTAR NOVAMENTE

def upSnakeAndGetList():
	sock.connect((HOST, PORT))
	data = pickle.dumps((cobra, "snake", "player1"))
	sock.send(data) #mandar a cobra e uma mensagem indicando a atualização da cobra 

	data = sock.recv(4096)
	sock.close()
	cobras = pickle.loads(data)

#Recebe uma lista de snakes e printa
def printGameScreen():
	#SOLICIDAT E RECEBER DO SERVIDOR UMA LISTA DE COBRAS ATUALIZADAS PARA PRINTAR AQUI
	while True:
		print(threading.current_thread())
		clock.tick(32)
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

#PrintSnake
def printSnake(cb):
	lock.acquire()
	for i in range(0, cb.getLength()):
			s.blit(cb.getImg(), (cb.xs[i], cb.ys[i]))
	lock.release()
	time.sleep(0.1)

#metodo que solicida conexão e recebe uma posição vazia.
def conectation():
	negado = False
	sock.connect(('localhost', 13000))
	data = pickle.dumps(("-", "solicitation"))
	sock.send(data) #manda a solicitação para a posicao inicial da cobra

	sock.close()
	decision = sock.recv(1024)

	if(clearString(decision) == "Denied"):
		print ("Solicitacao negada. Tente novamente mais tarde.")
	else:
		position = int(decision)
		cobra = Snake(position)
		negado = True
	sock.close()

	return negado

#metodo que captura o movimento da combra e envia para o servidor
def move():
	while True:
		print(threading.current_thread())
		lock.acquire()
		for e in pygame.event.get():
			if e.type == QUIT:
				sys.exit(0)
			elif e.type == KEYDOWN:
				if e.key == K_UP and cobra.getDir() != 0:
						cobra.setDir(2)
						print(2)
				elif e.key == K_DOWN and cobra.getDir() != 2:
						cobra.setDir(0)
						print(0)
				elif e.key == K_LEFT and cobra.getDir() != 1:
						cobra.setDir(3)
				elif e.key == K_RIGHT and cobra.getDir() != 3:
						cobra.setDir(1)

		i = cobra.getLength()-1
		while i >= 1:
			cobra.xs[i] = cobra.xs[i-1]
			cobra.ys[i] = cobra.ys[i-1]
			i -= 1
		if cobra.getDir() == 0:
			cobra.ys[0] += 20
		elif cobra.getDir() == 1:
			cobra.xs[0] += 20
		elif cobra.getDir() == 2:
			cobra.ys[0] -= 20
		elif cobra.getDir() == 3:
			cobra.xs[0] -= 20
		lock.release()
		time.sleep(0.1)

		upSnakeAndGetList()

		#MANDAR A COBRA ATUALIZADA PARA O SERVIDOR PARA QUE SEJA ATUALIZADA NA LISTA COM AS NOVAS POSICOES

if not conectation:
	t = threading.Thread(target=printGameScreen)
	t2 = threading.Thread(target=move)

	t.start()
	t2.start()	
	
	t2.join()
	t.join()
