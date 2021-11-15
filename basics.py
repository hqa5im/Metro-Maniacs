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
        self.moveLeft = False
        self.moveRight = False
        self.jump = False
        self.jumpDown = False

    # controls the movement of the sprite 
    # such as changing of frames 
    # and going left and right
    def update(self, posX, posY):
        self.currentSprite += 1
        if self.currentSprite >= len(self.sprite):
            self.currentSprite = 0
        self.image = self.sprite[self.currentSprite]

        if self.moveLeft and self.rect[0] - posX >= 0:
            pygame.Rect.move_ip(self.rect, -posX, 0)
            self.moveLeft = False

        if self.moveRight and self.rect[0] + posX <= 350:
            pygame.Rect.move_ip(self.rect, posX, 0)
            self.moveRight = False

        if self.jump:
            pygame.Rect.move_ip(self.rect, 0, -posY)
            self.jump = False
        
        if self.jumpDown:
            pygame.Rect.move_ip(self.rect, 0, posY)
            self.jumpDown = False

# for single sliding sprite
class Slide(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        self.sliding = pygame.image.load("linkSlide.png")
        self.rect = self.sliding.get_rect(midbottom = (self.x, self.y))

        # other variables
        self.slide = False
        self.onRight = False
        self.onLeft = False

    def update(self, posX):
        if self.slide and self.onLeft == False and self.onRight == False:
            # remove old sprite
            # maybe make a list of those so stays longer
            screen.blit(self.sliding, (self.rect[0], self.rect[1]))
            self.slide = False

        elif self.slide == True and self.onRight == True:
            screen.blit(self.sliding, (self.rect[0] + posX, self.rect[1]))
            self.slide = False
            self.onRight = False
            self.onLeft = False
        elif self.slide == True and self.onLeft == True:
            screen.blit(self.sliding, (self.rect[0] - posX, self.rect[1]))
            self.slide = False
            self.onLeft = False
            self.onRight = False

class gameState():
    def __init__(self):
        self.state = "start"
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

    def collision(self):
        pass

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

            if event.type == pygame.KEYDOWN:
                if event.unicode == "a":
                    runningLink.moveLeft = True
                    slidingLink.onLeft = True
                    slidingLink.onRight = False

                if event.unicode == "d":
                    runningLink.moveRight = True
                    slidingLink.onRight = True
                    slidingLink.onLeft = False

                if event.unicode == "w":
                    runningLink.jump = True

                if event.unicode == "s":
                    print("sliding!")
                    slidingLink.slide = True

            if event.type == pygame.KEYUP:
                if event.unicode == "w":
                    runningLink.jumpDown = True

        # collide.rect only takes in rect
        if pygame.Rect.colliderect(self.slideRect, self.trainRect) and \
            pygame.Rect.colliderect(self.slideRect, self.jumpRect):
            self.jumpX = random.choice(self.jumpXChoices)

        if pygame.Rect.colliderect(self.slideRect, self.trainRect) and \
            pygame.Rect.colliderect(self.slideRect, self.jumpRect):
            self.slideX = random.choice(self.slideXChoices)
        
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
            self.jumpY = -600
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
        linkSlides.draw(screen)
        linkRun.draw(screen)
        screen.blit(slideObs, (-self.slideX, self.slideY))
        linkRun.update(140, 70)

        slidingLink.update(140)

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
runningLink = Running(width/2, height - 100)
linkRun.add(runningLink) # add the sprites at this position

# sliding sprite pics
linkSlides = pygame.sprite.GroupSingle()
slidingLink = Slide(width/2, height - 100)
linkSlides.add(linkSlides)

# main loop
running = True
while running:
    gameState1.stateControl()
    # gameState1.gameOverPage()
    clock.tick(15)

