import pygame
import random
import os
import time
from sys import exit, get_asyncgen_hooks

from pygame import rect

# Assets: https://www.deviantart.com/tiozacdasgalaxias/art/Link-Sprite-Sheet-662562870
# coin asset: https://totuslotus.itch.io/pixel-coins
# basic loop and intial sprite template: https://youtu.be/MYaxPa_eZS0
# Background: https://htmlcolorcodes.com/colors/purple/
# background music : https://www.zapsplat.com/music/
#                       game-music-action-faced-paced-euro-style-house-rave
#                       -pumping-with-electronic-wobble-bass-synth-elements/
# click sound: https://www.zapsplat.com/music/active-studio-speaker-power-switch-click-5/
# coin sound: https://www.zapsplat.com/music/retro-8-bit-game-collect-point-00/
# resizing pixels of images: https://lospec.com/pixel-art-scaler/

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
        global rectRun
        rectRun = self.rect

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
        self.i = 0

        self.sliding = pygame.image.load("linkSlide.png")
        self.rect = self.sliding.get_rect(midbottom = (self.x, self.y))

        # other variables
        self.slide = False
        self.onRight = False
        self.onLeft = False

    def update(self, posX):
        if self.slide and self.onLeft == False and self.onRight == False:
            # remove old sprite
            # use a counter to make longer
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

class Coins(pygame.sprite.Sprite):
    def __init__(self, coinImg):
        super().__init__()

        pygame.sprite.Sprite.remove(coinImg)


