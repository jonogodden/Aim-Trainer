import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Aim Trainer')

# Load outer space background
background = pygame.image.load('outer_space.jpg').convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load background music and play
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # -1 to loop indefinitely

# Load click sound effect
click_sound = pygame.mixer.Sound('click_sound.mp3')

# Circle properties
circle_max_radius = 50
circle_growth_rate = 0.001  # Adjusted growth rate here
circle_x, circle_y = screen_width // 2, screen_height // 2
circle_radius = 0  # Initial radius
circle_growing = False  # Initially not growing
circle_grow_time = 2000  # 2 seconds in milliseconds
circle_last_grow_time = 0
circle_disappear_time = 2000  # 2 seconds in milliseconds
circle_last_disappear_time = 0
show_start_button = True

# Scoring
score = 0
current_points = 1000

# Function to generate new random circle position
def generate_random_position():
    new_x = random.randint(circle_max_radius, screen_width - circle_max_radius)
    new_y = random.randint(circle_max_radius, screen_height - circle_max_radius)
    return new_x, new_y

# Function to draw the start button
def draw_start_button():
    button_rect = pygame.Rect(screen_width // 2 - 50, screen_height // 2 - 25, 100, 50)
    pygame.draw.rect(screen, (0, 0, 0), button_rect)  # Black start button
    font = pygame.font.Font(None, 36)
    text = font.render("Start", True, (255, 255, 255))  # White text
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

# Function to draw score
def draw_score():
    font = pygame.font.Font(None, 24)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
    screen.blit(score_text, (10, 10))

# Main loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    elapsed_grow_time = current_time - circle_last_grow_time
    elapsed_disappear_time = current_time - circle_last_disappear_time

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if start button is clicked
            if show_start_button:
                button_rect = pygame.Rect(screen_width // 2 - 50, screen_height // 2 - 25, 100, 50)
                if button_rect.collidepoint(event.pos):
                    show_start_button = False
                    circle_x, circle_y = generate_random_position()
                    circle_growing = True
                    circle_last_grow_time = current_time
                    circle_last_disappear_time = current_time
                    current_points = 1000  # Reset points when a new circle appears
            elif circle_growing:
                # Check if mouse click is within the bounds of the circle
                mouse_x, mouse_y = event.pos
                distance = ((circle_x - mouse_x)**2 + (circle_y - mouse_y)**2)**0.5
                if distance <= circle_radius:
                    # Calculate points based on current_points
                    score += current_points

                    # Play click sound effect
                    click_sound.play()

                    circle_growing = False
                    circle_radius = 0
                    circle_x, circle_y = generate_random_position()
                    circle_last_grow_time = current_time
                    circle_last_disappear_time = current_time
                    circle_growing = True  # Start new circle immediately

                elif distance >= circle_radius:

                    score -= 1

    # Draw background first
    screen.blit(background, (0, 0))

    # Draw start button if game hasn't started yet
    if show_start_button:
        draw_start_button()

    # Update circle size if it's growing
    if circle_growing:
        if elapsed_grow_time < circle_grow_time:
            # Calculate current radius based on elapsed time and growth rate
            circle_radius += circle_max_radius * circle_growth_rate

            # Add or subtract points based on how long it takes to click the target

            if 0<= elapsed_grow_time <=700: 
                current_points = 1
            elif 701<= elapsed_grow_time <=2000:
                current_points = -1
            

            # Draw concentric circle (bullseye effect)
            if 0<= elapsed_grow_time <=700: 
                pygame.draw.circle(screen, (0, 255, 0), (circle_x, circle_y), int(circle_radius), 3)
            elif 701<= elapsed_grow_time <=2000:
                pygame.draw.circle(screen, (255, 0, 0), (circle_x, circle_y), int(circle_radius), 3)
       

        elif elapsed_disappear_time >= circle_disappear_time:
            score -= 1
            circle_growing = False
            circle_radius = 0
            circle_x, circle_y = generate_random_position()
            circle_last_grow_time = current_time
            circle_last_disappear_time = current_time
            circle_growing = True  # Start new circle immediately
        

    # Draw score
    draw_score()

    # Update the display
    pygame.display.flip()

# Stop background music and quit Pygame
pygame.mixer.music.stop()
pygame.quit()
sys.exit()
