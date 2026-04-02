import pygame, sys, random

pygame.init()

Width, Height = 600, 800
FONT = pygame.font.SysFont("Consolas", int(Width/20))
SCREEN = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Pong!")
CLOCK = pygame.time.Clock()

    