import pygame
import random
import sys


def draw_floor():
    display.blit(bgFloor, (bgFloorX, 945))
    display.blit(bgFloor, (bgFloorX + displayWidth, 945))


def create_pipe():
    randomPipePos = random.choice(pipeHeight)
    downPipe = pipeSurface.get_rect(midtop=(1980, randomPipePos))
    topPipe = pipeSurface.get_rect(midbottom=(1980, randomPipePos - 350))
    return downPipe, topPipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visiblePipes = [pipe for pipe in pipes if pipe.right > - 50]
    return visiblePipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1080:
            display.blit(pipeSurface, pipe)
        else:
            flipPipe = pygame.transform.flip(pipeSurface, False, True)
            display.blit(flipPipe, pipe)


def check_colisson(pipes):
    global canScore
    for pipe in pipes:
        if personRect.colliderect(pipe):
            chan3.play(hitSound)
            canScore = True
            return False

    if personRect.top <= -300 or personRect.bottom >= 945:
        chan3.play(hitSound)
        canScore = True
        return False

    return True


def rotate_person(person):
        newPerson = pygame.transform.rotozoom(person, -personMovement * 2, 1)
        return newPerson


def person_animation():
    newPerson = personAnimation[personIndex]
    newPersonRect = newPerson.get_rect(center=(300, personRect.centery))
    return newPerson, newPersonRect


