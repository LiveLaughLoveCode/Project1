import pygame
import sys
from Items import Item  # Import the Item class from Items.py
from Enemy import Enemy  # Import the Enemy class from Enemy.py

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1600, 900
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load the background image
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale the image to fit the window

# Set up the player
player_size = 50
player_pos = [WIDTH // 2, HEIGHT // 2]

# Initialize the items
items = [Item() for _ in range(10)]  # Creates 10 items

# Initialize the score and high score
score = 0
high_score = 0

def draw_player(pos):
    pygame.draw.circle(screen, RED, pos, player_size)

def handle_movement(keys, pos):
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        pos[1] -= 0.5
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        pos[1] += 0.5
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        pos[0] -= 0.5
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        pos[0] += 0.5

    # Check if the circle has moved off the edge of the screen
    if pos[0] < 0:
        pos[0] = WIDTH
    elif pos[0] > WIDTH:
        pos[0] = 0
    if pos[1] < 0:
        pos[1] = HEIGHT
    elif pos[1] > HEIGHT:
        pos[1] = 0

    return pos

def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def show_start_screen(items):
    screen.fill(GREEN)
    draw_text('Welcome to the Game!', 64, BLACK, WIDTH / 2, HEIGHT / 4)
    draw_text('Press any key to start', 22, BLACK, WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()
    wait_for_key()
    items[:] = [Item() for _ in range(10)]  # Regenerate the items here

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Change this line
                waiting = False

def game_loop(items, player_pos):
    global high_score  # Make sure to use the global high_score variable

    # Initialize the score
    score = 0

    # Initialize the enemy
    enemy = None

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Blit the background image onto the screen
        screen.blit(background, (0, 0))

        # If all items are collected, generate a new set
        if not items:
            pygame.time.wait(500)  # Wait for 500 milliseconds
            items = [Item() for _ in range(10)]

        # Create an enemy if it doesn't exist
        if enemy is None:
            enemy = Enemy(player_pos)

        # Handle player movement and draw the player
        player_pos = handle_movement(pygame.key.get_pressed(), player_pos)
        draw_player(player_pos)

        # Check for collisions and draw the items
        for item in items[:]:  # Iterate over a copy of the list
            if item.collides_with(player_pos, player_size):
                items.remove(item)  # Remove the item from the list
                score += 1  # Increment the score each time a circle is collected
                if score > high_score:  # If the current score is higher than the high score
                    high_score = score  # Update the high score

        # Draw the items
        for item in items:
            item.draw(screen)

        # Update and draw the enemy
        if enemy:
            enemy.update(player_pos)
            enemy.draw(screen)

            # Check for collision with the enemy
            if enemy.collides_with(player_pos, player_size):
                show_start_screen(items)  # Go back to the title screen
                return items, player_pos  # Exit the game loop

        # If all items are collected, generate a new set
        Item.regenerate_items(items)

        # Draw the score and high score
        draw_text(f'Score: {score}', 32, BLACK, 75, 10)  # Adjust the size and position as needed
        draw_text(f'High Score: {high_score}', 32, BLACK, 100, 50)  # Display the high score beneath the score

        pygame.display.flip()  # Update the display

    return items, player_pos  # Return the items list and player position at the end of the game loop

# Show the start screen
show_start_screen(items)

# Start the game loop
while True:  # Keep looping until the player decides to quit
    items, player_pos = game_loop(items, player_pos)