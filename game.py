import pygame
from random import randint, uniform
from math import radians, cos, sin
from config import WIDTH, HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT


def reset_positions():
    """
    Reset player and ball positions and ball velocity.
    Ball velocity is random in angle and speed.
    """
    p1_rect = pygame.Rect(100, 450, PLAYER_WIDTH, PLAYER_HEIGHT)
    p2_rect = pygame.Rect(800, 450, PLAYER_WIDTH, PLAYER_HEIGHT)
    ball_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 64, 64)

    angle_deg = uniform(-45, 45) 
    if randint(0, 1):
        angle_deg += 180 

    speed = uniform(8, 15)
    angle_rad = radians(angle_deg)
    vx = speed * cos(angle_rad)
    vy = speed * sin(angle_rad)

    ball_vel = [vx, vy]

    start_ticks = pygame.time.get_ticks()
    return p1_rect, p2_rect, ball_rect, ball_vel, start_ticks

def move_players(keys, p1_rect, p2_rect, player_speed):
    """Update player positions based on key presses with boundary checking."""
    if keys[pygame.K_w] and p1_rect.top > 0:
        p1_rect.y -= player_speed
    if keys[pygame.K_s] and p1_rect.bottom < HEIGHT:
        p1_rect.y += player_speed
    if keys[pygame.K_UP] and p2_rect.top > 0:
        p2_rect.y -= player_speed
    if keys[pygame.K_DOWN] and p2_rect.bottom < HEIGHT:
        p2_rect.y += player_speed

def update_ball(ball_rect, ball_vel, p1_rect, p2_rect):
    """
    Move the ball and check collisions with players and screen edges.
    Returns updated ball velocity and any goal scored (0 for player1, 1 for player2, None if no goal).
    """
    ball_rect.x += ball_vel[0]
    ball_rect.y += ball_vel[1]

    # Bounce off top and bottom edges
    if ball_rect.top <= 0:
        ball_rect.top = 0
        ball_vel[1] = abs(ball_vel[1])
    elif ball_rect.bottom >= HEIGHT:
        ball_rect.bottom = HEIGHT
        ball_vel[1] = -abs(ball_vel[1]) 

    # Bounce off player 1
    if ball_rect.colliderect(p1_rect) and ball_vel[0] < 0:
        ball_vel[0] = abs(ball_vel[0])  

        offset = (ball_rect.centery - p1_rect.centery) / (p1_rect.height / 2)
        ball_vel[1] = offset * 8 

    # Bounce off player 2
    if ball_rect.colliderect(p2_rect) and ball_vel[0] > 0:
        ball_vel[0] = -abs(ball_vel[0]) 

        offset = (ball_rect.centery - p2_rect.centery) / (p2_rect.height / 2)
        ball_vel[1] = offset * 8

    # Check for goals
    if ball_rect.right < 0:
        return ball_vel, 1
    elif ball_rect.left > WIDTH:
        return ball_vel, 0

    return ball_vel, None
