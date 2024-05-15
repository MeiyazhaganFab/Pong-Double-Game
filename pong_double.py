import pygame
import random

# Configurations
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 5
PADDLE_SPEED = 7
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Double")

# Class for paddles 
class Paddle(pygame.Rect):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 100)
        self.velocity = 0

    def move(self):
        self.y += self.velocity

        # Prevent paddles from going out of screen
        if self.top <= 0:
            self.top = 0
        elif self.bottom >= HEIGHT:
            self.bottom = HEIGHT

# Class for Ball
class Ball(pygame.Rect):
    def __init__(self):
        super().__init__(WIDTH // 2, HEIGHT // 2, 20, 20)
        self.velocity_x = random.choice((BALL_SPEED, -BALL_SPEED))
        self.velocity_y = random.choice((BALL_SPEED, -BALL_SPEED))

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top and bottom
        if self.top <= 0 or self.bottom >= HEIGHT:
            self.velocity_y *= -1

        # Reset position if ball goes out of bounds
        if self.left <= 0 or self.right >= WIDTH:
            self.__init__()

# Create players and ball
player1 = Paddle(50, HEIGHT // 2 - 50)
player2 = Paddle(WIDTH - 70, HEIGHT // 2 - 50)
ball = Ball()

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1.velocity = -PADDLE_SPEED
            elif event.key == pygame.K_s:
                player1.velocity = PADDLE_SPEED
            elif event.key == pygame.K_UP:
                player2.velocity = -PADDLE_SPEED
            elif event.key == pygame.K_DOWN:
                player2.velocity = PADDLE_SPEED
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1.velocity = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2.velocity = 0

    # Move paddles and ball
    player1.move()
    player2.move()
    ball.move()

    # Check collision with paddles
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball.velocity_x *= -1

    # Clear the screen
    screen.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
