import pygame, sys, time, math, random
from pygame import *
from random import randrange

def processSpriteSheet(fileName, nRows, nCols, colorKey, hFlip = True):
    playerSheet = pygame.image.load(fileName).convert()
    playerSheet.set_colorkey(colorKey)
    if hFlip:
        playerSheet = pygame.transform.flip(playerSheet,True, False)
    playerWidth = playerSheet.get_size()[0]/nCols
    playerHeight = playerSheet.get_size()[1]/nRows
    playerRects = []
    for i in range(nRows):
        for j in range(nCols):
            playerRects.append(pygame.Rect(j*playerWidth,i*playerHeight, playerWidth, playerHeight))
    return playerSheet, playerRects

def entryWalk(window, width,height, bg, bgRect, playerSheet,playerRects):
    currentRect = 0
    playerHoriz = 50
    while (playerHoriz < width/2):
        window.fill((255, 255, 255))
        window.blit(bg, bgRect)
        window.blit(playerSheet, (playerHoriz,2*height/3),playerRects[currentRect])
        # UPDATE DISPLAY #
        pygame.display.flip()
        currentRect = (currentRect+1)%16
        playerHoriz += 1
    return playerHoriz

#Always need to initialize pygame first
pygame.init()

#initialize font (used to display score)
myfont = pygame.font.SysFont("monospace", 32)

#############
#SETUP WINDOW
#############
#create variables to hold window dimensions
width = 800
height = 600
#create a new window
window = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
pygame.display.set_caption("Sprite Dance")

mainClock = pygame.time.Clock()
random.seed(125)

#Define a few colors. Note: ordered triplets in the form (red, green, blue)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

############
#LOAD IMAGES
############
#load player sprite sheet
playerSheet, playerRects = processSpriteSheet("actionstashhd.png",16,16, colorKey = WHITE)
currentPlayerRect = 0

#Load flying yoga ballet frog
frogSheet, frogRects = processSpriteSheet("frogrect.png",3,7, colorKey = WHITE, hFlip = False)
nFrog = 20
frogIndex = range(0,19) + range(18, -1, -1)
frogDir = 'left'

#Load explosions
explodeSheet, explodeRect = processSpriteSheet("explosion1.png",4,4, colorKey = GREEN, hFlip = False)

#load background
bg = pygame.image.load("meadow.jpg")

#create background rectangle
bgRect = pygame.Rect(0, 0, bg.get_size()[0],bg.get_size()[1])

##################
#INIT SOUNDS/MUSIC
##################
# set up music
pygame.mixer.music.load('badboy.mid')
pygame.mixer.music.play(-1, 0.0)
playerHoriz = entryWalk(window, width, height, bg, bgRect, playerSheet,playerRects) #the grand entrance...

#####################
#OTHER IMPORTANT VARS
#####################
flipDelay = 50 #Set delay to limit how often player can change dancing direction
elapsedTime = 0 #Total dance time
dancerPosition = [width, 0] #[frog, explosion] (this would be better with a dictionary...)
dancerRects = [0,0] #[frog,explosion]
dancerOnScreen = [False, False]
################
#START MAIN LOOP
################
while True:   #infinite loop
    for event in pygame.event.get(): #Terminate program if user tries to quit window
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if 3%randrange(3,6)==0 and playerHoriz < width:
        playerHoriz += 3
        flipDelay -= 1
    if 4%randrange(3,6)==0 and playerHoriz > 0:
        playerHoriz -= 3
        flipDelay -= 1
    if 5%randrange(3,6)==0 and flipDelay < 0:
        playerSheet = pygame.transform.flip(playerSheet,True, False)
        flipDelay = 50
        
    # draw a white background onto the window
    window.fill(WHITE)
    window.blit(bg, bgRect)
    window.blit(playerSheet, (playerHoriz,2*height/3),playerRects[currentPlayerRect])

    #Animate frog (I know this is an atrocious section...)
    if (elapsedTime/1000 == 10 or dancerOnScreen[0]==True or elapsedTime/1000%20 == 0):
        dancerOnScreen[0] = True
        window.blit(frogSheet,(dancerPosition[0],height/3),frogRects[frogIndex[dancerRects[0]]])
        if dancerRects[0]<38:
            dancerRects[0] = (dancerRects[0]+1)%38
        if frogDir == 'left':
            dancerPosition[0] -= 4
            if dancerPosition[0] < -80:
                dancerOnScreen[0] = False
                frogDir = 'right'
                dancerRects[0] = 0
        if frogDir == 'right':
            dancerPosition[0] += 4
            if dancerPosition[0] > (width+80):
                dancerOnScreen[0] = False
                frogDir = 'left'
                dancerRects[0] = 0

    #Animate explosions
    if (dancerOnScreen[1]==True or (elapsedTime/1000.0>31 and elapsedTime/1000<47)):
        dancerOnScreen[1] = True
        window.blit(explodeSheet,(dancerPosition[1],height/7),explodeRect[dancerRects[1]])
        if dancerRects[1]<16:
            dancerRects[1] = (dancerRects[1]+1)%16
            if dancerRects[1] == 15:
                dancerPosition[1] = randrange(0, width)
        if elapsedTime/1000>47:
                dancerOnScreen[1] = False
                dancerRects[1] = 0           

    # UPDATE DISPLAY #
    pygame.display.flip()
   #pygame.display.update([playerRects[currentPlayerRect], bgRect])
    currentPlayerRect = (currentPlayerRect-1)%256

        #Check if user has released escape key (quit program)
    if event.type == KEYUP:  
        if event.key == K_ESCAPE: #quit when escape key released
            pygame.quit()
            sys.exit()

    mainClock.tick(30)
    elapsedTime += mainClock.get_time()  