class gameState():
    def __init__(self):
        self.state = "start"
        # train variables
        trainXChoices = [30, 185, 320]
        self.trainXChoices = [30, 185, 320]
        self.trainX = random.choice(trainXChoices)
        self.trainY = -600
        self.trainObs = pygame.image.load("obstacles/train.png")
        self.trainRect = self.trainObs.get_rect(topleft = (self.trainX, self.trainY))

        # jump obstacles variables
        # make a jumpY in a list with the second obstacle 
        # just a few pixels behind it
        jumpXChoices = [60, 195, 350]
        self.jumpXChoices = [60, 195, 350]
        self.jumpX = random.choice(jumpXChoices)
        self.jumpY = -600
        self.jumpObs = pygame.image.load("obstacles/jumpObs.png")
        self.jumpRect = self.jumpObs.get_rect(topleft = (self.jumpX, self.jumpY))
        self.collideJump = False

        # slide obstacel variables
        slideXChoices = [43, 180, 330]
        self.slideXChoices = [43, 180, 330]
        self.slideX = random.choice(slideXChoices)
        self.slideY = -400
        self.slideObs = pygame.image.load("obstacles/slideObs.png")
        self.slideRect = self.slideObs.get_rect(topleft = (self.slideX, self.slideY))
        self.collideSlide = False

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

        # playerRect
        self.x = width/2
        self.y = height - 100
        self.sliding = pygame.image.load("linkSlide.png")
        self.rect = self.sliding.get_rect(midbottom = (self.x, self.y))

        # coin
        coinXChoices = [80, 230, 370]
        self.coinXChoices = [80, 230, 370]
        self.coinX = random.choice(coinXChoices)
        self.coinY = 0
        self.coin = pygame.image.load("coin.png")

        self.coinRect = self.coin.get_rect(topleft = (self.coinX, self.coinY))

        global coin, coinRect
        coin = self.coin
        coinRect = self.coinRect

    def scoring(self):
        global score, gameSpeed
        # print(score, gameSpeed)
        score += 1
        if score % 100 == 0 and gameState == "start":
            gameSpeed += 5

        text = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
         f"Score: {score}", True, (0, 0, 0))
        screen.blit(text, (width - 150, 50))

    def updateScores(self):
        f = open('scores.txt','r')
        file = f.readlines()
        last = int(file[0])
        if last < int(score):
            f.close() 
            file = open('scores.txt', 'w') 
            file.write(str(score)) 
            file.close() 
            return score       
        return last

    # def totalCoins(self):
    #     global coins
    #     if self.coinRect.colliderect(rectRun): # remove sprite
    #         coins += coins//8
    #         # pygame.sprite.Sprite.remove(self.coin)
    #         print(coins)

    def collision(self):
        global coins
        # global coins
        # running sprite
        if self.trainRect.colliderect(rectRun):
            print("collided!")
            self.state = "over"

        # sliding sprite
        if self.slideRect.colliderect(rectRun) and self.collideSlide != True:
            print("didnt slide!")
            self.state = "over"
        
        # jump sprite
        if self.jumpRect.colliderect(rectRun) and self.collideJump != True:
            print("didn't jump")
            self.state = "over"

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
        currentScore = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
         f"Score: {score}", True, (0, 0, 0))
        currentCoins = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
         f"Coins Collected: {coins}", True, (0, 0, 0))
        highscore = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
         f"Highscore: {self.updateScores()}", True, (0, 0, 0))
        screen.blit(currentScore, (width/2- 50, height/2))
        screen.blit(currentCoins, (width/2- 100, height/2 + 100))
        screen.blit(highscore, (width/2- 100, height/2 + 200))
        pygame.display.update()
        pygame.display.flip()
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
                    self.collideJump = True

                if event.unicode == "s":
                    slidingLink.slide = True
                    self.collideSlide = True

            if event.type == pygame.KEYUP:
                if event.unicode == "w":
                    runningLink.jumpDown = True
                # hold key to continue jumping
                if event.unicode == "w":
                    self.collideJump = False
                if event.unicode == "s":
                    self.collideSlide = False

        # if collide with player
        self.collision()

        # collide.rect only takes in rect
        if pygame.Rect.colliderect(self.slideRect, self.trainRect) and \
            pygame.Rect.colliderect(self.slideRect, self.jumpRect):
            self.jumpX = random.choice(self.jumpXChoices)

        if pygame.Rect.colliderect(self.jumpRect, self.trainRect) and \
            pygame.Rect.colliderect(self.slideRect, self.jumpRect):
            self.slideX = random.choice(self.slideXChoices)

        if self.coinY < 750:
            self.coinY += 20 + gameSpeed
            self.coinRect = self.coin.get_rect(topleft = (self.coinX, self.coinY))
        else:
            self.coinY = 0
        
        if self.trainY < 750:
            self.trainY += 20 + gameSpeed
            self.trainRect = self.trainObs.get_rect(topleft = (self.trainX, self.trainY - 10))
        else:
            # spawn train in random location
            self.trainY = -600
            self.trainX = random.choice(self.trainXChoices)

        if self.jumpY < 750:
            self.jumpY += 20 + gameSpeed
            self.jumpRect = self.jumpObs.get_rect(topleft = (self.jumpX, self.jumpY))
        else:
            # spawn jumps in random location
            self.jumpY = -600
            self.jumpX = random.choice(self.jumpXChoices)

        if self.slideY < 750:
            self.slideY += 20 + gameSpeed
            self.rect = self.sliding.get_rect(midbottom = (self.x, self.y))
        else:
            # spawn slides in random location
            self.slideY = -750
            self.slideX = random.choice(self.slideXChoices)

        screen.blit(background, (0, 0)) # coordinates x1 y1

        screen.blit(coin, (self.coinX, self.coinY)) # temporary

        screen.blit(trainObs, (self.trainX, self.trainY))
        screen.blit(jumpObs, (self.jumpX, self.jumpY))
        linkSlides.draw(screen)
        linkRun.draw(screen)
        screen.blit(slideObs, (self.slideX, self.slideY)) # won't collide with link
        linkRun.update(140, 70)
        slidingLink.update(140)

        # pygame.draw.rect(screen, (0, 255, 0), self.slideRect)
        pygame.draw.rect(screen, (255, 255, 255), (width - 175, 40, 150, 50))
        self.scoring()
        pygame.display.update()
        pygame.display.flip() # make running look more smoother

    def stateControl(self):
        if self.state == "start":
            self.startPage()
        if self.state == "gameState":
            self.game()
        if self.state == "over":
            self.gameOverPage()

# general setup
width = 500
height = 800
score = 0
gameSpeed = 0
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

# jump variables
jumpObs = pygame.image.load("obstacles/jumpObs.png")

# slide variables
slideObs = pygame.image.load("obstacles/slideObs.png") 

# coin variables
coin = pygame.image.load("coin.png")
coins = 0

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

