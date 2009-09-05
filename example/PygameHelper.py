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
txt = fnt.render("hello", 1, (0, 0, 0))

class PygameHelper:
	def Events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
				exit()
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.PenDraw(event)
				txtpos = event.pos
				txt = fnt.render('click', 1, (0, 0, 0))
	
	def Draw(self):
	        screen.fill([255, 255, 255])
		pygame.draw.rect(screen, [0, 0, 255, 100], (100, 100, 150, 100), 0)
		screen.blit(txt, txtpos)
	        pygame.display.flip()

