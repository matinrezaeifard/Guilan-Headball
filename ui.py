import pygame, sys
from config import WIDTH, HEIGHT, BLACK, RED, WHITE
from assets import load_image, load_players_with_names

pygame.font.init()

# Fonts♦
FONT = pygame.font.SysFont("Calibri", 40)
SB_FONT = pygame.font.SysFont("Calibri", 26, bold=True)
_22_BOLD_FONT = pygame.font.SysFont("Calibri", 22, bold=True)
_26_BOLD_FONT = pygame.font.SysFont("Calibri", 26, bold=True)
_32_BOLD_FONT = pygame.font.SysFont("Calibri", 32, bold=True)
BIG_FONT = pygame.font.SysFont("Calibri", 50, bold=True)

def draw_text(screen, text, font, color, center):
    """Render text on the screen centered at 'center' coordinates."""
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=center)
    screen.blit(surf, rect)

def player_selection_menu(screen, clock, background, player1_list, player2_list):
    """
    Show player selection screen allowing users to scroll and pick players.
    Controls:
    Player 1: A/D keys
    Player 2: Left/Right arrows
    Space to confirm
    """

    # Load Assets
    el_001 = load_image("assets/menu/el_001.png")

    player1_index, player2_index = 0, 0
    selecting_players = True

    while selecting_players:
        clock.tick(60)
        screen.blit(background, (0, 0))

        draw_text(screen, "MAIN MENU", BIG_FONT, BLACK, (WIDTH // 2, 50))


        # Draw player 1
        screen.blit(el_001, ((WIDTH // 4 - 137.5), 100))
        draw_text(screen, "Player 1", _26_BOLD_FONT, WHITE, (WIDTH // 4, 150))
        p1_img = player1_list[player1_index]["image"]
        p1_name = player1_list[player1_index]["name"]
        screen.blit(p1_img, (WIDTH // 4 - p1_img.get_width() // 2, 225))
        draw_text(screen, p1_name, _32_BOLD_FONT, WHITE, (WIDTH // 4, 400))
        draw_text(screen, "A/D to scroll", _22_BOLD_FONT, WHITE, (WIDTH // 4, 425))

        # Draw player 2
        screen.blit(el_001, ((3 * WIDTH // 4 - 137.5), 100))
        draw_text(screen, "Player 2", _26_BOLD_FONT, WHITE, (3 * WIDTH // 4, 150))
        p2_img = player2_list[player2_index]["image"]
        p2_name = player2_list[player2_index]["name"]
        screen.blit(p2_img, (3 * WIDTH // 4 - p2_img.get_width() // 2, 225))
        draw_text(screen, p2_name, _32_BOLD_FONT, WHITE, (3 * WIDTH // 4, 400))
        draw_text(screen, "←/→ to scroll", _22_BOLD_FONT, WHITE, (3 * WIDTH // 4, 425))

        draw_text(screen, "Press SPACE to Start", _32_BOLD_FONT, RED, (WIDTH // 2, 600))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.WINDOWCLOSE: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player1_index = (player1_index - 1) % len(player1_list)
                elif event.key == pygame.K_d:
                    player1_index = (player1_index + 1) % len(player1_list)
                elif event.key == pygame.K_LEFT:
                    player2_index = (player2_index - 1) % len(player2_list)
                elif event.key == pygame.K_RIGHT:
                    player2_index = (player2_index + 1) % len(player2_list)
                elif event.key == pygame.K_SPACE:
                    selecting_players = False

        pygame.display.flip()

    return player1_index, player2_index

def draw_score_and_timer(screen, score, time_left, player1_name, player2_name):
    """Display current score and countdown timer."""
    p1_name_text = player1_name
    draw_text(screen, p1_name_text, SB_FONT, WHITE, ((WIDTH // 2) - 107.5, 47.5))
    p1_score_text = f'{score[0]}'
    draw_text(screen, p1_score_text, SB_FONT, WHITE, ((WIDTH // 2) - 12.5, 50))

    p2_name_text = player2_name
    draw_text(screen, p2_name_text, SB_FONT, WHITE, ((WIDTH // 2) + 107.5, 47.5))
    p2_score_text = f'{score[1]}'
    draw_text(screen, p2_score_text, SB_FONT, WHITE, ((WIDTH // 2) + 12.5, 50))

    minutes = int(time_left) // 60
    seconds = int(time_left) % 60
    timer_text = f"{minutes}:{seconds:02d}"
    draw_text(screen, timer_text, SB_FONT, WHITE, (WIDTH // 2, 87.5))

def pause_menu(screen, clock, background):
    """Show pause menu with options and return selected action."""
    # Load Assets
    el_002 = load_image("assets/menu/el_002.png")

    options = ["Resume", "Restart", "Main Menu"]
    selected = 0
    paused = True

    while paused:
        clock.tick(60)
        screen.blit(background, (0, 0))
        screen.blit(el_002, ((WIDTH // 2 - 175), 100))
        draw_text(screen, "Game Paused", BIG_FONT, RED, (WIDTH // 2, HEIGHT // 2 - 150))

        for i, option in enumerate(options):
            color = RED if i == selected else BLACK
            draw_text(screen, option, FONT, color, (WIDTH // 2, HEIGHT // 2 - 20 + i * 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.WINDOWCLOSE: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected].lower().replace(" ", "_")

        pygame.display.flip()

def game_over_screen(screen, clock, score, player1_name, player2_name):
    """
    Display game over screen and wait for user to press Enter to return to main menu.
    """
    running = True

    # Load Assets
    el_003 = load_image("assets/menu/el_003.png")
    el_004 = load_image("assets/menu/el_004.png")
    w_name = player1_name
    l_name = player2_name
    bg = load_image("assets/no-draw.png")
    if score[0] > score[1]:
        result_text = f"{player1_name} Wins!"
    elif score[1] > score[0]:
        result_text = f"{player2_name} Wins!"
        w_name = player2_name
        l_name = player1_name
    else:
        result_text = "Draw!"
        bg = load_image("assets/draw.png")
    winners = load_players_with_names("p1")
    losers = load_players_with_names("p2")

    winner = None
    for w in winners:
        if w_name in w["name"]:
            winner = w["image"]
            break
    w_x = 400
    if "Dr. Amirian" in w_name:
        w_x = 405
    elif "Dr. Atari" in w_name:
        w_x = 398
    elif "Dr. Saheli" in w_name:
        w_x = 402
    elif "Dr. Ahadifar" in w_name:
        w_x = 403
    elif "Dr. Shekar v1" in w_name:
        w_x = 405
    elif "Dr. Shekar v2" in w_name:
        w_x = 408
    elif "Dr. Shekar v2" in w_name:
        l_x = 402
    elif "Dr. Mir" in w_name:
        w_x = 398
    
    loser = None
    for l in losers:
        if l_name in l["name"]:
            loser = l["image"]
            break
    l_x = 528
    if "Dr. Amirian" in l_name:
        l_x = 530
    elif "Dr. Atari" in l_name:
        l_x = 520
    elif "Dr. Ahadifar" in w_name:
        l_x = 532
    elif "Dr. Shekar v1" in w_name:
        l_x = 532
    elif "Dr. Shekar v2" in w_name:
        l_x = 534
    elif "Dr. Mir Happy" in w_name:
        l_x = 532
    elif "Dr. Mir" in w_name:
        l_x = 535
    elif "Dr. Zeyfi" in w_name:
        l_x = 525

    result = False

    while running:
        clock.tick(60)
        if winner is not None and loser is not None:
            screen.blit(bg, (0, 0))
            screen.blit(winner, (w_x, 180))
            screen.blit(loser, (l_x, 185))

        if result:
            screen.blit(el_003, ((WIDTH // 2) - 262.5, (HEIGHT // 2) - 100))
            p1_name_text = player1_name
            draw_text(screen, p1_name_text, _32_BOLD_FONT, WHITE, ((WIDTH // 2) - 135, (HEIGHT // 2) - 72.5)) # +27.5
            p1_score_text = f'{score[0]}'
            draw_text(screen, p1_score_text, _32_BOLD_FONT, WHITE, ((WIDTH // 2) - 15, (HEIGHT // 2) - 67.5)) # +32.5

            p2_name_text = player2_name
            draw_text(screen, p2_name_text, _32_BOLD_FONT, WHITE, ((WIDTH // 2) + 135, (HEIGHT // 2) - 72.5)) # +27.5
            p2_score_text = f'{score[1]}'
            draw_text(screen, p2_score_text, _32_BOLD_FONT, WHITE, ((WIDTH // 2) + 15, (HEIGHT // 2) - 67.5)) # +32.5

            draw_text(screen, result_text, BIG_FONT, WHITE, (WIDTH // 2, (HEIGHT // 2) + 10)) # +110
            draw_text(screen, "Press ENTER to continute", _26_BOLD_FONT, RED, (WIDTH // 2, (HEIGHT // 2) + 50)) # +150
        else:
            screen.blit(el_004, ((WIDTH // 2) - 200, 25))

            draw_text(screen, "Game Over", BIG_FONT, RED, (WIDTH // 2, 65))
            draw_text(screen, "Press ENTER to see results", _26_BOLD_FONT, RED, (WIDTH // 2, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.WINDOWCLOSE: 
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not result:
                        result = True
                    else:
                        running = False

        pygame.display.flip()