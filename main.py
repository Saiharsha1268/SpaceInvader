import math
import pygame
import random
from pygame import mixer

# initialize the pygame
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))
# Title and Icon
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
backgroundImg = pygame.image.load("imresizer.jpg")
playerImg = pygame.image.load("spaceship (1).png")
playerX = 370
playerY = 480
playerXchange = 0
enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
n = 8
complete = 0
for i in range(n):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(0.4)
    enemyYchange.append(40)
monsterImg = pygame.image.load("cthulhu.png")
monsterX = random.randint(0, 736)
monsterY = random.randint(50, 150)
monsterXchange = 0.5
monsterYchange = 50
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletYchange = -2.5
bulletstate = "ready"
scorevalue = 0
font = pygame.font.Font("Munsteria.ttf", 32)
textX = 10
textY = 10
gameover = pygame.font.Font("Munsteria.ttf", 48)
gameoverX = 290
gameoverY = 300
mixer.music.load("background.wav")
mixer.music.play(-1)
escape1 = pygame.font.Font("freesansbold.ttf", 20)
escape1X = 600
escape1Y = 100
explosionImg = pygame.image.load("explosion.png")
explosionX = 1000
explosionY = 1000
e = 0
collision1 = False

def explosion(x, y):
    screen.blit(explosionImg, (x, y))


def escape():
    es = escape1.render("press esc to exit", True, (255, 255, 255))
    screen.blit(es, (escape1X, escape1Y))


def game_over():
    game = gameover.render("GAME OVER", True, (0, 0, 0))
    screen.blit(game, (gameoverX, gameoverY))


def showscore():
    score = font.render("SCORE : " + str(scorevalue), True, (230, 0, 230))
    screen.blit(score, (textX, textY))


def player(x):
    screen.blit(playerImg, (x, playerY))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
def monster(x,y):
    screen.blit(monsterImg, (x, y))


def firebullet(x, y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollision(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if distance < 54:
        return True
    else:
        return False
def iscollision1(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if distance < 27:
        return True
    else:
        return False
f = 0

# game loop
running = True
while running:
    e = e + 1
    # R G B
    screen.fill((0, 0, 0))
    # Background
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -1
            if event.key == pygame.K_RIGHT:
                playerXchange = 1
            if event.key == pygame.K_SPACE:
                if bulletstate == "ready":
                    bulletsound = mixer.Sound("laser.wav")
                    bulletsound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)
            if complete == 1:
                if event.key == pygame.K_ESCAPE:
                    exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0
    playerX += playerXchange
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    for i in range(n):
        enemyX[i] += enemyXchange[i]
        if enemyX[i] <= 0:
            enemyXchange[i] = 0.5
            enemyY[i] += enemyYchange[i]
        elif enemyX[i] >= 736:
            enemyXchange[i] = -0.5
            enemyY[i] += enemyYchange[i]
        enemy(enemyX[i], enemyY[i], i)
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionsound = mixer.Sound("explosion.wav")
            explosionsound.play()
            explosionX = bulletX
            explosionY = bulletY
            bulletY = 480
            bulletstate = "ready"
            scorevalue += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            e = 0
    if scorevalue > 10:
        monsterX += monsterXchange
        if monsterX <= 0:
            monsterXchange = 0.6
            monsterY += monsterYchange
        elif monsterX >= 736:
            monsterXchange = -0.6
            monsterY += monsterYchange
        monster(monsterX, monsterY)
        collision1 = iscollision(monsterX, monsterY, bulletX, bulletY)
    if collision1:
        explosionsound = mixer.Sound("explosion.wav")
        explosionsound.play()
        explosionX = bulletX
        explosionY = bulletY
        bulletY = 480
        bulletstate = "ready"
        scorevalue += 1
        f = f+1
        print(f)
        e = 0
    for i in range(n):
        if enemyY[i] > 416:
            for j in range(n):
                enemyY[j] = 2000
            game_over()
            escape()
            complete = 1
            break
    if bulletY <= 0:
        bulletY = 480
        bulletstate = "ready"
    if bulletstate == "fire":
        firebullet(bulletX, bulletY)
        bulletY += bulletYchange
    if e < 50:
        explosion(explosionX, explosionY)
    if f >= 5:
        monsterX = 2000
        monsterY = 2000
    showscore()
    player(playerX)
    pygame.display.update()