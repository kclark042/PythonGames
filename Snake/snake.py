# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

FPS = 10
#WINDOWWIDTH = 640
#WINDOWHEIGHT = 480
WINDOWWIDTH = 740
WINDOWHEIGHT = 580
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
TEAL 	  = ( 51, 255, 209)
DARKBLUE  = ( 51,  63, 255)
LIGHTBLUE = ( 22, 171, 216)
GREY      = (201, 203, 240)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords1 = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction1 = RIGHT

    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords2 = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction2 = RIGHT
    # Start the apple in a random place.
    apple1 = getRandomLocation()
    apple2 = getRandomLocation()
    apple3 = getRandomLocation()
    
    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                #if (event.key == K_LEFT or event.key == K_a) and direction1 != RIGHT:
                #handles either snake going left or both going left
                if event.key == K_LEFT and direction1 != RIGHT:
                    direction1 = LEFT
                elif event.key == K_a and direction2 != RIGHT:
                	direction2 = LEFT
                elif event.key ==  K_KP4 and (direction1 != RIGHT and direction2 != RIGHT):
                	direction1 = LEFT
                	direction2 = LEFT

                #handles turning right
                elif event.key == K_RIGHT and direction1 != LEFT:
                    direction1 = RIGHT
                elif event.key == event.key == K_d and direction2 != LEFT:
                	direction2 = RIGHT
               	elif event.key == K_KP6 and (direction1 != LEFT and direction2 != LEFT): 
                	direction1 = RIGHT
                	direction2 = RIGHT

                #handles turning up
                elif event.key == K_UP and direction1 != DOWN:
                    direction1 = UP
                elif event.key == event.key == K_w and direction2 != DOWN:
                	direction2 = UP
                elif event.key == K_KP8 and (direction1 != DOWN and direction2 != DOWN):
                	direction1 = UP
                	direction2 = UP

                elif event.key == K_DOWN and direction1 != UP:
                    direction1 = DOWN
                elif event.key == event.key == K_s and direction2 != UP:
                	direction2 = DOWN
                elif event.key == K_KP2 and (direction1 != UP and direction2 != UP):
                	direction1 = DOWN
                	direction2 = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords1[HEAD]['x'] == -1 or wormCoords1[HEAD]['x'] == CELLWIDTH or wormCoords1[HEAD]['y'] == -1 or wormCoords1[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody1 in wormCoords1[1:]:
            if wormBody1['x'] == wormCoords1[HEAD]['x'] and wormBody1['y'] == wormCoords1[HEAD]['y']:
                return # game over

        # check if worm has eaten an apply
        if wormCoords1[HEAD]['x'] == apple1['x'] and wormCoords1[HEAD]['y'] == apple1['y']:
            # don't remove worm's tail segment
            apple1 = getRandomLocation() # set a new apple somewhere
        elif wormCoords1[HEAD]['x'] == apple2['x'] and wormCoords1[HEAD]['y'] == apple2['y']:
        	apple2 = getRandomLocation()
        elif wormCoords1[HEAD]['x'] == apple3['x'] and wormCoords1[HEAD]['y'] == apple3['y']:
        	apple3 = getRandomLocation()                                 
        else:
            del wormCoords1[-1] # remove worm's tail segment


        # check if the worm has hit itself or the edge
        if wormCoords2[HEAD]['x'] == -1 or wormCoords2[HEAD]['x'] == CELLWIDTH or wormCoords2[HEAD]['y'] == -1 or wormCoords2[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody2 in wormCoords2[1:]:
            if wormBody2['x'] == wormCoords2[HEAD]['x'] and wormBody2['y'] == wormCoords2[HEAD]['y']:
                return # game over

        #check if worm has eaten an apply
        if wormCoords2[HEAD]['x'] == apple1['x'] and wormCoords2[HEAD]['y'] == apple1['y']:
            # don't remove worm's tail segment
            apple1 = getRandomLocation() # set a new apple somewhere
        elif wormCoords2[HEAD]['x'] == apple2['x'] and wormCoords2[HEAD]['y'] == apple2['y']:
        	apple2 = getRandomLocation()
        elif wormCoords2[HEAD]['x'] == apple3['x'] and wormCoords2[HEAD]['y'] == apple3['y']:
        	apple3 = getRandomLocation()
        else:
            del wormCoords2[-1] # remove worm's tail segment

        
        		
        # move the worm by adding a segment in the direction it is moving
        if direction1 == UP:
            newHead1 = {'x': wormCoords1[HEAD]['x'], 'y': wormCoords1[HEAD]['y'] - 1}
        elif direction1 == DOWN:
            newHead1 = {'x': wormCoords1[HEAD]['x'], 'y': wormCoords1[HEAD]['y'] + 1}
        elif direction1 == LEFT:
            newHead1 = {'x': wormCoords1[HEAD]['x'] - 1, 'y': wormCoords1[HEAD]['y']}
        elif direction1 == RIGHT:
            newHead1 = {'x': wormCoords1[HEAD]['x'] + 1, 'y': wormCoords1[HEAD]['y']}
        
        
        if direction2 == UP:
        	newHead2 = {'x': wormCoords2[HEAD]['x'], 'y': wormCoords2[HEAD]['y'] - 1}
        elif direction2 == DOWN:
        	newHead2 = {'x': wormCoords2[HEAD]['x'], 'y': wormCoords2[HEAD]['y'] + 1}
        elif direction2 == LEFT:
        	newHead2 = {'x': wormCoords2[HEAD]['x'] - 1, 'y': wormCoords2[HEAD]['y']}
        elif direction2 == RIGHT:
        	newHead2 = {'x': wormCoords2[HEAD]['x'] + 1, 'y': wormCoords2[HEAD]['y']}

        
        wormCoords1.insert(0, newHead1)
        wormCoords2.insert(0, newHead2)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm1(wormCoords1)
        drawWorm2(wormCoords2)
        
        rand = random.randint(1,25)
        if rand == 5:
        	apple1 = getRandomLocation()
        	apple2 = getRandomLocation()
        	apple3 = getRandomLocation()

        drawApple(apple1)
        drawApple(apple2)
        drawApple(apple3)
        drawScore1(len(wormCoords1) - 3)
        drawScore2(len(wormCoords2) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snake!', True, GREY, DARKBLUE)
    titleSurf2 = titleFont.render('Snake!', True, TEAL)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore1(score):
    scoreSurf = BASICFONT.render('Player 1 : %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (WINDOWWIDTH - 320, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawScore2(score):
	scoreSurf = BASICFONT.render('Player 2 : %s' % (score), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topright = (WINDOWWIDTH - 140, 10)
	DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawWorm1(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

def drawWorm2(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKBLUE, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()