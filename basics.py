import pygame
import random
import os
import time
from sys import exit

# Assets: https://www.deviantart.com/tiozacdasgalaxias/art/Link-Sprite-Sheet-662562870
# basic loop and intial sprite template: clearcode
# Background: https://htmlcolorcodes.com/colors/purple/
# background music : https://www.zapsplat.com/music/
#                       game-music-action-faced-paced-euro-style-house-rave
#                       -pumping-with-electronic-wobble-bass-synth-elements/
# click sound: https://www.zapsplat.com/music/active-studio-speaker-power-switch-click-5/
# coin sound: https://www.zapsplat.com/music/retro-8-bit-game-collect-point-00/

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
        self.pressed = False
        self.jump = False
        self.jumpCount = 0
        self.slide = False
        self.slideCount = 0

    # controls the movement of the sprite 
    # such as changing of frames 
    # and going left and right
    def update(self, key, posX, posY):
        self.currentSprite += 1
        if self.currentSprite >= len(self.sprite):
            self.currentSprite = 0
        self.image = self.sprite[self.currentSprite]

        # change number of pixel moved in one key press
        if key[pygame.K_a] and self.rect[0] - posX >= 0:
            self.pressed = True
            pygame.Rect.move_ip(self.rect, -posX, 0)
        if key[pygame.K_d] and self.rect[0] + posX <= 350:
            self.pressed = True
            pygame.Rect.move_ip(self.rect, posX, 0)

        if key[pygame.K_w] and self.jumpCount < 2:
            self.pressed = True
            self.jump = True
            self.jumpCount += 1
            # print(self.jumpCount)
            pygame.Rect.move_ip(self.rect, 0, -posY) ## to jump
        elif self.jumpCount >= 2:
            self.jump = False
            self.jumpCount = 0
            pygame.Rect.move_ip(self.rect, 0, 2*posY) ## doesnt go back down

        if key[pygame.K_s]:
            self.pressed = True
            self.slide = True
            self.slideCount += 1
            # make character slide and change sprite being used

        if pygame.key.get_pressed()[0] == False:
            self.pressed = False

# for single sliding sprite
# class Slide(pygame.sprite.Sprite):
    # def __init__(self, x, y):
    #     super().__init__()
    #     self.x = x
    #     self.y = y

    #     # other variables
    #     self.slide = False
    #     self.slideCount = 0

    #     self.sliding = pygame.image.load("linkSlide.png")
    #     self.rect = self.sliding.get_rect(midbottom = (self.x, self.y))

    # def update(self, key):

    #     # key = pygame.key.get_pressed()

    #     if key[pygame.K_s]:
    #         self.pressed = True
    #         self.slide = True
    #         self.slideCount += 1
    #         # make character slide and change sprite being used

    #     if pygame.key.get_pressed()[0] == False:
    #         self.pressed = False

    #     pass

