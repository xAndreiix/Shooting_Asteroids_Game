import pygame
import sys
import math
import random

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BACKGROUND_COLOR = (0, 0, 0)
SHIP_COLOR = (255, 255, 255)
BULLET_COLOR = (255, 192, 203)
ASTEROID_COLOR = (255, 165, 0)
SHIP_SIZE = 20
SHIP_SPEED = 0.2
BULLET_SIZE = 3
ASTEROID_SIZE = 40
BULLET_SPEED = 3
ASTEROID_SPEED = 0.1
MAX_ASTEROIDS = 5
SPAWN_RATE = 400
MAX_LIVES = 3
BULLET_FIRE_DELAY = 300
EXPLOSION_DURATION = 500
EXPLOSION_MAX_RADIUS = 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooting Asteroids")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

ship_x = SCREEN_WIDTH // 2
ship_y = SCREEN_HEIGHT // 2
ship_angle = 0
ship_exploded = False
lives = MAX_LIVES
points = 0
bullets = []
asteroids = []
game_over = False
explosion_start_time = 0

game_over_text = font.render("Game Over - Press R to Restart", True, (255, 255, 255))

def check_ship_asteroid_collisions(ship_x, ship_y, asteroids):
    asteroids_to_remove = []
    for asteroid in asteroids:
        asteroid_x, asteroid_y, _ = asteroid
        distance = math.hypot(ship_x - asteroid_x, ship_y - asteroid_y)
        if distance < ASTEROID_SIZE:
            asteroids_to_remove.append(asteroid)
    for asteroid in asteroids_to_remove:
        asteroids.remove(asteroid)
    return len(asteroids_to_remove) > 0

def spawn_asteroid():
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    edge = random.choice(["top", "bottom", "left", "right"])
    if edge == "top":
        x = random.randint(0, SCREEN_WIDTH)
        y = 0
    elif edge == "bottom":
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT
    elif edge == "left":
        x = 0
        y = random.randint(0, SCREEN_HEIGHT)
    else:  # right
        x = SCREEN_WIDTH
        y = random.randint(0, SCREEN_HEIGHT)
    angle = math.atan2(center_y - y, center_x - x)
    asteroids.append((x, y, angle))

def check_bullet_asteroid_collision(bullets, asteroids):
    global points
    bullets_to_remove = []
    asteroids_to_remove = []
    for bullet in bullets:
        bullet_x, bullet_y, _ = bullet
        for asteroid in asteroids:
            asteroid_x, asteroid_y, _ = asteroid
            distance = math.hypot(bullet_x - asteroid_x, bullet_y - asteroid_y)
            if distance < BULLET_SIZE + ASTEROID_SIZE:
                bullets_to_remove.append(bullet)
                asteroids_to_remove.append(asteroid)
                points += 10
    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)
    for asteroid in asteroids_to_remove:
        if asteroid in asteroids:
            asteroids.remove(asteroid)

def draw_explosion(x, y, radius):
    pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), int(radius))

def explosion_animation():
    global ship_exploded
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - explosion_start_time
    if elapsed_time <= EXPLOSION_DURATION:
        radius = (elapsed_time / EXPLOSION_DURATION) * EXPLOSION_MAX_RADIUS
        draw_explosion(ship_x, ship_y, radius)
    else:
        ship_exploded = False

def reset_game():
    global ship_x, ship_y, ship_angle, ship_exploded
    global lives, game_over, bullets, asteroids, points
    ship_x = SCREEN_WIDTH // 2
    ship_y = SCREEN_HEIGHT // 2
    ship_angle = 0
    ship_exploded = False
    lives = MAX_LIVES
    game_over = False
    bullets.clear()
    asteroids.clear()
    points = 0

running = True
last_spawn_time = pygame.time.get_ticks()
last_bullet_fired_time = 0

while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not ship_exploded and not game_over:
        if keys[pygame.K_LEFT]:
            ship_angle += 0.004 * dt
        if keys[pygame.K_RIGHT]:
            ship_angle -= 0.004 * dt

        if keys[pygame.K_UP]:
            ship_x += SHIP_SPEED * math.cos(ship_angle) * dt
            ship_y -= SHIP_SPEED * math.sin(ship_angle) * dt
            ship_x %= SCREEN_WIDTH
            ship_y %= SCREEN_HEIGHT

        if keys[pygame.K_SPACE] and current_time - last_bullet_fired_time >= BULLET_FIRE_DELAY:
            bullet_x = ship_x + SHIP_SIZE * math.cos(ship_angle)
            bullet_y = ship_y - SHIP_SIZE * math.sin(ship_angle)
            bullets.append((bullet_x, bullet_y, ship_angle))
            last_bullet_fired_time = current_time

        if check_ship_asteroid_collisions(ship_x, ship_y, asteroids):
            ship_exploded = True
            explosion_start_time = current_time
            lives -= 1
            if lives <= 0:
                game_over = True

        check_bullet_asteroid_collision(bullets, asteroids)

    screen.fill(BACKGROUND_COLOR)

    new_bullets = []
    for bullet in bullets:
        bullet_x, bullet_y, bullet_angle = bullet
        bullet_x += BULLET_SPEED * math.cos(bullet_angle) * dt
        bullet_y -= BULLET_SPEED * math.sin(bullet_angle) * dt
        if 0 <= bullet_x < SCREEN_WIDTH and 0 <= bullet_y < SCREEN_HEIGHT:
            new_bullets.append((bullet_x, bullet_y, bullet_angle))
            pygame.draw.circle(screen, BULLET_COLOR, (int(bullet_x), int(bullet_y)), BULLET_SIZE)
    bullets = new_bullets

    if current_time - last_spawn_time > SPAWN_RATE:
        if len(asteroids) < MAX_ASTEROIDS:
            spawn_asteroid()
        last_spawn_time = current_time

    new_asteroids = []
    for asteroid in asteroids:
        asteroid_x, asteroid_y, asteroid_angle = asteroid
        asteroid_x += ASTEROID_SPEED * math.cos(asteroid_angle) * dt
        asteroid_y += ASTEROID_SPEED * math.sin(asteroid_angle) * dt
        if -ASTEROID_SIZE <= asteroid_x <= SCREEN_WIDTH + ASTEROID_SIZE and -ASTEROID_SIZE <= asteroid_y <= SCREEN_HEIGHT + ASTEROID_SIZE:
            new_asteroids.append((asteroid_x, asteroid_y, asteroid_angle))
            pygame.draw.circle(screen, ASTEROID_COLOR, (int(asteroid_x), int(asteroid_y)), ASTEROID_SIZE)
    asteroids = new_asteroids

    if not ship_exploded:
        ship_vertices = [
            (ship_x + SHIP_SIZE * math.cos(ship_angle), ship_y - SHIP_SIZE * math.sin(ship_angle)),
            (ship_x + SHIP_SIZE * math.cos(ship_angle + 2.5), ship_y - SHIP_SIZE * math.sin(ship_angle + 2.5)),
            (ship_x, ship_y),
            (ship_x + SHIP_SIZE * math.cos(ship_angle - 2.5), ship_y - SHIP_SIZE * math.sin(ship_angle - 2.5)),
        ]
        pygame.draw.polygon(screen, SHIP_COLOR, ship_vertices)
    else:
        explosion_animation()

    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    points_text = font.render(f"Points: {points}", True, (255, 255, 255))
    screen.blit(points_text, (SCREEN_WIDTH - 150, 10))

    if game_over:
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

    pygame.display.update()

    if game_over and keys[pygame.K_r]:
        reset_game()

pygame.quit()
sys.exit()
