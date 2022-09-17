import pygame
import random
import math

# initalize pygame
pygame.init()

# creating the screen
# width * height
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('./assets/background.png')

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("./assets/spaceship.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("./assets/player.png")
playerX = 370
playerY = 480
playerX_change = 0

# alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 26)
textX = 15
textY = 15

# game over text
overFont = pygame.font.Font('freesansbold.ttf', 72)

# inspiration text
insp = pygame.font.Font('freesansbold.ttf', 16)

# num of enemies
numOfEnemies = 3

for enemy in range(numOfEnemies):
    alienImg.append(pygame.image.load("./assets/alien.png"))
    alienX.append(random.randint(0,735))
    alienY.append(random.randint(50,150))
    alienX_change.append(2)
    alienY_change.append(20)

#bullet
# Ready - Constant
# Fire - in Motion

bulletImg = pygame.image.load("./assets/bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 10
bulletState = "ready"

def player(x, y):
    # blit == draw
    screen.blit(playerImg, (x, y))

def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))

def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    # using distance formula
    distance = math.sqrt((bulletY - enemyY)**2 + (bulletX - enemyX)**2)
    if distance < 27:
        return True
    return False

def showScore(x, y):
    score_render = font.render(f'Score : {score}', True, (255,255,255))
    screen.blit(score_render, (x, y))

def gameOverText():
    gameOverRender = overFont.render("Game Over", True, (255, 255, 255))
    screen.blit(gameOverRender, (200, 250))

def inspirationText():
    ins = insp.render("Inspired by bugs!", True, (255,255,255))
    screen.blit(ins, (330, 570))

# game loop
# persistent content
running = True
while running:

    # background color of image
    screen.fill((0,0,0))
    # background image
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            running = False

        # keystroke event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # boundary checking for alien
    for i in range(numOfEnemies):
        
        # game over
        if alienY[i] > 400:
            for j in range(numOfEnemies):
                alienY[j] = 2000
            gameOverText()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 2
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -2
            alienY[i] += alienY_change[i]

        # collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bulletState = "ready"
            score += 1
            alienX[i] = random.randint(0,735)
            alienY[i] = random.randint(50,150)
        alien(alienX[i], alienY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # boundary checking for spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    inspirationText()
    showScore(textX, textY)
    player(playerX, playerY)

    # ALWAYS UPDATE
    pygame.display.update()