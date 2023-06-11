import pygame
import random

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

SCORE_FONT = pygame.font.SysFont("comicsans", 40)
WINNING_SCORE = 1


class Paddle:
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.original_x, self.original_y = x, y
        self.width, self.height = width, height

    def draw_paddle(self, win):
        pygame.draw.rect(
            win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, direction="up"):
        if direction == "up":
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

        # Prevent paddle from going off the screen
        if self.y < 0:
            self.y = 0

        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

    def reset(self):
        self.x, self.y = self.original_x, self.original_y


class Ball:
    COLOR = WHITE
    VELOCITY = 5

    def __init__(self, x, y, radius):
        self.x, self.y = x, y
        self.original_x, self.original_y = x, y
        self.radius = radius
        self.x_vel, self.y_vel = self.VELOCITY, 0

    def draw_ball(self, win):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x, self.y = self.original_x, self.original_y
        self.x_vel *= -1
        self.y_vel = 0


def draw_window(win, paddles, ball, left_score=0, right_score=0):
    win.fill(BLACK)  # Fill the window with black color

    # Draw the score
    left_score_text = SCORE_FONT.render(
        f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(
        f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2,
                               HEIGHT // 2 - left_score_text.get_height() // 2))

    win.blit(right_score_text, (WIDTH // 4 * 3 - right_score_text.get_width() // 2,
                                HEIGHT // 2 - right_score_text.get_height() // 2))

    for paddle in paddles:
        paddle.draw_paddle(win)

    # Draw the center line
    for i in range(10, HEIGHT, HEIGHT // 20):
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 5, HEIGHT // 40))

    ball.draw_ball(win)

    pygame.display.update()


def handle_collision(ball, left_paddle, right_paddle):
    # Check if ball has collided with the top or bottom of the screen
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # Check if ball has collided with the left or right paddle
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                diff_in_y = ball.y - middle_y
                reduction_factor = (left_paddle.height / 2) / ball.VELOCITY
                ball.y_vel = diff_in_y / reduction_factor
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                diff_in_y = ball.y - middle_y
                reduction_factor = (right_paddle.height / 2) / ball.VELOCITY
                ball.y_vel = diff_in_y / reduction_factor


def handle_paddle_movement(keys, left_paddle, right_paddle):
    # Move left paddle with W and S keys
    if keys[pygame.K_w]:
        left_paddle.move("up")
    if keys[pygame.K_s]:
        left_paddle.move("down")

    # Move right paddle with UP and DOWN arrow keys
    if keys[pygame.K_UP]:
        right_paddle.move("up")
    if keys[pygame.K_DOWN]:
        right_paddle.move("down")


def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH // 2, HEIGHT // 2, 10)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)
        draw_window(WIN, [left_paddle, right_paddle],
                    ball, left_score, right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Check if ball has gone off the screen
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
        won = False
        # Check if either player has won
        if left_score == WINNING_SCORE:
            won = True
        elif right_score == WINNING_SCORE:
            won = True

        if won:
            win_text = SCORE_FONT.render(
                f"Player {1 if left_score == WINNING_SCORE else 2} won!", 1, WHITE)
            WIN.blit(win_text, (WIDTH // 2 - win_text.get_width() //
                                2, HEIGHT // 2 - win_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)

            left_paddle.reset()
            right_paddle.reset()
            ball.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == "__main__":
    main()
