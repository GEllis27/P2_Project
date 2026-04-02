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
    
class Ball:
    def __init__(self, x_position, y_position):
        self.position_and_size = pygame.Rect(x_position, y_position, 15, 15)
        self.horizontal_velo = 4 #How many pixels the ball moves horizontally per frame
        self.vertical_velo = 4 #How many pixels the ball moves vertically per frame

    def move(self):
        self.position_and_size.x += self.horizontal_velo #How many pixels the ball moves horizontally per frame
        self.position_and_size.y += self.vertical_velo #How many pixels the ball moves vertically per frame

    def bounce_off_wall(self):
        self.vertical_velo *= -1 #Reverses the vertical velocity to bounce off the wall

    def bounce_off_paddle(self):
        self.horizontal_velo *= -1 #Reverses the horizontal velocity to bounce off the paddle

    def reset_to_center(self, screen_width, screen_height):
        self.position_and_size.center = (screen_width // 2, screen_height // 2) #Resets the ball to the center of the screen
        self.horizontal_velo *= -1 #Change the direction of the ball after a point is scored