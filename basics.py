import pygame
import random
import os
import time
from sys import exit

# Assets: https://www.deviantart.com/tiozacdasgalaxias/art/Link-Sprite-Sheet-662562870
# Background: https://htmlcolorcodes.com/colors/purple/

pygame.init()

# creating a class for sprites
class Running(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.sprite = []
        self.sprite.append(pygame.image.load("linkRunningSprites/Link1.png"))
        self.sprite.append(pygame.image.load("linkRunningSprites/Link2.png"))
        self.sprite.append(pygame.image.load("linkRunningSprites/Link3.png"))
        self.sprite.append(pygame.image.load("linkRunningSprites/Link4.png"))
        self.sprite.append(pygame.image.load("linkRunningSprites/Link5.png"))
        self.sprite.append(pygame.image.load("linkRunningSprites/Link6.png"))
        self.sprite.append(pygame.image.load("linkRunningSprites/Link7.png"))
        self.sprite.append(pygame.image.load("linkRunningSprites/Link8.png"))
        self.sprite.append(pygame.image.load("linkRunningSprites/Link9.png"))
        self.sprite.append(pygame.image.load("linkRunningSprites/Link10.png"))
        self.currentSprite = 0
        self.image = self.sprite[self.currentSprite]

        # starting position
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))

        # other variables 
        self.jump = False
        self.jumpCount = 0

    # controls the movement of the sprite 
    # such as changing of frames 
    # and going left and right
    def update(self, key, posX, posY):
        self.currentSprite += 1
        if self.currentSprite >= len(self.sprite):
            self.currentSprite = 0
        self.image = self.sprite[self.currentSprite]

        if key[pygame.K_a] and self.rect[0] - posX >= 0:
            pygame.Rect.move_ip(self.rect, -posX, 0)
        if key[pygame.K_d] and self.rect[0] + posX <= 350:
            pygame.Rect.move_ip(self.rect, posX, 0)
        if key[pygame.K_w] and self.jumpCount < 3:
            self.jump = True
            self.jumpCount += 1
            print(self.jumpCount)
            pygame.Rect.move_ip(self.rect, 0, -posY) ## to jump
        else:
            self.jump = False
            pygame.Rect.move_ip(self.rect, 0, 0) ## doesnt go back down


# trainObs = pygame.image.load("obstacles/train.png")
# slideObs = pygame.image.load("obstacles/slideObs.png")
# jumpObs = pygame.image.load("obstacles/jumpObs.png")

class gameState():
    def __init__(self):
        self.state = "start"
        # train variables
        trainXChoices = [50, -90, -220]
        self.trainX = random.choice(trainXChoices)
        self.trainY = -600
        self.easyButton = pygame.image.load("buttons/easy.png")
        self.normalButton = pygame.image.load("buttons/normal.png")
        self.hardButton = pygame.image.load("buttons/hard.png")

        self.rectEasy = self.easyButton.get_rect(topleft = (170, 469))
        print(self.rectEasy)
        self.rectNormal = self.normalButton.get_rect(topleft = ((170, 564)))
        self.rectHard = self.hardButton.get_rect(topleft = ((170, 664)))
        self.click = False

    def button(self):
        # add click sound effect
        if self.rectEasy.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.state = "gameState"
        if self.rectNormal.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.state = "gameState"
        if self.rectHard.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.state = "gameState"

        if pygame.mouse.get_pressed()[0] == False:
            self.click = False

    def startPage(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            self.button()
        
        screen.blit(introBackground, (0, 0))
        screen.blit(introText, (-10, 50))

        screen.blit(self.easyButton, (150, 450))
        screen.blit(self.normalButton, (155, 550))
        screen.blit(self.hardButton, (157, 650))
        pygame.display.update()
        pygame.display.flip()

    def gameOverPage(self):
        pass

    def game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if self.trainY < 750:
            self.trainY += 20
        else:
            # remove train and spawn new train 
            # in random location
            self.trainY = -600
            
        screen.blit(background, (0, 0)) # coordinates x1 y1
        screen.blit(trainObs, (-self.trainX, self.trainY))

        linkRun.draw(screen)
        linkRun.update(pygame.key.get_pressed(), 70, 50)
        pygame.display.update()
        pygame.display.flip() # make running look more smoother

    def stateControl(self):
        if self.state == "start":
            self.startPage()
        if self.state == "gameState":
            self.game()

# general setup
width = 500
height = 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Metro Maniacs")
# background through image
background = pygame.image.load("purple.png")
gameState1 = gameState()

# intro variables
introBackground = pygame.Surface((width, height))
introBackground.fill((206, 147, 216))
introText = pygame.image.load("metroManiacs.png")

# train variables
# needs to move and randomize
trainObs = pygame.image.load("obstacles/train.png")
trainObs = pygame.transform.scale(trainObs, (320, 650))

# running sprite pics
linkRun = pygame.sprite.Group()
running = Running(width/2, height - 100)
linkRun.add(running) # add the sprites at this position

# main loop
running = True
while running:
    gameState1.stateControl()
    # gameState1.game()
    clock.tick(15)







