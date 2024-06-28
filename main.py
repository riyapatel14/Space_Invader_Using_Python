import math
import random
import pygame
from pygame.locals import *
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)
restart_font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

# create enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
    show_restart_button()

def win_text():
    win_text = game_over_font.render("YOU WIN!", True, (0, 255, 0))
    screen.blit(win_text, (250, 250))
    show_restart_button()

def show_restart_button():
    restart_text = restart_font.render("Press 'R' to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (250, 350))

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# draw bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# collision detection, find distance between (x1,y1) and (x2,y2)
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    return distance < 27

def set_background():
    global background
    screen.fill((0, 0, 128))  # Dark blue background
    screen.blit(background, (0, 0))

def move_bullet():
    global bulletX, bulletY, bullet_state
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

def game_input():
    global running, playerX_change, bulletX, playerX, bulletY, bullet_state, game_active, score_value
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and game_active:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
            if event.key == pygame.K_r and not game_active:
                game_active = True
                score_value = 0
                reset_enemies()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if game_active:
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

def enemy_movement():
    global enemyX, enemyX_change, enemyY, enemyY_change, game_active
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            game_active = False

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        enemy(enemyX[i], enemyY[i], i)

def collision():
    global num_of_enemies, enemyX, enemyY, bulletX, bulletY, bullet_state, score_value, game_active
    for i in range(num_of_enemies):
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        if score_value >= 10:
            win_text()
            game_active = False

def reset_enemies():
    global enemyX, enemyY, enemyX_change, enemyY_change
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = 4
        enemyY_change[i] = 40

# Game Loop
running = True
game_active = True

while running:
    set_background()
    game_input()
    if game_active:
        enemy_movement()
        collision()
        move_bullet()
        player(playerX, playerY)
    show_score(textX, textY)
    if not game_active:
        game_over_text() if score_value < 10 else win_text()
    pygame.display.update()