def score_display(gameState):
    if gameState == 'main_game':
        scoreSurface = gameFont.render(str(int(score)), True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center=(displayWidth//2, 50))
        display.blit(scoreSurface, scoreRect)
    if gameState == 'game_over':
        scoreSurface = gameFont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scoreRect = scoreSurface.get_rect(center=(300, 50))
        display.blit(scoreSurface, scoreRect)

        highScoreSurface = gameFont.render(f'High Score: {int(highScore)}', True, (255, 255, 255))
        highScoreRect = highScoreSurface.get_rect(center=(1500, 50))
        display.blit(highScoreSurface, highScoreRect)


def score_update(score, highScore):
    if score > highScore:
        highScore = score
    return highScore


def score_check():
    global score, canScore

    if pipeList:
        for pipe in pipeList:
            if 299 < pipe.centerx < 305 and canScore:
                score += 1
                chan4.play(scoreSound)
                canScore = False
            if pipe.centerx < 0:
                canScore = True


def gameover_animation():
    newGameOver = gameOverAnimation[gameOverIndex]
    newGameOverRect = newGameOver.get_rect(center=(displayWidth//2, displayHeight//2))
    return newGameOver, newGameOverRect


def exit_animation():
    newExit = exitAnimation[exitIndex]
    newExitRect = newExit.get_rect(center=(70, 70))
    return newExit, newExitRect


def color_animation():
    newColor = colorAnimation[colorIndex]
    newColorRect = newColor.get_rect(center=(70, 200))
    return newColor, newColorRect


pygame.init()


# display settings
# ---------------
displayWidth = 1920
displayHeight = 1080

display = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Tap-tap Bird')
clock = pygame.time.Clock()
gameFont = pygame.font.Font('fonts/04B_19__.ttf', 70)


# game variables
# ---------------

gravity = 0.25
personMovement = 0
gameActive = False
score = 0
highScore = 0
canScore = True
pygame.mouse.set_visible(False)  # makes cursor invisible
colorChange = 0


# image settings
# ---------------
# icon
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

# background
bgImage = pygame.image.load('images/bg.png').convert()

# ground
bgFloor = pygame.image.load('images/bgfloor.png').convert()
bgFloorX = 0

# character
personDownFlap = pygame.transform.scale(pygame.image.load('images/person1_down.png'), (102, 72)).convert_alpha()
personMidFlap = pygame.transform.scale(pygame.image.load('images/person1_mid.png'), (102, 72)).convert_alpha()
personUpFlap = pygame.transform.scale(pygame.image.load('images/person1_up.png'), (102, 72)).convert_alpha()
person2DownFlap = pygame.transform.scale(pygame.image.load('images/person2_down.png'), (102, 72)).convert_alpha()
person2MidFlap = pygame.transform.scale(pygame.image.load('images/person2_mid.png'), (102, 72)).convert_alpha()
person2UpFlap = pygame.transform.scale(pygame.image.load('images/person2_up.png'), (102, 72)).convert_alpha()
personAnimation = [personDownFlap, personMidFlap, personUpFlap]
personIndex = 0
personSurface = personAnimation[personIndex]
personRect = personSurface.get_rect(center=(300, displayHeight//2))

# menu
gameOverSurface1 = pygame.image.load('images/menu.png').convert_alpha()
gameOverSurface2 = pygame.image.load('images/menu2.png').convert_alpha()
gameOverAnimation = [gameOverSurface1, gameOverSurface2]
gameOverIndex = 1
gameOverSurface = gameOverAnimation[gameOverIndex]
gameOverRect = gameOverSurface.get_rect(center=(displayWidth//2, displayHeight//2))

# pipe
pipeSurface = pygame.image.load('images/pipe.png').convert_alpha()
pipeSurface = pygame.transform.scale(pipeSurface, (156, 936))

# exit button
exitIcon1 = pygame.transform.scale(pygame.image.load('images/quit.png'), (96, 102)).convert_alpha()
exitIcon2 = pygame.transform.scale(pygame.image.load('images/quit2.png'), (96, 102)).convert_alpha()
exitAnimation = [exitIcon1, exitIcon2]
exitIndex = 0
exitSurface = exitAnimation[exitIndex]
exitRect = exitSurface.get_rect(center=(70, 70))

# change color button
colorIcon1 = pygame.transform.scale(pygame.image.load('images/color.png'), (96, 102)).convert_alpha()
colorIcon2 = pygame.transform.scale(pygame.image.load('images/color2.png'), (96, 102)).convert_alpha()
colorAnimation = [colorIcon1, colorIcon2]
colorIndex = 0
colorSurface = colorAnimation[colorIndex]
colorRect = colorSurface.get_rect(center=(70, 200))

# cursor
cursor = pygame.transform.scale(pygame.image.load('images/cursor.png'), (36, 48)).convert_alpha()


# user events
# ---------------
PERSONFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(PERSONFLAP, 200)  # change pictures every 200 ms

MENU = pygame.USEREVENT + 2
pygame.time.set_timer(MENU, 500)        # change pictures every 500 ms

BUTTONS = pygame.USEREVENT + 3
pygame.time.set_timer(BUTTONS, 700)     # change pictures every 700 ms


# pipe settings
# ---------------
pipeList = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1800)  # spawning pipes every 1800 ms
pipeHeight = [450, 500, 550, 600, 650, 700, 750, 800]


# sound settings
# ---------------
# sounds
flapSound = pygame.mixer.Sound('sounds/wing.wav')
hitSound = pygame.mixer.Sound('sounds/hit.wav')
menuSound = pygame.mixer.Sound('sounds/menu.wav')
bgSound = pygame.mixer.Sound('sounds/bg.wav')
scoreSound = pygame.mixer.Sound('sounds/point.wav')
clickSound = pygame.mixer.Sound('sounds/click.wav')

# volume
clickSound.set_volume(0.1)
menuSound.set_volume(0.1)
bgSound.set_volume(0.5)
hitSound.set_volume(0.1)
flapSound.set_volume(0.1)
scoreSound.set_volume(0.1)

# channels
pygame.mixer.set_num_channels(6)
chan1 = pygame.mixer.Channel(0)
chan2 = pygame.mixer.Channel(1)
chan3 = pygame.mixer.Channel(2)
chan4 = pygame.mixer.Channel(3)
chan5 = pygame.mixer.Channel(4)
chan6 = pygame.mixer.Channel(5)


# game run
# ---------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # key settings
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameActive:
                personMovement = 0
                personMovement -= 12
                chan5.play(flapSound)
            if event.key == pygame.K_SPACE and gameActive == False:
                gameActive = True
                pipeList.clear()
                personRect.center = (300, displayHeight//2)
                personMovement = 0
                score = 0

        # pipe spawning
        if event.type == SPAWNPIPE:
            pipeList.extend(create_pipe())

        # flap animation
        if event.type == PERSONFLAP:
            if personIndex < 2:
                personIndex += 1
            else:
                personIndex = 0

        personSurface, personRect = person_animation()

        # menu animation
        if event.type == MENU:
            if gameOverIndex < 1:
                gameOverIndex += 1
            else:
                gameOverIndex = 0

        # buttons animation
        if event.type == BUTTONS:
            if exitIndex < 1:
                exitIndex += 1
            else:
                exitIndex = 0

            if colorIndex < 1:
                colorIndex += 1
            else:
                colorIndex = 0

    display.blit(bgImage, (0, 0))

    if gameActive:
        # sound
        chan1.play(bgSound, loops=-1)

        # person
        personMovement += gravity
        rotatedPerson = rotate_person(personSurface)
        personRect.centery += personMovement
        display.blit(rotatedPerson, personRect)
        gameActive = check_colisson(pipeList)

        # pipes
        pipeList = move_pipes(pipeList)
        draw_pipes(pipeList)
        score_check()
        score_display('main_game')

    else:
        # sound
        chan2.play(menuSound, loops=-1)

        # score
        highScore = score_update(score, highScore)
        score_display('game_over')

        # images and animation
        display.blit(gameOverSurface, gameOverRect)
        gameOverSurface, gameOverRect = gameover_animation()

        display.blit(exitSurface, exitRect)
        display.blit(colorSurface, colorRect)

        # mouse position checker
        if 22 < (pygame.mouse.get_pos())[0] < 118 and 19 < (pygame.mouse.get_pos())[1] < 121:
            exitSurface, exitRect = exit_animation()
            if pygame.mouse.get_pressed()[0]:
                chan6.play(clickSound)
                pygame.time.delay(300)
                pygame.quit()
        else:
            display.blit(exitIcon1, exitRect)

        if 22 < (pygame.mouse.get_pos())[0] < 118 and 151 < (pygame.mouse.get_pos())[1] < 253:
            colorSurface, colorRect = color_animation()
            if pygame.mouse.get_pressed()[0]:
                chan6.play(clickSound, loops=0)
                pygame.time.delay(300)
                if colorChange < 1:
                    colorChange += 1
                    personAnimation = [person2DownFlap, person2MidFlap, person2UpFlap]
                else:
                    colorChange = 0
                    personAnimation = [personDownFlap, personMidFlap, personUpFlap]
        else:
            display.blit(colorIcon1, colorRect)

        # cursor
        display.blit(cursor, (pygame.mouse.get_pos()))

    # floor
    bgFloorX -= 5
    draw_floor()
    if bgFloorX <= -1920:
        bgFloorX = 0

    pygame.display.update()
    clock.tick(120)