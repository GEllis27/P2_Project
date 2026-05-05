import pygame, sys, random
# This initializes all pygame modules (display, sound, fonts, etc.)
pygame.init()
#Dimensions of the game window
WIDTH, HEIGHT = 600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong!")
CLOCK = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)
DIM = (80, 80, 80)


# ---------------- PADDLE ----------------
class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed      # How many pixels the paddle moves per frame
        self.velocity = 0       # Current movement direction

        #This stores position and size, it also handles collision detection
        self.rect = pygame.Rect(x, y, width, height)

    def move_up(self):
        self.velocity = -self.speed
    # Set velocity to negative so the paddle moves toward the top of the screen
    def move_down(self):
        self.velocity = self.speed
    # Positive velocity moves the paddle toward the bottom
    def stop(self):
        self.velocity = 0
    # Called when no movement key is held; paddle stays in place
    def update(self, screen_height):
        self.rect.y += self.velocity
        self.rect.y = max(0, min(self.rect.y, screen_height - self.height))


# ---------------- BALL ----------------
class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.horizontal_velo = random.choice([-4, 4]) #Randomly picks a horizontal and vertical direction
        self.vertical_velo = random.choice([-4, 4])

    def move(self):
        self.rect.x += self.horizontal_velo
        self.rect.y += self.vertical_velo

    def bounce_wall(self):
        self.vertical_velo *= -1 #reverse velo when ball hits wall

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
        self.label_font = pygame.font.Font(None, 28)
        self.number_font = pygame.font.Font(None, 56)

    def draw(self, screen, width):
        #left side, Player 1
        p1_label = self.label_font.render("P1", True, GRAY)
        p1_score = self.number_font.render(str(self.left), True, WHITE)

        p1_x = width // 4
        screen.blit(p1_label, (p1_x - p1_label.get_width() // 2, 14))
        screen.blit(p1_score, (p1_x - p1_score.get_width() // 2, 36))

        pygame.draw.line(screen, DIM, (width // 2, 10), (width // 2, 90), 2)

        #right side, Player 2
        p2_label = self.label_font.render("P2", True, GRAY)
        p2_score = self.number_font.render(str(self.right), True, WHITE)

        p2_x = width * 3 // 4
        screen.blit(p2_label, (p2_x - p2_label.get_width() // 2, 14))
        screen.blit(p2_score, (p2_x - p2_score.get_width() // 2, 36))

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
        self.waiting = True
        self.scored = False

        #Initialize countdown and countdown_end so they always exist
        self.countdown = 0
        self.countdown_end = 0

        #Fonts reused across frames
        self._instr_font = pygame.font.Font(None, 26)
        self._big_font = pygame.font.Font(None, 64)
        self._sub_font = pygame.font.Font(None, 34)

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

        # Reposition ball to paddle edge before bouncing to prevent
        # clipping/tunneling through the paddle at high speed
        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.rect.left = self.left_paddle.rect.right
            self.ball.bounce_paddle()
        elif self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.rect.right = self.right_paddle.rect.left
            self.ball.bounce_paddle()

        # scoring RIGHT player (ball left side out)
        if self.ball.rect.left <= 0:
            self.score.add_right()
            self.ball.reset(self.width, self.height)
            self.scored = True   #flag that a point was just scored

        # scoring LEFT player (ball right side out)
        elif self.ball.rect.right >= self.width:
            self.score.add_left()
            self.ball.reset(self.width, self.height)
            self.scored = True   #flag that a point was just scored

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

    # -------- DRAW HELPERS --------
    def _draw_instructions(self):
        controls = [
            ("P1",  "W / S"),
            ("P2",  "↑ / ↓"),
            ("Win", "First to 5"),
        ]

        box_w, box_h = 120, 44
        gap = 14
        total_w = len(controls) * box_w + (len(controls) - 1) * gap
        start_x = (self.width - total_w) // 2
        y = self.height - 68

        key_font = pygame.font.Font(None, 22)
        label_font = pygame.font.Font(None, 19)

        for i, (label, keys_str) in enumerate(controls):
            x = start_x + i * (box_w + gap)

            surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            pygame.draw.rect(surf, (255, 255, 255, 18), (0, 0, box_w, box_h), border_radius=6)
            pygame.draw.rect(surf, (255, 255, 255, 50), (0, 0, box_w, box_h), width=1, border_radius=6)
            self.screen.blit(surf, (x, y))

            lbl  = label_font.render(label, True, GRAY)
            keys = key_font.render(keys_str, True, WHITE)
            self.screen.blit(lbl,  (x + box_w // 2 - lbl.get_width()  // 2, y + 6))
            self.screen.blit(keys, (x + box_w // 2 - keys.get_width() // 2, y + 22))

    def _draw_game_over(self):
        #Semi-transparent dark overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Winner banner
        win_text = self._big_font.render(f"{self.winner} Wins!", True, WHITE)
        self.screen.blit(
            win_text,
            (self.width // 2 - win_text.get_width() // 2,
             self.height // 2 - 60)
        )

        pulse  = int(180 + 75 * abs(__import__('math').sin(pygame.time.get_ticks() / 400)))
        prompt = self._sub_font.render("Press  R  to play again", True, (pulse, pulse, pulse))
        self.screen.blit(
            prompt,
            (self.width // 2 - prompt.get_width() // 2,
             self.height // 2 + 20)
        )


    # -------- DRAW --------
    def draw(self):
        self.screen.fill(BLACK)

        #Centre dashed dividing line (cosmetic)
        for y in range(100, self.height - 80, 18):
            pygame.draw.rect(self.screen, DIM, (self.width // 2 - 1, y, 2, 10))

        pygame.draw.rect(self.screen, WHITE, self.left_paddle.rect)
        pygame.draw.rect(self.screen, WHITE, self.right_paddle.rect)
        pygame.draw.ellipse(self.screen, WHITE, self.ball.rect)

        self.score.draw(self.screen, self.width)
        self._draw_instructions()

        if self.game_over:
            self._draw_game_over()
        elif self.waiting:
            pulse  = int(180 + 75 * abs(__import__('math').sin(pygame.time.get_ticks() / 400)))
            prompt = self._sub_font.render("Press any move key to serve", True, (pulse, pulse, pulse))
            self.screen.blit(prompt, (self.width // 2 - prompt.get_width() // 2, self.height // 2 + 24))

        pygame.display.flip()

    # -------- RUN LOOP --------
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Restart only accepted after game over — player must press R intentionally
                if self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()

            if not self.game_over:
                if self.scored:
                    # A point just landed — start countdown immediately
                    self.scored = False
                    self.waiting = False
                    self.countdown = 3
                    self.countdown_end = pygame.time.get_ticks() + 3000
                elif self.waiting:
                    # Start of game / after restart — wait for a key press first
                    keys = pygame.key.get_pressed()
                    if any([keys[pygame.K_w], keys[pygame.K_s],
                            keys[pygame.K_UP], keys[pygame.K_DOWN]]):
                        self.waiting = False
                        self.countdown = 3
                        self.countdown_end = pygame.time.get_ticks() + 3000
                elif self.countdown > 0:
                    # Countdown running — paddles move, ball stays put
                    self.handle_input()
                    self.left_paddle.update(self.height)
                    self.right_paddle.update(self.height)
                    now = pygame.time.get_ticks()
                    self.countdown = max(0, (self.countdown_end - now + 999) // 1000)
                else:
                    self.handle_input()
                    self.update()

            self.draw()
            self.clock.tick(60)

# ---------------- START ----------------
if __name__ == "__main__":
    Game().run()