import pygame
import random
import tkinter as tk
from tkinter import simpledialog

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
font = pygame.font.Font(None, 36)

# Get player names using a GUI
root = tk.Tk()
root.withdraw()  # Hide the root window
player1_name = simpledialog.askstring("Player 1", "Enter Player 1 name:")
player2_name = simpledialog.askstring("Player 2", "Enter Player 2 name:")

# Class for paddles
class Paddle(pygame.Rect):
    def __init__(self, x, y, name):
        super().__init__(x, y, 20, 100)
        self.velocity = 0
        self.score = 0
        self.name = name

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
        if self.left <= 0:
            self.__init__()
            player2.score += 1
        elif self.right >= WIDTH:
            self.__init__()
            player1.score += 1

# Create players and ball
player1 = Paddle(50, HEIGHT // 2 - 50, player1_name)
player2 = Paddle(WIDTH - 70, HEIGHT // 2 - 50, player2_name)
ball = Ball()

# Game state
start = False
paused = False

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True
            if event.key == pygame.K_p:  # Pause/Unpause
                paused = not paused
            if start and not paused:
                if event.key == pygame.K_w:
                    player1.velocity = -PADDLE_SPEED
                elif event.key == pygame.K_s:
                    player1.velocity = PADDLE_SPEED
                elif event.key == pygame.K_UP:
                    player2.velocity = -PADDLE_SPEED
                elif event.key == pygame.K_DOWN:
                    player2.velocity = PADDLE_SPEED
                elif event.key == pygame.K_r:  # Reset scores
                    player1.score = 0
                    player2.score = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1.velocity = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2.velocity = 0

    if start and not paused:
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

    # Draw scores
    player1_text = font.render(f"{player1.name}: {player1.score}", True, WHITE)
    player2_text = font.render(f"{player2.name}: {player2.score}", True, WHITE)
    screen.blit(player1_text, (10, 10))
    screen.blit(player2_text, (WIDTH - player2_text.get_width() - 10, 10))

    # Draw start message
    if not start:
        start_text = font.render("Press Space to Start", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))

    # Draw pause message
    if paused:
        pause_text = font.render("Paused (Press P to Unpause)", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

    # Separate area for scores
    score_area = pygame.Rect(WIDTH // 2 - 100, 10, 200, 50)
    pygame.draw.rect(screen, (128, 128, 128), score_area, 2)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
