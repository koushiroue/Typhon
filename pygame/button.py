import pygame
import sys
import os
from config import *

pygame.font.init()
guiFont = pygame.font.SysFont("Arial",30)

class Button:
	def __init__(self, text, width, height, pos, elevation):
		# Core Attributes
		self.pressed = False
		self.elevation = elevation
		self.dynamicElevation = elevation
		self.original_y_pos = pos[1]

		# Top rectangle
		self.topRect = pygame.Rect(pos, (width, height))
		self.topColour = "#475F77"

		# Bottom rectangle
		self.bottomRect = pygame.Rect(pos, (width, elevation))
		self.bottomColour = "#354B5E"

		# text
		self.textSurf = guiFont.render(text, True, "#FFFFFF")
		self.textRect = self.textSurf.get_rect(center=self.topRect.center)

	def draw(self,screen):
		# Elevation logic
		self.topRect.y = self.original_y_pos - self.dynamicElevation
		self.textRect.center = self.topRect.center

		self.bottomRect.midtop = self.topRect.midtop;
		self.bottomRect.height = self.topRect.height + self.dynamicElevation

		pygame.draw.rect(screen, self.bottomColour, self.bottomRect, border_radius=15)
		pygame.draw.rect(screen, self.topColour, self.topRect, border_radius=15)
		screen.blit(self.textSurf, self.textRect)
		return self.checkClick()


	def checkClick(self):
		action = False
		pos = pygame.mouse.get_pos()
		if self.topRect.collidepoint((pos)):
			self.topColour = "#D74B4B"
			if pygame.mouse.get_pressed()[0]== 1 and self.pressed == False:
				self.dynamicElevation = 0
				self.pressed = True
				action = True
			else:
				self.dynamicElevation = self.elevation;
				if self.pressed == True:
					print("Click")
					self.pressed = False
		else:
			self.dynamicElevation = self.elevation;
			self.topColour = "#475F77"

		if pygame.mouse.get_pressed()[0] == 0:
			self.pressed = False

		return action



