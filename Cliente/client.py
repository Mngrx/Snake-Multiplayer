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


cobra = Snake()

print(cobra.__sizeof__()) 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Criação do Socket

