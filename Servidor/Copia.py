import pygame
import random
import sys
import threading
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
	pass

def printGameScreen():
  	pass



#xs = [290, 290, 290, 290, 290];
#ys = [290, 270, 250, 230, 210];

pygame.init();
clock = pygame.time.Clock()
cobra = Snake(190)
cobra2 = Snake(290)

cobras = [cobra]


def main(cobra):
	s = pygame.display.set_mode((600, 600))
	pygame.display.set_caption('Snake')
	appleimage = pygame.Surface((10, 10))
	appleimage.fill((0, 255, 0))
	#img = pygame.Surface((20, 20));
	#img.fill((255, 127, 127));
	f = pygame.font.SysFont('Arial', 20) 
	while True:
		clock.tick(12)
		for e in pygame.event.get():
			if e.type == QUIT:
				sys.exit(0)
			elif e.type == KEYDOWN:
				if e.key == K_UP and cobra.getDir() != 0:
						cobra.setDir(2)
				elif e.key == K_DOWN and cobra.getDir() != 2:
						cobra.setDir(0)
				elif e.key == K_LEFT and cobra.getDir() != 1:
						cobra.setDir(3)
				elif e.key == K_RIGHT and cobra.getDir() != 3:
						cobra.setDir(1)
		i = cobra.getLength()-1

		while i >= 2:
			if collide(cobra.xs[0], cobra.xs[i], cobra.ys[0], cobra.ys[i], 20, 20, 20, 20):
				die(s, cobra.getScore())
			i-= 1
		if collide(cobra.xs[0], applepos[0], cobra.ys[0], applepos[1], 20, 10, 20, 10):
			cobra.increaseScore()
			cobra.increaseSize()
			applepos=(random.randint(0,590),random.randint(0,590))
		if cobra.xs[0] < 0 or cobra.xs[0] > 580 or cobra.ys[0] < 0 or cobra.ys[0] > 580:
			die(s, cobra.getScore())
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
		s.fill((255, 255, 255))	

		
		for i in range(0, cobra.getLength()):
			s.blit(cobra.getImg(), (cobra.xs[i], cobra.ys[i]))

		s.blit(appleimage, applepos)
		t=f.render(str(cobra.getScore()), True, (0, 0, 0))
		s.blit(t, (10, 10))
		pygame.display.update()


t1 = threading.Thread(target=main, args=([cobra]))
#t2 = threading.Thread(target=main, args=(cobra2))
#
t1.start()
#t2.start()
					
			


