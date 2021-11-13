import pygame
import random
import os
import time
from sys import exit

pygame.init()

width = 500
height = 800

# Assets: https://www.deviantart.com/tiozacdasgalaxias/art/Link-Sprite-Sheet-662562870

# Background: https://htmlcolorcodes.com/colors/purple/

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

# class Obstacles(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.trainObs = pygame.image.load("obstacles/train.png")
#         self.slideObs = pygame.image.load("obstacles/slideObs.png")
#         self.jumpObs = pygame.image.load("obstacles/jumpObs.png")

def mainLoop():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Metro Maniacs")

    # background through image
    background = pygame.image.load("purple.png")

    # train variables
    # needs to move and randomize
    trainXChoices = [50, -90, -220]
    trainX = random.choice(trainXChoices)
    trainY = -600
    trainObs = pygame.image.load("obstacles/train.png")
    trainObs = pygame.transform.scale(trainObs, (320, 650))

    # running sprite pics
    linkRun = pygame.sprite.Group()
    running = Running(width/2, height - 100)
    linkRun.add(running) # add the sprites at this position

    # general setup
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if trainY < 750:
            trainY += 20
        else:
            # remove train and spawn new train 
            # in random location
            trainY = -600
            
        screen.blit(background, (0, 0)) # coordinates x1 y1
        screen.blit(trainObs, (-trainX, trainY))

        linkRun.draw(screen)
        linkRun.update(pygame.key.get_pressed(), 70, 50)
        pygame.display.update()
        pygame.display.flip() # make running look more smoother
        clock.tick(15)

mainLoop()





