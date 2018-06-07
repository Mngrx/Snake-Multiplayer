import pygame
import random
from random import randint
import sys
import socket, pickle, threading, time
from pygame.locals import *

lock = threading.Lock() #Inicialização do sistema de semáforo
pygame.init() #Inicialização do Pygame


class Snake:
  xs = [190, 190, 190, 190, 190] # Posição de cada pedaço da Snake no eixo X
  ys = [190, 170, 150, 130, 110] # Posição de cada pedaço da Snake no eixo Y 
  img = pygame.Surface((20, 20)) # Criando quadrado do sprite da Snake
  color = (randint(0,255), randint(0,255), randint(0,255))
  img.fill(color) # Cor da Snake
  dirs = 0 											 # Direção da Snake
  score = 0											 # Pontuação desta Snake
  name = "jorge"

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

  def move(self):
    while True:
      lock.acquire()
      for e in pygame.event.get():
        if e.type == QUIT:
          sys.exit(0)
        elif e.type == KEYDOWN:
          if e.key == K_UP and self.dirs != 0:
              self.dirs = 2
              print(2)
          elif e.key == K_DOWN and self.dirs != 2:
              self.dirs = 0
              print(0)
          elif e.key == K_LEFT and self.dirs != 1:
              self.dirs = 3
              print(3)
          elif e.key == K_RIGHT and self.dirs != 3:
              self.dirs = 1
              print(1)
      lock.release()



HOST = 'localhost'
PORT = 13001

# Create a socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


'''
# Create an instance of ProcessData() to send to server.
variable = ProcessData()
variable2 = ProcessData()
variables = ("juninho",[12, "melhor", "vida", 213])

# Pickle the object and send it to the server
data_string = pickle.dumps(variables)
s.send(data_string)

s.close()
'''
cobra = Snake()

def serverComunication():
  while True:
    data = (cobra.name, [cobra.dirs, cobra.xs, cobra.ys, cobra.color])
    data_pickle = pickle.dumps(data)
    s.send(data_pickle)
    data_pickle = s.recv(1024)
    data = pickle.loads(data_pickle)
    print(data)
    if (data[1] == 'out'):
      break
  s.close()


serverComunication()

s = pygame.display.set_mode((600, 600))



t = threading.Thread(target=cobra.move())
t2 = threading.Thread(target=serverComunication())
t.start()
t2.start()


