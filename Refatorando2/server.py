import pygame
import random
from random import randint
import sys
import socket
import pickle
import threading
import time

cobras = {}  # Dicionário de cobras
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket
HOST = ''
PORT = 13007
lock = threading.Lock()  # Inicialização do sistema de semáforo

listen = (HOST, PORT)

s.bind(listen)

clock = pygame.time.Clock()
tela = pygame.display.set_mode((800,640))
pygame.display.set_caption('Snake')
img = pygame.Surface((20, 20))


#Função atualizar movimento (será thread)
def monitorarConexao(conn):
  nome = None #futuro
  
  while 1:   
    try:
      data = conn.recv(4096)
      #print(data)
    except:
      del cobras[nome]
    cobra = pickle.loads(data)  # cobra == [nome, dir, xs, yx, cor]
    print("---------------------------------------\n")
    print(cobra)
    if nome is None:
      nome = cobra[0]
    if collide(cobra):
      del cobras[nome]
      break
    cobra = atualizarMovimento(cobra)
    lock.acquire()
    cobras[nome] = cobra
    lock.release()
    time.sleep(0.1)
    data = pickle.dumps(cobras)
    conn.send(data)

  print("asdasd")

  #del cobras[nome]
  #conn.close()
  #threading._shutdown()

def aux_collide(x1, x2, y1, y2, w1, w2, h1, h2):
  if x1+w1>x2 and x1<x2+w2 and y1+h1>y2 and y1<y2+h2:return True
  else:return False
  
def collideWithOtherSnake(cobra):
  pass

def collide(cobra):
  lock.acquire()
  lista_cobras = cobras.values()
  lock.release()
  for c in lista_cobras:
    i = len(cobra[2])-1
    while i >= 2:
      if aux_collide(cobra[2][0], c[2][i], cobra[3][0], c[3][i], 20, 20, 20, 20):
        return True
      i -= 1

  if cobra[2][0] < 0 or cobra[2][0] > 800 or cobra[3][0] < 0 or cobra[3][0] > 640:
  			return True
  
  return False

def atualizarMovimento(cobra):
  #lock.acquire()
  i = len(cobra[2])-1
  while i >= 1:
    cobra[2][i] = cobra[2][i-1]
    cobra[3][i] = cobra[3][i-1]
    i -= 1
  if cobra[1] == 0:
    cobra[3][0] += 20
  elif cobra[1] == 1:
    cobra[2][0] += 20
  elif cobra[1] == 2:
    cobra[3][0] -= 20
  elif cobra[1] == 3:
    cobra[2][0] -= 20
  #lock.release()
  return cobra

def printSnake(cb):
  lock.acquire()
  img.fill(cb[4])
  for i in range(0, len(cb[2])):
    tela.blit(img, (cb[2][i], cb[3][i]))
  lock.release()
  time.sleep(0.1)

def printGameScreen():
  while True:
    clock.tick(12)
    tela.fill((255, 255, 255))
    #lock.acquire()
    time.sleep(0.01)
    lista_cobras = cobras.values()
    #lock.release()
   
    for c in lista_cobras:	
      t1 = threading.Thread(target=printSnake, args=([c]))
      t1.start()
      #t1.join()
    pygame.display.update()


impressao = threading.Thread(target=printGameScreen)
impressao.start()

while 1:
  s.listen(1)
  conn, addr = s.accept()
  print('Connected by', addr)
  t = threading.Thread(target=monitorarConexao, args=[conn])
  t.start()

