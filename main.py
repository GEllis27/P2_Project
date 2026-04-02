import pygame, sys, random

pygame.init()

Width, Height = 600, 800
FONT = pygame.font.SysFont("Consolas", int(Width/20))
SCREEN = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Pong!")
CLOCK = pygame.time.Clock()

    
class Paddle:
    def __init__(self, Y, width, height, speed):
        self.Y = Y
        self.width = width
        self.height = height
        self.speed = speed
    
    def move_up(self):
        self.velocity = -self.speed
    
    def move_down(self):
        self.velocity = self.speed
    
    def stop(self):
        self.velocity = 0

    def update(self, screen_height):
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
    