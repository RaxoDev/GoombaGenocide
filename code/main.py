import pygame
import time  # For win timer
from Mario import Mario
from Controls import Controls
from EntityCollider import EntityCollider
from Camera import Camera
from Draw import Draw
from Level import Level

# === Initialization ===
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 384, 516
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GoombaGenocide - Mario Clone")
clock = pygame.time.Clock()
fps = 60
pygame.font.init()
font = pygame.font.SysFont("Arial", 28)  # Smaller font

# === Game State Variables ===
def initialize_game():
    level = Level("level2.tmx")
    spawn_x, spawn_y = level.get_spawn_point()
    mario = Mario(spawn_x, spawn_y)
    controls = Controls(mario)
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, 2300)  # Adjust if your level width changes
    collider = EntityCollider(mario)
    draw = Draw(screen, camera)
    platforms = level.platforms
    return mario, level, controls, camera, collider, draw, platforms

mario, level, controls, camera, collider, draw, platforms = initialize_game()
game_won = False
win_timer_start = None
game_start_time = time.time()  # Start the game timer
final_time = None  # Will store final time when game is won

# === Game Loop ===
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_won:
        # Check if 5 seconds have passed
        if time.time() - win_timer_start >= 5:
            # Restart the game
            mario, level, controls, camera, collider, draw, platforms = initialize_game()
            game_won = False
            win_timer_start = None
            game_start_time = time.time()  # Reset timer
            final_time = None
        else:
            # Display "YOU WIN!" screen
            screen.fill((230, 230, 230))  # Light gray background
            win_text = font.render("YOU WIN!", True, (0, 0, 0))  # Black text
            screen.blit(win_text, (screen.get_width() // 2 - win_text.get_width() // 2, screen.get_height() // 2))

            # Show final elapsed time below win text
            timer_text = font.render(f"Time: {final_time}s", True, (0, 0, 0))
            screen.blit(timer_text, (screen.get_width() // 2 - timer_text.get_width() // 2, screen.get_height() // 2 + 40))

            pygame.display.flip()
            clock.tick(fps)
            continue  # Skip game logic until win screen is done

    # Input
    keys = pygame.key.get_pressed() 
    controls.handle_inputs(keys)

    # Update game objects
    mario.update(platforms, collider, controls)
    camera.update(mario)

    # Draw game
    screen.fill((230, 230, 230))  # Light gray background
    level.draw_map(screen, camera)
    mario.draw(screen, camera.apply(mario.rect)) 

    # Show timer (live during gameplay, frozen after win)
    elapsed_time = final_time if game_won else int(time.time() - game_start_time)
    timer_text = font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))  # Black text
    screen.blit(timer_text, (10, 10))

    # Win condition check (adjust bounds as needed)
    mario_x = mario.rect.centerx
    mario_y = mario.rect.centery
    if 64 < mario_x < 80 and mario_y == 144 and not game_won:
        game_won = True
        win_timer_start = time.time()
        final_time = int(win_timer_start - game_start_time)  # Freeze the timer when winning

    # Frame update
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
