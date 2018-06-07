import pygame
import random
from random import randint
import sys
import socket
import pickle
import threading
import time
from pygame.locals import *

global cobra 

pygame.init() #Inicialização do Pygame
cobras = {}  # Dicionário de cobras
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket
HOST = 'localhost'
PORT = 13005
lock = threading.Lock()

dest = (HOST, PORT)

s.connect(dest)
xs = [190, 190, 190, 190, 190]
ys = [190, 170, 150, 130, 110]
nome = "Jorge"

cobra = [nome, 0, xs, ys,
         (randint(0, 255), randint(0, 255), randint(0, 255))]

cobras = {}

clock = pygame.time.Clock()
tela = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Snake')
img = pygame.Surface((20, 20))


def move():
  #while True:
  lock.acquire()
  for e in pygame.event.get():
    if e.type == QUIT:
      sys.exit(0)
    elif e.type == KEYDOWN:
      if e.key == K_UP and cobra[1] != 0:
          cobra[1] = 2
          print(2)
      elif e.key == K_DOWN and cobra[1] != 2:
          cobra[1] = 0
          print(0)
      elif e.key == K_LEFT and cobra[1] != 1:
          cobra[1] = 3
          print(3)
      elif e.key == K_RIGHT and cobra[1] != 3:
          cobra[1] = 1
          print(1)
  lock.release()

def printSnake(cb):
  lock.acquire()
  img.fill(cb[4])
  for i in range(0, len(cb[2])):
			tela.blit(img, (cb[2][i], cb[3][i]))
  lock.release()
  time.sleep(0.1)

def printGameScreen():
  while True:
    clock.tick(10)
    tela.fill((255, 255, 255))
    for c in cobras.values():	
      t1 = threading.Thread(target=printSnake, args=([c]))
      t1.start()
      t1.join()
    pygame.display.update()



#movimento = threading.Thread(target=move) #Thread para atualizar a direção da cobra
impressao = threading.Thread(target=printGameScreen)
#movimento.start()
impressao.start()
#movimento.join()
#impressao.join()




while 1:
  move()
  lock.acquire()
  cobra_pickle = pickle.dumps(cobra)
  s.send(cobra_pickle)
  cobras_pickle = s.recv(4096)
  cobras = pickle.loads(cobras_pickle)
  lock.release()
  print("---------------------------------------\n")
  print(cobras)
  cobra = cobras[nome]

s.close()



