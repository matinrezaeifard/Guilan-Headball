import pygame
import sys
from config import WIDTH, HEIGHT, FPS, WHITE
from assets import load_image, load_players_with_names
from ui import draw_text, player_selection_menu, draw_score_and_timer, pause_menu, game_over_screen
from game import reset_positions, move_players, update_ball

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guilan Headball")
clock = pygame.time.Clock()

# Load assets once
background = load_image("assets/background.png")
sb_img = load_image("assets/scoreboard.png")
player1_list = load_players_with_names("p1")
player2_list = load_players_with_names("p2")
ball_img = load_image("assets/ball.png")

def main():
    # Player selection screen returns chosen player indices
    player1_index, player2_index = player_selection_menu(screen, clock, background, player1_list, player2_list)

    # Initialize game variables
    score = [0, 0]
    p1_rect, p2_rect, ball_rect, ball_vel, start_ticks = reset_positions()
    player_speed = 20

    running = True
    paused = False
    game_over = False

    while running:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.WINDOWCLOSE: 
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused

                if event.key == pygame.K_r and not paused:
                    score = [0, 0]
                    p1_rect, p2_rect, ball_rect, ball_vel, start_ticks = reset_positions()

        if not paused and not game_over:
            keys = pygame.key.get_pressed()
            move_players(keys, p1_rect, p2_rect, player_speed)

            ball_vel, goal = update_ball(ball_rect, ball_vel, p1_rect, p2_rect)
            if goal is not None:
                score[goal] += 1
                tmp = start_ticks
                p1_rect, p2_rect, ball_rect, ball_vel, start_ticks = reset_positions()
                start_ticks = tmp

            # Check win condition
            if (score[0] == 1 or score[1] == 1):
                game_over = True

            # Check time left
            seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
            time_left = max(0, 180 - seconds_passed)
            if time_left <= 0:
                game_over = True
        else:
            time_left = 0  # If paused or game over, freeze timer

        sb_rect = pygame.Rect((WIDTH // 2) - 190, 25, 380, 55)
        screen.blit(sb_img, sb_rect)
        draw_score_and_timer(screen, score, time_left, player1_list[player1_index]["name"], player2_list[player2_index]["name"])

        # Draw players and ball
        screen.blit(player1_list[player1_index]["image"], p1_rect)
        screen.blit(player2_list[player2_index]["image"], p2_rect)
        screen.blit(ball_img, ball_rect)

        if paused:
            pause_start = pygame.time.get_ticks()
            action = pause_menu(screen, clock, background)
            if action == "restart":
                score = [0, 0]
                p1_rect, p2_rect, ball_rect, ball_vel, start_ticks = reset_positions()
                paused = False
            elif action == "main_menu":
                main()
                return
            elif action == "resume": 
                paused = False
                pause_duration = pygame.time.get_ticks() - pause_start 
                start_ticks += pause_duration

        if game_over:
            game_over_screen(screen, clock, score, player1_list[player1_index]["name"], player2_list[player2_index]["name"])
            main()
            return

        pygame.display.flip()

if __name__ == "__main__":
    main()
