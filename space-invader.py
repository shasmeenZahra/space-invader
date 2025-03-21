import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player
player_img = pygame.Surface((50, 30))  # Creating player rectangle
player_img.fill(GREEN)  # Filling player with green color
player_x = WIDTH // 2 - 25  # Initial X position of player
player_y = HEIGHT - 60  # Initial Y position of player
player_speed = 5  # Speed of player movement

# Enemies
enemy_img = pygame.Surface((40, 40))  # Creating enemy rectangle
enemy_img.fill(RED)  # Filling enemy with red color
enemy_x = []  # List to store enemy X positions
enemy_y = []  # List to store enemy Y positions
enemy_speed_x = []  # List to store enemy X speed
enemy_speed_y = 20  # Speed of enemy movement in Y direction
num_of_enemies = 8  # Number of enemies

# Initializing enemy positions
for i in range(num_of_enemies):
    enemy_x.append(random.randint(0, WIDTH - 40))  # Random X position
    enemy_y.append(random.randint(50, 150))  # Random Y position
    enemy_speed_x.append(2)  # Initial X speed of enemy

# Bullet
bullet_img = pygame.Surface((5, 15))  # Creating bullet rectangle
bullet_img.fill(WHITE)  # Filling bullet with white color
bullet_x = 0  # Initial bullet X position
bullet_y = HEIGHT - 60  # Initial bullet Y position
bullet_speed = 10  # Speed of bullet movement
bullet_state = "ready"  # Bullet state (ready to fire or moving)

# Score
score = 0  # Initial score
font = pygame.font.Font(None, 36)  # Font for displaying score

# Game over text
game_over_font = pygame.font.Font(None, 80)  # Font for game over text
game_over = False  # Game over flag

# Function to draw the player
def player_draw(x, y):
    screen.blit(player_img, (x, y))

# Function to draw an enemy
def enemy_draw(x, y):
    screen.blit(enemy_img, (x, y))

# Function to fire a bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 22, y))

# Function to check for collision between bullet and enemy
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance_x = abs(enemy_x - bullet_x)
    distance_y = abs(enemy_y - bullet_y)
    return distance_x < 40 and distance_y < 40

# Function to display score on screen
def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to display game over text
def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, WHITE)
    screen.blit(over_text, (WIDTH//2 - 200, HEIGHT//2 - 40))

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)  # Fill screen with black color
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Quit game loop
            
        # Keypress controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed  # Move player left
            if event.key == pygame.K_RIGHT:
                player_x_change = player_speed  # Move player right
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x  # Set bullet position to player position
                fire_bullet(bullet_x, bullet_y)  # Fire bullet
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0  # Stop player movement
    
    # Player movement
    player_x += player_x_change if 'player_x_change' in locals() else 0
    
    # Boundaries
    if player_x <= 0:
        player_x = 0
    elif player_x >= WIDTH - 50:
        player_x = WIDTH - 50
        
    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over Condition
        if enemy_y[i] > HEIGHT - 120:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000  # Move enemies off screen
            game_over = True
            break
            
        enemy_x[i] += enemy_speed_x[i]  # Move enemy in X direction
        
        if enemy_x[i] <= 0:
            enemy_speed_x[i] = 2
            enemy_y[i] += enemy_speed_y
        elif enemy_x[i] >= WIDTH - 40:
            enemy_speed_x[i] = -2
            enemy_y[i] += enemy_speed_y
            
        # Collision Detection
        if bullet_state == "fire" and is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = HEIGHT - 60  # Reset bullet position
            bullet_state = "ready"  # Reset bullet state
            score += 1  # Increase score
            enemy_x[i] = random.randint(0, WIDTH - 40)  # Reset enemy position
            enemy_y[i] = random.randint(50, 150)
            
        enemy_draw(enemy_x[i], enemy_y[i])  # Draw enemy
        
    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = HEIGHT - 60
        bullet_state = "ready"
        
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed  # Move bullet upwards
    
    # Draw player
    player_draw(player_x, player_y)
    
    # Show score
    show_score()
    
    # Game over display
    if game_over:
        game_over_text()
    
    pygame.display.update()  # Update screen
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
sys.exit()
