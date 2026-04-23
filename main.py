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
        self.velocity = 0 
    
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
        self.horizontal_velo = random.choice([-4, 4]) #How many pixels the ball moves horizontally per frame
        self.vertical_velo = random.choice([-4, 4])#How many pixels the ball moves vertically per frame

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

class Score:
    def __init__(self):
        self.left_player_score = 0
        self.right_player_score = 0
        self.display_font = pygame.font.Font(None, 50)

    def draw(self, screen, screen_width):
        score_text = self.display_font.render(
            f"{self.left_player_score}  {self.right_player_score}",
            True,
            (255, 255, 255)
        )
        screen.blit(score_text, (screen_width // 2 - 40, 20))

    def increase_left_player_score(self):
        self.left_player_score += 1

    def increace_right_player_score(self):
        self.right_player_score += 1

class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 800
        self.screen_height = 600
        self.game_window = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong")

        self.frame_rate_controller = pygame.time.Clock()

        self.left_paddle = Paddle(Y=self.screen_height//2 - 60, width=20, height=120, speed=6)
        self.left_paddle.rect = pygame.Rect(50, self.left_paddle.Y, self.left_paddle.width, self.left_paddle.height)
        
        self.right_paddle = Paddle(Y=self.screen_height//2 - 60, width=20, height=120, speed=6)
        self.right_paddle.rect = pygame.Rect(self.screen_width - 70, self.right_paddle.Y, self.right_paddle.width, self.right_paddle.height)
        

        self.ball = Ball(
            x_position=self.screen_width//2 - 7,
            y_position=self.screen_height//2 - 7
        )

        self.score = Score()

        self.winning_score = 5
        self.game_over = False
        self.winner = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Left paddle controls
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        elif keys[pygame.K_s]:
            self.left_paddle.move_down()
        else:
            self.left_paddle.stop()

        # Right paddle controls
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        elif keys[pygame.K_DOWN]:
            self.right_paddle.move_down()
        else:
            self.right_paddle.stop()

    def check_collisions(self):
        # Ball collision with top/bottom
        if self.ball.position_and_size.top <= 0 or self.ball.position_and_size.bottom >= self.screen_height:
            self.ball.bounce_off_wall()

        # Ball collision with paddles
        if self.ball.position_and_size.colliderect(self.left_paddle.rect) or \
           self.ball.position_and_size.colliderect(self.right_paddle.rect):
            self.ball.bounce_off_paddle()

        # Scoring
        if self.ball.position_and_size.left <= 0:
            self.score.increase_left_player_score()
            self.ball.reset_to_center(self.screen_width, self.screen_height)
        elif self.ball.position_and_size.right >= self.screen_width:
            self.score.right_player_score += 1
            self.ball.reset_to_center(self.screen_width, self.screen_height)

        #Check Winner
        if self.score.left_player_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player 1"
        elif self.score.right_player_score >= self.winning_score:
            self.game_over = True
            self.winner = "Player 2"

    def update(self):
        self.left_paddle.update(self.screen_height)
        self.right_paddle.update(self.screen_height)
        self.ball.move()
        self.check_collisions()

    def draw(self):
        self.game_window.fill((0, 0, 0))  # Clear screen

        pygame.draw.rect(self.game_window, (255, 255, 255), self.left_paddle.rect)
        pygame.draw.rect(self.game_window, (255, 255, 255), self.right_paddle.rect)
        pygame.draw.ellipse(self.game_window, (255, 255, 255), self.ball.position_and_size)

        self.score.draw(self.game_window, self.screen_width)
        pygame.display.flip()

        #Instructions
        font = pygame.font.Font(None, 28)
        instructions = font.render(
            "Player 1: W/S | Player 2: Up/Down | First to 5 wins | Press R to restart",
            True,
            (255, 255, 255)
        )
        self.game_window.blit(instructions, (40, self.screen_height - 40))

        #Winner Message
        if self.game_over:
            big_font = pygame.font.Font(None, 60)
            win_text = big_font.render(f"{self.winner} Wins!", True, (255, 255, 255))
            self.game_window.blit(win_text, (self.screen_width//2 - 140, self.screen_height//2 - 30))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #Restart game
                if self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__() 

            if not self.game_over:
                self.handle_input()
                self.update()

            self.draw()
            self.frame_rate_controller.tick(60) 


# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()

