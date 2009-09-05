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
		self.status = "connecting"
		self.players = "0 players"
	
	def Events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
				exit()
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.PenDraw(event)
	
	def Draw(self):
	        screen.fill([255, 255, 255])
		txt = fnt.render(self.status, 1, (0, 0, 0))
		pygame.draw.rect(screen, [0, 0, 255, 100], (100, 100, 150, 100), 0)
		screen.blit(fnt.render(self.status, 1, (0, 0, 0)), [10, 10])
		screen.blit(fnt.render(self.players, 1, (0, 0, 0)), [10, 20])
	        pygame.display.flip()

