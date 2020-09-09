import pygame
import random
import math
import sys
import pygame_menu
from pygame import mixer
from pygame.locals import *

# initialize all pygame modules
pygame.init()

# create the screen
# set_mode(size=(0, 0), flags=0, depth=0, display=0)
# this means size will be passed in a tuple
# If no size is passed or is set to (0, 0) and pygame uses SDL version 1.2.10 or above,
# the created Surface will have the same size as the current screen resolution.
# If only the width or height are set to 0, the Surface will have the same width or height as the screen resolution.

S = 0
screen = pygame.display.set_mode((800, 600))  # 800 = width and 600=height

# background
background = pygame.image.load('2819.jpg')
# caption and Icon

pygame.display.set_caption("Space Invaders")

icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# background_music
mixer.music.load('background.wav')
mixer.music.play(-1)
# Player
playerImg = pygame.image.load('destroyer.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for _ in range(num_of_enemies):
    enemyImg.append(pygame.image.load('monsters.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(5)
    enemyY_change.append(10)

# bullet

# ready- you cant see the bullet on the screen
# fire- the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480  # because the bullet is always fired at the same level
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# we have taken these coordinates because we want to place the
# spaceship in the middle lower section of the screen

# score

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
over_FONT = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score_VALUE = font.render("score :" + str(score), True, (255, 255, 255))
    screen.blit(score_VALUE, (x, y))


def game_over_text():
    OVER_text = over_FONT.render("GAME OVER", True, (255, 255, 255))
    screen.blit(OVER_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # to blit means to draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # to blit means to draw


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # +16 and +10 is to ensure that bullet emerges from centre of spacesip


def set_difficulty(value, s):
    if value == 1:
        S = 6
    else:
        S = 12

click = False

def menu_screen():
    while True:
        menu = pygame_menu.Menu(300, 400, 'Welcome',
                                theme=pygame_menu.themes.THEME_DARK)


    mx, my = pygame.mouse.get_pos()

    button_1 = pygame.Rect(50, 100, 200, 50)
    button_2 = pygame.Rect(50, 200, 200, 50)
    if button_1.collidepoint((mx, my)):
        if click:
            S = 6
    if button_2.collidepoint((mx, my)):
        if click:
            S = 12
    pygame.draw.rect(screen, (255, 0, 0), button_1)
    pygame.draw.rect(screen, (255, 0, 0), button_2)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True

    pygame.display.update()


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

        # Game Loop


def welcome_screen():
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

                # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                #menu_screen()
                return
            else:
                x = pygame.image.load('homepage.jpg').convert_alpha()
                screen.blit(x, (-40, 100))
                start_Instruction = pygame.font.Font('freesansbold.ttf', 32)
                instruction = start_Instruction.render("PRESS SPACE TO START", True, (255, 255, 255))
                screen.blit(instruction, (200, 360))
                # screen.blit(GAME_SPRITES['player'], (playerx, playery))
                pygame.display.update()


welcome_screen()

running = True
while running:

    # RGB = red,green and blue
    # takes rgb argument as a tuple
    screen.fill((50.2, 0, 50.2))
    # we need to always update our screen continuously since our game is a dynamic thing

    screen.blit(background, (0, 0))  # (0,0) becuase we want our image to start from origin
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed , check whehter its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("left arrow is pressed")
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                print("right arrow is pressed")
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound(
                        'laser.wav')  # if you want sound to play for short while, we use mixer.sound otherwise we will use mixer.load

                    bullet_sound.play()

                bulletX = playerX  # because if we took simply playerX , then bullet
                # was changing its x according with player
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("keystroke has been released")
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 736
    elif playerX >= 736:
        playerX = -0
    # we took x co-ordinate to be 736 pixels because the size of the spaceship is 64 pixels
    # so 800-64=736

    # enemy movement
    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyX_change[i] =7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]

            # collision

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_SOUND = mixer.Sound('explosion.wav')
            explosion_SOUND.play()
            bulletY = 480
            bullet_state = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 200)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
