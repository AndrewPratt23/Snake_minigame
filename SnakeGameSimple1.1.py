import pygame
import random
import time
from collections import deque

pygame.init()

## Key Variables
imgWidth = 64
imgHeight = 64

num_boxes = 10


## Creating Window
display_width = (imgWidth+1)*num_boxes + 1
display_height = (imgHeight+1)*num_boxes + 1

gameDisplay = pygame.display.set_mode((display_width, display_height))

## Name
pygame.display.set_caption("Snake")

## Useful Binds
black = (0, 0, 0)
white = (255, 255, 255)
lightRed = (255, 100, 100)
red = (255, 0, 0)
lightGreen = (100, 255, 100)
green = (0, 255, 0)
lightBlue = (84, 150, 255)
lightYellow = (255, 255, 100)
yellow = (255, 255, 0)



## Translator

def pixelsToBlock(x, y):
    width =(x-2)/65
    height =((y-2)/65) * 10
    return int(width+height)

def blockToPixelsX(block):
    width = (block%10)*65 + 2
    return int(width)
    
def blockToPixelsY(block):
    height = (block//10)*65 + 2
    return int(height)
    

## The Mouse
def mouse(mouseX, mouseY):
    pygame.draw.rect(gameDisplay, yellow, [mouseX, mouseY, 64, 64])
    

## Board
def board():
    pygame.draw.rect(gameDisplay, black, [1, 1, 1, display_height])
    pygame.draw.rect(gameDisplay, black, [1, 1, display_width, 1])
    for i in range(1, num_boxes+1):
        pygame.draw.rect(gameDisplay, black, [i*(imgWidth+1)+1, 1, 1, display_height])
        pygame.draw.rect(gameDisplay, black, [1, i*(imgHeight+1)+1, display_width, 1])

## Game Clock
clock = pygame.time.Clock()

## Text Display
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def center_message(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/3))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


def score_message(text):
    largeText = pygame.font.Font('freesansbold.ttf', 65)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (2*display_height/3))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def custom_message(text, fontSize, x, y):
    largeText = pygame.font.Font('freesansbold.ttf', fontSize)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

