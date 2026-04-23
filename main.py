import pygame, sys, random

pygame.init()

WIDTH, HEIGHT = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")
CLOCK = pygame.time.Clock()


# ---------------- PADDLE ----------------
class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed
        self.velocity = 0

        self.rect = pygame.Rect(x, y, width, height)

    def move_up(self):
        self.velocity = -self.speed

    def move_down(self):
        self.velocity = self.speed

    def stop(self):
        self.velocity = 0

    def update(self, screen_height):
        self.rect.y += self.velocity
        self.rect.y = max(0, min(self.rect.y, screen_height - self.height))


# ---------------- BALL ----------------
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.horizontal_velo = random.choice([-4, 4])
        self.vertical_velo = random.choice([-4, 4])

    def move(self):
        self.rect.x += self.horizontal_velo
        self.rect.y += self.vertical_velo

    def bounce_wall(self):
        self.vertical_velo *= -1

    def bounce_paddle(self):
        self.horizontal_velo *= -1

    def reset(self, screen_width, screen_height):
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.horizontal_velo = random.choice([-4, 4])
        self.vertical_velo = random.choice([-4, 4])


# ---------------- SCORE ----------------
class Score:
    def __init__(self):
        self.left = 0
        self.right = 0
        self.font = pygame.font.Font(None, 50)

    def draw(self, screen, width):
        text = self.font.render(f"{self.left}  {self.right}", True, (255, 255, 255))
        screen.blit(text, (width // 2 - 40, 20))

    def add_left(self):
        self.left += 1

    def add_right(self):
        self.right += 1


# ---------------- GAME ----------------
class Game:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT

        self.screen = SCREEN
        self.clock = CLOCK

        self.left_paddle = Paddle(50, HEIGHT // 2 - 60, 20, 120, 6)
        self.right_paddle = Paddle(WIDTH - 70, HEIGHT // 2 - 60, 20, 120, 6)

        self.ball = Ball(WIDTH // 2, HEIGHT // 2)

        self.score = Score()

        self.winning_score = 5
        self.game_over = False
        self.winner = None

    # -------- INPUT --------
    def handle_input(self):
        keys = pygame.key.get_pressed()

        # left
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        elif keys[pygame.K_s]:
            self.left_paddle.move_down()
        else:
            self.left_paddle.stop()

        # right
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        elif keys[pygame.K_DOWN]:
            self.right_paddle.move_down()
        else:
            self.right_paddle.stop()

    # -------- COLLISIONS --------
    def check_collisions(self):

        # top/bottom wall
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.height:
            self.ball.bounce_wall()

        # paddle hits
        if self.ball.rect.colliderect(self.left_paddle.rect) or \
           self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.bounce_paddle()

        # scoring RIGHT player (ball left side out)
        if self.ball.rect.left <= 0:
            self.score.add_right()
            self.ball.reset(self.width, self.height)

        # scoring LEFT player (ball right side out)
        elif self.ball.rect.right >= self.width:
            self.score.add_left()
            self.ball.reset(self.width, self.height)

        # win condition
        if self.score.left >= self.winning_score:
            self.game_over = True
            self.winner = "Player 1"

        elif self.score.right >= self.winning_score:
            self.game_over = True
            self.winner = "Player 2"

    # -------- UPDATE --------
    def update(self):
        self.left_paddle.update(self.height)
        self.right_paddle.update(self.height)
        self.ball.move()
        self.check_collisions()

    # -------- DRAW --------
    def draw(self):
        self.screen.fill((0, 0, 0))

        pygame.draw.rect(self.screen, (255, 255, 255), self.left_paddle.rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.right_paddle.rect)
        pygame.draw.ellipse(self.screen, (255, 255, 255), self.ball.rect)

        self.score.draw(self.screen, self.width)

        # instructions
        font = pygame.font.Font(None, 28)
        instructions = font.render(
            "W/S | Up/Down | First to 5 wins | R to restart",
            True,
            (255, 255, 255)
        )
        self.screen.blit(instructions, (40, self.height - 40))

        # winner text
        if self.game_over:
            big_font = pygame.font.Font(None, 60)
            win_text = big_font.render(f"{self.winner} Wins!", True, (255, 255, 255))
            self.screen.blit(
                win_text,
                (self.width // 2 - 140, self.height // 2 - 30)
            )

        pygame.display.flip()

    # -------- RUN LOOP --------
    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # restart
                if self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()

            if not self.game_over:
                self.handle_input()
                self.update()

            self.draw()
            self.clock.tick(60)


# ---------------- START ----------------
if __name__ == "__main__":
    Game().run()