import pygame
import random
from random import randint
import sys
import socket, pickle
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
cobra = Snake();
#cobra2 = Snake(290)
lock = threading.Lock()

#print(cobra.__sizeof__()) ##??

#HOST = 'localhost'
#PORT = 50007
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Criação do Socket



##TODO-DAR PARA O JOGADOR A OPÇÃO DE SE CONECTAR NOVAMENTE

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

#PrintSnak
def printSnake(cb):
	lock.acquire()
	for i in range(0, cb.getLength()):
			s.blit(cb.getImg(), (cb.xs[i], cb.ys[i]))
	lock.release()
	time.sleep(0.1)

#metodo que solicida conexão e recebe uma posição vazia.
def conectation():
	s.connect((HOST, PORT))
	sock.send("request\n".encode('UTF-8'))
	decision = sock.recv(1024)

	if(clearString(decision) == "Denied"):
		print ("Solicitacao negada. Tente novamente mais tarde.")
	else:
		position = int(decision)
		cobra = Snake(position)
	#enviando a cobra criada 
	data = pikle.dumps(cobra)
	#MANDAR UMA COBRA INICIADA EM POSITION, MANDAR A COBRA JUNTO COM UMA MENSAGEM PARA SER TRATADA LA NO SERVIDOR
	sock.send(data;"")

	sock.close()

#metodo que captura o movimento da combra e envia para o servidor
def move():
	while True:
		print(threading.current_thread())
		lock.acquire()
		for e in pygame.event.get():
			if e.type == QUIT:
				sys.exit(0)
			elif e.type == KEYDOWN:
				if e.key == K_UP and cobras.getDir() != 0:
						cobras.setDir(2)
						print(2)
				elif e.key == K_DOWN and cobras.getDir() != 2:
						cobras.setDir(0)
						print(0)
				elif e.key == K_LEFT and cobras.getDir() != 1:
						cobras.setDir(3)
				elif e.key == K_RIGHT and cobras.getDir() != 3:
						cobras.setDir(1)

		i = cobras.getLength()-1
		while i >= 1:
			cobras.xs[i] = cobras.xs[i-1]
			cobras.ys[i] = cobras.ys[i-1]
			i -= 1
		if cobras.getDir() == 0:
			cobras.ys[0] += 20
		elif cobras.getDir() == 1:
			cobras.xs[0] += 20
		elif cobras.getDir() == 2:
			cobras.ys[0] -= 20
		elif cobras.getDir() == 3:
			cobras.xs[0] -= 20
		lock.release()
		time.sleep(0.1)

		#MANDAR A COBRA ATUALIZADA PARA O SERVIDOR PARA QUE SEJA ATUALIZADA NA LISTA COM AS NOVAS POSICOES