def button(msg,x,y,w,h,ic,ac,action=None,var=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None and var == None:
            action()
        elif click[0] == 1 and action != None and var != None:
            action(var)
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("freesansbold.ttf",30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def exit():
    pygame.quit()
    quit()



####### THE SNAKE #########

class Snake:
    def __init__(self, x = 2, y = 2, grid = ["Y"]):
        self.x = deque([x])
        self.y = deque([y])
        self.grid = {"Y": [0], "N": []}
        for i in range(1,100):
            self.grid["N"].append(i)

    def move(self, x, y, score):
        self.x.append(x)
        self.y.append(y)

        tempBlock = pixelsToBlock(x, y)
        self.grid["Y"].append(tempBlock)
        self.grid["N"].remove(tempBlock)

        self.draw(x, y)
        for i in range(score-1):
            tempX = self.x.popleft()
            tempY = self.y.popleft()
            
            self.draw(tempX, tempY)

            self.x.append(tempX)
            self.y.append(tempY)

        tempBlock = pixelsToBlock(self.x.popleft(), self.y.popleft())
        self.grid["Y"].remove(tempBlock)
        self.grid["N"].append(tempBlock)
            

    def eat(self, x, y, score):
        
        self.x.append(x)
        self.y.append(y)

        tempBlock = pixelsToBlock(x, y)
        self.grid["Y"].append(tempBlock)
        self.grid["N"].remove(tempBlock)

        self.draw(x, y)
        
        for i in range(score-1):
            tempX = self.x.popleft()
            tempY = self.y.popleft()

            self.draw(tempX, tempY)

            self.x.append(tempX)
            self.y.append(tempY)


    def draw(self, x, y):
        pygame.draw.rect(gameDisplay, lightBlue, [x, y, 64, 64])

    def checkLocation(self, x, y, score):
        for i in range(score):
            tempX = self.x.popleft()
            tempY = self.y.popleft()
            if tempX == x and tempY == y:
                return False
            self.x.append(tempX)
            self.y.append(tempY)
        return True

## Game Intro
def game_intro():
    intro = True

    
##    pygame.draw.rect(gameDisplay, green,(display_width/4-75,475,150,50))
##    pygame.draw.rect(gameDisplay, yellow,(display_width/2-75,475,150,50))
##    pygame.draw.rect(gameDisplay, red,(3*display_width/4-75,475,150,50))
    

##    custom_message("Easy", 30, (display_width/4), 500)
##    custom_message("Medium", 30, (display_width/2), 500)
##    custom_message("Hard", 30, (3*display_width/4), 500)

    pygame.display.update()
    gameDisplay.fill(white)
    center_message("SNAKE")
    custom_message("Please choose a difficulty", 40, (display_width/2), (2*display_height/3))
            
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            
            button("Easy", display_width/4-75,475,150,50, green, lightGreen, game_loop, 3)
            button("Medium", display_width/2-75,475,150,50, yellow, lightYellow, game_loop, 4)
            button("Hard", 3*display_width/4-75,475,150,50, red, lightRed, game_loop, 5)
            button("Quit", display_width-75,1,75,50, red, lightRed, exit)
        pygame.display.update()
            
            
##            if event.type == pygame.MOUSEBUTTONUP:
##                mouse = pygame.mouse.get_pos()
##                
##
##                if display_width/4-75 + 150 > mouse[0] > display_height/4-75 and 475+50 > mouse[1] > 475:
##                    pygame.draw.rect(gameDisplay, lightGreen,(display_width/4-75,475,150,50))
##                    custom_message("Selected", 30, (display_width/4), 500)
##                    pygame.display.update()
##                    time.sleep(1)
##                    return 3
##                if display_width/2-75 + 150 > mouse[0] > display_height/4-75 and 475+50 > mouse[1] > 475:
##                    pygame.draw.rect(gameDisplay, lightYellow,(display_width/2-75,475,150,50))
##                    custom_message("Selected", 30, (display_width/2), 500)
##                    pygame.display.update()
##                    time.sleep(1)
##                    return 4
##                if 3*display_width/4-75 + 150 > mouse[0] > display_height/4-75 and 475+50 > mouse[1] > 475:
##                    pygame.draw.rect(gameDisplay, lightRed,(3*display_width/4-75,475,150,50))
##                    custom_message("Selected", 30, (3*display_width/4), 500)
##                    pygame.display.update()
##                    time.sleep(1)
##                    return 5
    
            

        
        clock.tick(15)

    
        
######## THE GAME ##########
def game_loop(speed):
    crashed = False
    snake = Snake(2, 2)
    x = 2
    y = 2
    nextDirection = 'down'

    mouseX = 2 + (imgWidth+1)*random.randint(0, num_boxes-1)
    mouseY = 2 + (imgHeight+1)*random.randint(0, num_boxes-1)

    score = 1

    while not crashed:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    nextDirection = 'left'
                elif event.key == pygame.K_RIGHT:
                    nextDirection = 'right'
                elif event.key == pygame.K_UP:
                    nextDirection = 'up'
                elif event.key == pygame.K_DOWN:
                    nextDirection = 'down'
                elif event.key == pygame.K_p:
                    paused = True
                    while paused:
                        for event in pygame.event.get():
                            if event.key == pygame.K_p:
                                paused = False
##                elif event.key == pygame.K_v:
##                    score = 100
##                    crashed = True

        
        if nextDirection == 'left':
            x = x - 65
        elif nextDirection == 'right':
            x = x + 65
        elif nextDirection == 'down':
            y = y + 65
        elif nextDirection == 'up':
            y = y - 65

        

        
        gameDisplay.fill(white)
        
        if x == mouseX and y == mouseY and score != 100:
            score += 1
            snake.eat(x, y, score)

            tempBlock = snake.grid["N"][random.randint(0, 99-score)]
            mouseX = blockToPixelsX(tempBlock)
            mouseY = blockToPixelsY(tempBlock) 
                
                    
        else:
             
            if x < 0 or y < 0 or y > num_boxes*imgHeight or x > num_boxes*imgWidth:
                crashed = True
            elif snake.checkLocation(x, y, score):
                snake.move(x, y, score)
            else:
                crashed = True
        board()
        mouse(mouseX, mouseY)
        pygame.display.update()
        clock.tick(speed)

        if score == 100:
            crashed == True

    if score == 100:
        center_message("YOU WON")
    else:
        center_message("Game Over")
    score_message("Score: " + str(score))
    time.sleep(2)
    game_intro()
    



## Main

game_intro()



