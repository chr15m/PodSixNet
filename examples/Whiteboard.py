from sys import exit
from os import environ
import pygame

SCREENSIZE = (640, 480)

environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)

pygame.font.init()
fnt = pygame.font.SysFont("Arial", 14)
txtpos = (100, 90)

class Whiteboard:
	def __init__(self):
		self.statusLabel = "connecting"
		self.playersLabel = "0 players"
		self.frame = 0
		self.down = False
	
	def Events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
				exit()
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.down = True
				self.PenDown(event)
			
			if event.type == pygame.MOUSEMOTION and self.down:
				self.PenMove(event)
			
			if event.type == pygame.MOUSEBUTTONUP:
				self.down = False
				self.PenUp(event)
	
	def Draw(self, linesets):
	        screen.fill([255, 255, 255])
		txt = fnt.render(self.statusLabel, 1, (0, 0, 0))
		screen.blit(fnt.render(self.statusLabel, 1, (0, 0, 0)), [10, 10])
		txt = fnt.render(self.playersLabel, 1, (0, 0, 0))
		screen.blit(fnt.render(self.playersLabel, 1, (0, 0, 0)), [10, 20])
		[[pygame.draw.aalines(screen, c, False, l) for l in lines if len(l) > 1] for c, lines in linesets]
	        pygame.display.flip()
		self.frame += 1

