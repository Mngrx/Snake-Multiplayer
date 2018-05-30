import pygame
import random
import sys
import socket
from pygame.locals import *



class Snake:
  xs = [190, 190, 190, 190, 190] # Posição de cada pedaço da Snake no eixo X
  ys = [190, 170, 150, 130, 110] # Posição de cada pedaço da Snake no eixo Y 
  img = pygame.Surface((20, 20)) # Criando quadrado do sprite da Snake
  img.fill((255, 127, 127))			 # Cor da Snake
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
cobra = Snake(450)
cobra2 = Snake(290)
lock = threading.Lock()

print(cobra.__sizeof__()) ##??

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Criação do Socket


##TODO-METODO PARA RECEBER A COBRA DO SERVIDOR
##TODO-METODO PARA PRITAR A COBRA QUE RECEBE DO SERVIDOR
##OK -- TODO-METODO PARA PEGAR COMANDOS DO TECLADO E MOVER A COBRA
##TODO-METODO PARA ENVIAR A COBRA APOS O MOVIMENTO PARA O SERVIDOR (PARA ATUALIZAR)
##TODO-DAR PARA O JOGADOR A OPÇÃO DE SE CONECTAR NOVAMENTE

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