class gameState():
    def __init__(self):
        self.state = "start"
        # self.backgroundMusic = pygame.mixer.Sound("background.mp3")
        # train variables
        trainXChoices = [50, -90, -220]
        self.trainXChoices = [50, -90, -220]
        self.trainX = random.choice(trainXChoices)
        self.trainY = -600
        trainObs = pygame.image.load("obstacles/train.png")
        self.trainObs = pygame.transform.scale(trainObs, (320, 650))
        self.trainRect = self.trainObs.get_rect(topleft = (self.trainX, self.trainY)) ######

        # jump obstacles variables
        # make a jumpY in a list with the second obstacle 
        # just a few pixels behind it
        jumpXChoices = [-30, -165, -305]
        self.jumpXChoices = [-30, -165, -305]
        self.jumpX = random.choice(jumpXChoices)
        self.jumpY = -600
        jumpObs = pygame.image.load("obstacles/jumpObs.png")
        self.jumpObs = pygame.transform.scale(jumpObs, (150, 120))
        self.jumpRect = self.jumpObs.get_rect(topleft = (self.jumpX, self.jumpY)) ######

        # slide obstacel variables
        slideXChoices = [-40, -170, -315]
        self.slideXChoices = [-40, -170, -315]
        self.slideX = random.choice(slideXChoices)
        self.slideY = -400
        slideObs = pygame.image.load("obstacles/slideObs.png") #####work on this
        self.slideObs = pygame.transform.scale(slideObs, (150, 120))
        self.slideRect = self.slideObs.get_rect(topleft = (self.slideX, self.slideY))

        # button variables
        self.easyButton = pygame.image.load("buttons/easy.png")
        self.normalButton = pygame.image.load("buttons/normal.png")
        self.hardButton = pygame.image.load("buttons/hard.png")

        self.easyButton2 = pygame.image.load("buttons/easy2.png")
        self.normalButton2 = pygame.image.load("buttons/normal2.png")
        self.hardButton2 = pygame.image.load("buttons/hard2.png")

        self.rectEasy = self.easyButton.get_rect(topleft = (170, 469))
        self.rectNormal = self.normalButton.get_rect(topleft = ((170, 564)))
        self.rectHard = self.hardButton.get_rect(topleft = ((170, 664)))
        self.click = False
        self.clickSound = pygame.mixer.Sound("click.mp3")

    def button(self):
        if self.rectEasy.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.state = "gameState"
                self.clickSound.play()
        if self.rectNormal.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.state = "gameState"
                self.clickSound.play()
        if self.rectHard.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.state = "gameState"
                self.clickSound.play()

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(gameBackground, (0, 0))
        # need to add restart button
        # need to add score
        # pass

    def game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # collide.rect only takes in rect
        # to prevent overlapping
        # if pygame.Rect.colliderect(self.jumpRect, self.trainRect):
        #     self.jumpX = random.choice(self.jumpXChoices)

        # if pygame.Rect.colliderect(self.slideRect, self.trainRect) and \
        #     pygame.Rect.colliderect(self.slideRect, self.jumpRect):
        #     self.slideX = random.choice(self.slideXChoices)
        
        if self.trainY < 750:
            self.trainY += 20
        else:
            # spawn train in random location
            self.trainY = -600
            self.trainX = random.choice(self.trainXChoices)

        if self.jumpY < 750:
            self.jumpY += 20
        else:
            # spawn jumps in random location
            self.jumpY = -400
            self.jumpX = random.choice(self.jumpXChoices)

        if self.slideY < 750:
            self.slideY += 20
        else:
            # spawn slides in random location
            self.slideY = -750
            self.slideX = random.choice(self.slideXChoices)

        screen.blit(background, (0, 0)) # coordinates x1 y1
        screen.blit(trainObs, (-self.trainX, self.trainY))
        screen.blit(jumpObs, (-self.jumpX, self.jumpY))
        screen.blit(slideObs, (-self.slideX, self.slideY))

        linkRun.draw(screen)
        linkRun.update(pygame.key.get_pressed(), 70, 50)
        pygame.display.update()
        pygame.display.flip() # make running look more smoother

    def stateControl(self):
        if self.state == "start":
            self.startPage()
        if self.state == "gameState":
            self.game()
        if self.state == "over":
            self.gameOverPage

# general setup
width = 500
height = 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Metro Maniacs")
# intro background through image
background = pygame.image.load("purple.png")
# game call
gameState1 = gameState()

# intro variables
introBackground = pygame.Surface((width, height))
introBackground.fill((206, 147, 216))
introText = pygame.image.load("metroManiacs.png")

# outro variables
gameBackground = pygame.Surface((width, height))
gameBackground.fill((255, 255, 102))

# train variables
trainObs = pygame.image.load("obstacles/train.png")
trainObs = pygame.transform.scale(trainObs, (320, 650))

# jump variables
jumpObs = pygame.image.load("obstacles/jumpObs.png")
jumpObs = pygame.transform.scale(jumpObs, (150, 120))

# slide variables
slideObs = pygame.image.load("obstacles/slideObs.png") #####work on this
slideObs = pygame.transform.scale(slideObs, (150, 120))

# running sprite pics
linkRun = pygame.sprite.Group()
running = Running(width/2, height - 100)
linkRun.add(running) # add the sprites at this position

# sliding sprite pics
# linkSlides = pygame.sprite.GroupSingle()
# sliding = Slide()

# main loop
running = True
while running:
    gameState1.stateControl()
    # gameState1.gameOverPage()
    clock.tick(15)

