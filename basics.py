from os import name
import pygame
import random
from sys import exit

# Asset Link: https://www.deviantart.com/tiozacdasgalaxias/art/Link-Sprite-Sheet-662562870
# Asset Sonic: https://mb.srb2.org/threads/adventure-sonic-sa-sonic-progress.29955/page-5
# Asset Other Characters: https://www.deviantart.com/dudeanime21/
#                           art/SMBZ-Backview-Running-Sprites-614481455
#https://www.deviantart.com/dudeanime21/art/SMBZ-Forward-Run-Sprites-597217977
        
# coin asset: https://totuslotus.itch.io/pixel-coins
# basic loop and intial sprite template: https://youtu.be/MYaxPa_eZS0
# Background: https://htmlcolorcodes.com/colors/purple/
# background music : https://www.zapsplat.com/music/
#                       game-music-action-faced-paced-euro-style-house-rave
#                       -pumping-with-electronic-wobble-bass-synth-elements/
# click sound: https://www.zapsplat.com/music/active-studio-speaker-power-switch-click-5/
# slide sound:
# jump sound: 
# powerup sound:
# coin sound: https://www.zapsplat.com/music/retro-8-bit-game-collect-point-00/
# resizing pixels of images: https://lospec.com/pixel-art-scaler/
# high score method: https://www.techwithtim.net/tutorials/game
#                   -development-with-python/pygame-tutorial/scoring-health-bars/

pygame.init()

# creating a class for sprites
class Running(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.x = x
        self.y = y

        self.sprite = []
        self.sprite.append(pygame.image.load(f"linkRunningSprites/{name}1.png"))
        self.sprite.append(pygame.image.load(f"linkRunningSprites/{name}2.png"))
        self.sprite.append(pygame.image.load(f"linkRunningSprites/{name}3.png"))
        self.sprite.append(pygame.image.load(f"linkRunningSprites/{name}4.png"))
        self.sprite.append(pygame.image.load(f"linkRunningSprites/{name}5.png"))
        self.sprite.append(pygame.image.load(f"linkRunningSprites/{name}6.png"))
        self.sprite.append(pygame.image.load(f"linkRunningSprites/{name}7.png"))
        self.sprite.append(pygame.image.load(f"linkRunningSprites/{name}8.png"))
        self.sprite.append(pygame.image.load(f"linkRunningSprites/{name}9.png"))
        self.sprite.append(pygame.image.load(f"linkRunningSprites/{name}10.png"))
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
    def __init__(self, x, y, name):
        super().__init__()
        self.x = x
        self.y = y

        self.i = 0

        self.sliding = pygame.image.load(f"slides/{name}Slide.png")
        self.rect = self.sliding.get_rect(midbottom = (self.x, self.y))

        # other variables
        self.slide = False

    def update(self):
        if self.slide == True and self.i < 10:
            screen.blit(self.sliding, (rectRun[0], rectRun[1]))
            self.i += 1
        else:
            self.i = 0
            self.slide = False

class gameState():
    def __init__(self):
        global coins, score, gameSpeed ############
        # player variables !!!!
        self.name = "Link"
        self.linkRun = pygame.sprite.Group()
        self.runningLink = Running(width/2, height - 100, self.name)
        self.linkRun.add(self.runningLink) # add the sprites at this position
        
        self.linkSlides = pygame.sprite.GroupSingle()
        self.slidingLink = Slide(width/2, height - 100, self.name)
        self.linkSlides.add(self.linkSlides)

        self.i = 0
        self.num = 0
        self.state = "start"
        self.updateCoin = True
        self.fail = pygame.image.load("fail.png")
        self.unbuy = False
        self.slideSound = pygame.mixer.Sound("slideSound.mp3")
        self.jumpSound = pygame.mixer.Sound("jumpSound.mp3")
        self.powerUp = pygame.mixer.Sound("powerUp.mp3")

        # train 1 variables
        self.trainXChoices = [30, 185, 320]
        self.trainX = random.choice(self.trainXChoices)
        self.trainY = -600
        self.trainObs = pygame.image.load("obstacles/train.png")
        self.trainRect = self.trainObs.get_rect(topleft = (self.trainX, self.trainY))

        # train 2 variables - for hard mode
        self.train2XChoices = [30, 185, 320]
        self.train2X = random.choice(self.train2XChoices)
        self.train2Y = random.randint(-1200, -600)
        self.train2Obs = pygame.image.load("obstacles/train.png")
        self.train2Rect = self.train2Obs.get_rect(topleft = (self.train2X, self.train2Y))

        # jump 1 obstacles
        self.jumpXChoices = [60, 195, 350]
        self.jumpX = random.choice(self.jumpXChoices)
        self.jumpY = -600
        self.jumpObs = pygame.image.load("obstacles/jumpObs.png")
        self.jumpRect = self.jumpObs.get_rect(topleft = (self.jumpX, self.jumpY))
        self.collideJump = False

        # jump 2 obstacles - for hard mode
        self.jump2XChoices = [60, 195, 350]
        self.jump2X = random.choice(self.jump2XChoices)
        self.jump2Y = random.randint(-1200, -600)
        self.jump2Obs = pygame.image.load("obstacles/jumpObs.png")
        self.jump2Rect = self.jump2Obs.get_rect(topleft = (self.jump2X, self.jump2Y))

        # slide 1 variables
        self.slideXChoices = [43, 180, 330]
        self.slideX = random.choice(self.slideXChoices)
        self.slideY = -400
        self.slideObs = pygame.image.load("obstacles/slideObs.png")
        self.slideRect = self.slideObs.get_rect(topleft = (self.slideX, self.slideY))
        self.collideSlide = False

        # slide 2 variables
        self.slide2XChoices = [43, 180, 330]
        self.slide2X = random.choice(self.slide2XChoices)
        self.slide2Y = random.randint(-1200, -600)
        self.slide2Obs = pygame.image.load("obstacles/slideObs.png")
        self.slide2Rect = self.slide2Obs.get_rect(topleft = (self.slide2X, self.slide2Y))

        # button variables
        self.easyButton = pygame.image.load("buttons/easy.png")
        self.normalButton = pygame.image.load("buttons/normal.png")
        self.hardButton = pygame.image.load("buttons/hard.png")
        self.shopButton = pygame.image.load("buttons/shop.png")
        self.restartButton = pygame.image.load("buttons/restart.png")

        self.rectEasy = self.easyButton.get_rect(topleft = (170, 469))
        self.rectNormal = self.normalButton.get_rect(topleft = ((170, 564)))
        self.rectHard = self.hardButton.get_rect(topleft = ((170, 664)))
        self.rectShop = self.shopButton.get_rect(topleft = ((170, 764)))
        self.click = False
        self.clickSound = pygame.mixer.Sound("click.mp3")
        self.rectRestart = self.restartButton.get_rect(topleft = (150, 600)) # for now

        # shop buttons
        self.linkButton = pygame.image.load("buttons/Link.png")
        self.sonicButton = pygame.image.load("buttons/Sonic.png")
        self.marioButton = pygame.image.load("buttons/mario.png")
        self.shopText1 = pygame.image.load("shopText1.png")
        self.shopText2 = pygame.image.load("shopText2.png")

        self.rectLink = self.linkButton.get_rect(topleft = (153, 252))
        self.rectSonic = self.sonicButton.get_rect(topleft = (153, 353))
        self.rectMario = self.marioButton.get_rect(topleft = (153, 453))
        self.buySonic = False
        self.buyMario = False
        self.buy = False

        # playerRect
        self.x = width/2
        self.y = height - 100
        self.sliding = pygame.image.load("slides/linkSlide.png")
        self.rect = self.sliding.get_rect(midbottom = (self.x, self.y))

        # boosters
        # jetapack - with jetpack comes 100 coins
        self.jetpackXChoices = [80, 230, 370]
        self.jetpackX = random.choice(self.jetpackXChoices)
        self.jetpackY = -1000
        self.jetpack = pygame.image.load("boosters/jetpack.png")
        self.jetpackRect = self.jetpack.get_rect(topleft = (self.jetpackX, self.jetpackY))
        self.jets = False
        self.jetButton = pygame.image.load("buttons/boosterButton.png")
        self.theJet = pygame.image.load("theJet.png")

        # extra life
        self.extraLifeXChoices = [80, 230, 370]
        self.extraLifeX = random.choice(self.extraLifeXChoices)
        self.extraLifeY = -1500
        self.extraLife = pygame.image.load("boosters/extraLife.png")
        self.extraLifeRect = self.extraLife.get_rect(topleft = (self.extraLifeX, self.extraLifeY))
        self.lives = False
        self.numLives = 0
        self.extraButton = pygame.image.load("buttons/extraButton.png")

        # coin 1
        self.coinXChoices = [80, 230, 370]
        self.coinX = random.choice(self.coinXChoices)
        self.coinY = random.randint(-300, 0)
        self.coin = pygame.image.load("coin.png")
        self.coinRect = self.coin.get_rect(topleft = (self.coinX, self.coinY))

        # coin 2
        self.coin2XChoices = [80, 230, 370]
        self.coin2X = random.choice(self.coin2XChoices)
        self.coin2Y = random.randint(-300, 0)
        self.coin2 = pygame.image.load("coin.png")
        self.coin2Rect = self.coin2.get_rect(topleft = (self.coin2X, self.coin2Y))

        # coin 3
        self.coin3XChoices = [80, 230, 370]
        self.coin3X = random.choice(self.coin3XChoices)
        self.coin3Y = random.randint(-300, 0)
        self.coin3 = pygame.image.load("coin.png")
        self.coin3Rect = self.coin3.get_rect(topleft = (self.coin3X, self.coin3Y))

        # coin 4
        self.coin4XChoices = [80, 230, 370]
        self.coin4X = random.choice(self.coin4XChoices)
        self.coin4Y = random.randint(-300, 0)
        self.coin4 = pygame.image.load("coin.png")
        self.coin4Rect = self.coin3.get_rect(topleft = (self.coin4X, self.coin4Y))

        self.coinSound = pygame.mixer.Sound("coin.mp3")

    def scoring(self):
        global score, gameSpeed
        score += 1
        if score % 100 == 0:
            gameSpeed += 1

        text = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
         f"Score: {score}", True, (0, 0, 0))
        screen.blit(text, (width - 150, 50))

    def jetCounter(self):
 
        text = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 24),
         f"{10 - (self.num)}", True, (0, 0, 0))
        screen.blit(text, (50, 50))

    def lifeCount(self):
        text = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
         f"{self.numLives}", True, (0, 0, 0))
        screen.blit(text, (50, 110))


    def coinTotal(self):
        global coins
        text = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
         f"Coins: {coins}", True, (0, 0, 0))
        screen.blit(text, (width - 150, 80))

    # high score for easy
    def updateScoresEasy(self):
        self.stateScore = "easy"
        f = open('scores.txt','r')
        file = f.readlines()
        last = int(file[0])
        if last < int(score):
            f.close() 
            file = open('scores.txt', 'w') 
            file.write(str(score)) 
            file.close() 
            return score
        f.close()       
        return last

    # high score for hard
    # def updateScoresHard(self):
    #     self.stateScore = "hard"
    #     f = open('scoresHard.txt','r')
    #     file = f.readlines()
    #     last = int(file[0])
    #     if last < int(score):
    #         f.close() 
    #         file = open('scoresHard.txt', 'w') 
    #         file.write(str(score)) 
    #         file.close() 
    #         return score       
    #     return last

    # sum of coins
    # use for buying characters 
    def updateCoins(self):
        f = open('coins.txt','r') 
        file = f.readline()
        f.close()
        f = open('coins.txt','w')
        # print(coins)
        tot = int(file) + coins
        if tot <= 0:
            tot = 0
        tot = str(tot)
        f.write(tot)
        f.close()
        return tot

    def readCoins(self):
        f = open('coins.txt', 'r')
        file = f.readline()
        tot = int(file)
        if tot <= 0:
            tot = 0
        tot = str(tot)
        f.close()
        return tot

    def updateShopCoins(self):
        tot = int(self.readCoins()) + coins
        f = open('coins.txt', 'w')
        if tot <= 0:
            tot = 0
        tot = str(tot)
        f.write(tot)
        f.close()
        return tot

    def bank(self):
        money = self.readCoins()
        text = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
         f"Coins: {money}", True, (0, 0, 0))
        screen.blit(text, (width - 150, 80))

    def collision(self):
        global coins
        # running sprite
        if self.trainRect.colliderect(rectRun) and self.jets == False and self.numLives <= 0 and self.lives == False:
            self.state = "over"
        elif self.jets == True:
            self.i += 1
        elif self.trainRect.colliderect(rectRun) and self.numLives > 0 and self.lives == True:
            self.numLives -= 1
            self.trainY -= 500 ## move other ojects with it

        # sliding sprite
        if self.slideRect.colliderect(rectRun) and self.collideSlide != True and \
             self.jets == False and self.numLives <= 0 and self.lives == False:
            self.state = "over"
        elif self.jets == True:
            self.i += 1
        elif self.slideRect.colliderect(rectRun) and self.numLives > 0 and self.lives == True:
            self.numLives -= 1
            self.slideY -= 500
        
        # jump sprite
        if self.jumpRect.colliderect(rectRun) and self.collideJump != True and \
            self.jets == False and self.numLives <= 0 and self.lives == False:
            self.state = "over"
        elif self.jets == True:
            self.i += 1
        elif self.jumpRect.colliderect(rectRun) and self.numLives > 0 and self.lives == True:
            self.numLives -= 1
            self.jumpY -= 500

        # train hard
        if self.train2Rect.colliderect(rectRun) and self.jets == False and self.numLives <= 0 and self.lives == False:
            self.state = "over"
        elif self.jets == True:
            self.i += 1
        elif self.train2Rect.colliderect(rectRun) and self.numLives > 0 and self.lives == True:
            self.numLives -= 1
            self.train2Y -= 500

        # slide hard
        if self.slide2Rect.colliderect(rectRun) and self.collideSlide != True and \
            self.jets == False and self.numLives <= 0 and self.lives == False:
            self.state = "over"
        elif self.jets == True:
            self.i += 1
        elif self.slide2Rect.colliderect(rectRun) and self.numLives > 0 and self.lives == True:
            self.numLives -= 1
            self.slide2Y -= 500
            ## move the object some distance back or have no collsion enabled for short time period

        # jump hard
        if self.jump2Rect.colliderect(rectRun) and self.collideJump != True and \
            self.jets == False and self.numLives <= 0 and self.lives == False:
            self.state = "over"
        elif self.jets == True:
            self.i += 1
        elif self.jump2Rect.colliderect(rectRun) and self.numLives > 0 and self.lives == True:
            self.numLives -= 1
            self.jump2Y -= 500

        # coin collision
        if self.coinRect.colliderect(rectRun):
            self.coinY = random.randint(-300, 0)
            self.coinX = random.choice(self.coinXChoices)
            self.coinSound.play()
            coins += 1

        if self.coin2Rect.colliderect(rectRun):
            self.coin2Y = random.randint(-300, 0)
            self.coin2X = random.choice(self.coin2XChoices)
            self.coinSound.play()
            coins += 1

        if self.coin3Rect.colliderect(rectRun):
            self.coin3Y = random.randint(-300, 0)
            self.coin3X = random.choice(self.coin3XChoices)
            self.coinSound.play()
            coins += 1

        if self.coin4Rect.colliderect(rectRun):
            self.coin4Y = random.randint(-300, 0)
            self.coin4X = random.choice(self.coin4XChoices)
            self.coinSound.play()
            coins += 1

        # collison with boosters
        if self.jetpackRect.colliderect(rectRun) and self.i < 100:
            self.jetpackY = - 2000
            self.jetpackX = random.choice(self.jetpackXChoices)
            coins += 100
            self.jets = True
            self.powerUp.play()
        elif self.i >= 1000:
            self.i = 0
            self.jets = False
        
        if self.extraLifeRect.colliderect(rectRun):
            self.extraLifeY = - 2500
            self.extraLifeX = random.choice(self.extraLifeXChoices)
            self.lives = True
            self.numLives += 1
            self.powerUp.play()
        elif self.numLives <= 0:
            self.lives = False
    
    # add something here for different high scores
    def button(self):
        if self.rectEasy.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.state = "gameStateEasy"
                self.clickSound.play()
        if self.rectNormal.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.state = "gameStateNormal"
                self.clickSound.play()
        if self.rectHard.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.state = "gameStateHard"
                self.clickSound.play()
        if self.rectShop.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.state = "shop"
                self.clickSound.play()

        if pygame.mouse.get_pressed()[0] == False:
            self.click = False

    def startPage(self):
        self.updateCoin = True

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
        screen.blit(self.shopButton, (170, 750))
        pygame.display.update()
        pygame.display.flip()

    def shop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            self.shopButtons(event)

        screen.blit(gameBackground, (0, 0))
        screen.blit(self.linkButton, (150, 250))
        screen.blit(self.sonicButton, (150, 350))
        screen.blit(self.marioButton, (150, 450))
        screen.blit(self.shopText1, (110, 600))
        screen.blit(self.shopText2, (150, 150))
        # back to start button
        if self.unbuy == True:
            screen.blit(self.fail, (100, 400))
            self.unbuy = False

        # show total coins
        self.bank()
        pygame.display.update()
        pygame.display.flip()

# write locked next to buying item until unlocked
    def shopButtons(self, func):
        global coins
        if func.type == pygame.KEYDOWN:
            if func.unicode == "1" and int(self.readCoins()) >= 100:
                self.buy = True
                coins -=100
                self.updateShopCoins()
            elif func.unicode == "1" and int(self.readCoins()) < 100:
                self.unbuy = True

            if func.unicode == "2" and int(self.readCoins()) >= 200:
                self.buy = True
                coins -= 200
                self.updateShopCoins()
            elif func.unicode == "2" and int(self.readCoins()) < 200:
                self.unbuy = True

        if self.rectLink.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.name = "Link"
                self.linkRun = pygame.sprite.Group()
                self.runningLink = Running(width/2, height - 100, self.name)
                self.linkRun.add(self.runningLink)

                self.linkSlides = pygame.sprite.GroupSingle()
                self.slidingLink = Slide(width/2, height - 100, self.name)
                self.linkSlides.add(self.linkSlides)

                self.state = "start"
                self.clickSound.play()
        # Locked charactcers
        if self.rectSonic.collidepoint(pygame.mouse.get_pos()) and self.click == False and self.buySonic == True:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.name = "sonic"
                self.linkRun = pygame.sprite.Group()
                self.runningLink = Running(width/2, height - 100, self.name)
                self.linkRun.add(self.runningLink)

                self.linkSlides = pygame.sprite.GroupSingle()
                self.slidingLink = Slide(width/2, height - 100, self.name)
                self.linkSlides.add(self.linkSlides)

                coins = 0

                self.state = "start"
                self.clickSound.play()
        elif self.rectSonic.collidepoint(pygame.mouse.get_pos()) and self.click == False and self.buySonic == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                if self.buy == True:
                    self.buySonic = True
                    self.buy = False
        if self.rectMario.collidepoint(pygame.mouse.get_pos()) and self.click == False and self.buyMario == True:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.name = "mario"
                self.linkRun = pygame.sprite.Group()
                self.runningLink = Running(width/2, height - 100, self.name)
                self.linkRun.add(self.runningLink)

                self.linkSlides = pygame.sprite.GroupSingle()
                self.slidingLink = Slide(width/2, height - 100, self.name)
                self.linkSlides.add(self.linkSlides)

                coins = 0

                self.state = "start"
                self.clickSound.play()
        elif self.rectMario.collidepoint(pygame.mouse.get_pos()) and self.click == False and self.buyMario == False and self.buy == True:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                if self.buy == True:
                    self.buyMario = True
                    self.buy = False

        if pygame.mouse.get_pressed()[0] == False:
            self.click = False

    def gameOverPage(self):
        global coins, score, gameSpeed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.rectRestart.collidepoint(pygame.mouse.get_pos()) and self.click == False:
                if pygame.mouse.get_pressed()[0] == 1:
                    self.click = True
                    self.clickSound.play()
                    coins = 0
                    score = 0
                    gameSpeed = 0
                    self.__init__()
                    
            if pygame.mouse.get_pressed()[0] == False:
                self.click = False

        if self.updateCoin == True:
            self.updateCoins()
            self.updateCoin = False
        
        screen.blit(gameBackground, (0, 0))
        currentScore = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
         f"Score: {score}", True, (0, 0, 0))
        currentCoins = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
         f"Coins Collected: {coins}", True, (0, 0, 0))
        highscore = pygame.font.Font.render(pygame.font.SysFont("Stgotic", 32),
        f"Highscore: {self.updateScoresEasy()}", True, (0, 0, 0))

        screen.blit(highscore, (width/2- 100, 200))
        screen.blit(currentScore, (width/2- 50, height/2))
        screen.blit(currentCoins, (width/2- 100, height/2 + 100))
        screen.blit(highscore, (width/2- 100, 200))
        
        screen.blit(self.restartButton, (width/2 - 100, height - 200))
        pygame.display.update()
        pygame.display.flip()

    def game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.unicode == "a":
                    self.runningLink.moveLeft = True

                if event.unicode == "d":
                    self.runningLink.moveRight = True

                if event.unicode == "w":
                    self.runningLink.jump = True
                    self.collideJump = True
                    self.jumpSound.play()

                if event.unicode == "s":
                    self.slidingLink.slide = True
                    self.collideSlide = True
                    self.slideSound.play()

            if event.type == pygame.KEYUP:
                if event.unicode == "w":
                    self.runningLink.jumpDown = True
                # hold key to continue jumping
                if event.unicode == "w":
                    self.collideJump = False
                if event.unicode == "s":
                    self.collideSlide = False

        # if collide with player
        self.collision()

        # prevent colision b/w easy obs
        if pygame.Rect.colliderect(self.jumpRect, self.trainRect):
            self.jumpX = random.choice(self.jumpXChoices)

        if pygame.Rect.colliderect(self.slideRect, self.trainRect):
            self.slideX = random.choice(self.slideXChoices)

        if pygame.Rect.colliderect(self.slideRect, self.jumpRect):
            self.slideY = -10

        # prevent collision b/w type 2 obs 
        if pygame.Rect.colliderect(self.jump2Rect, self.train2Rect):
            self.jump2Y = random.randint(-1200, -600)

        if pygame.Rect.colliderect(self.slide2Rect, self.train2Rect):
            self.slide2Y = random.randint(-1200, -600)

        if pygame.Rect.colliderect(self.slide2Rect, self.jump2Rect):
            self.jump2Y = random.randint(-1200, -600)

        # prevent collsion b/w slide 2 and obs
        if pygame.Rect.colliderect(self.slide2Rect, self.slideRect):
            self.slide2Y = random.randint(-1200, -600)

        if pygame.Rect.colliderect(self.slide2Rect, self.trainRect):
            self.slide2Y = random.randint(-1200, -600)

        if pygame.Rect.colliderect(self.slide2Rect, self.jumpRect):
            self.jump2Y = random.randint(-1200, -600)

        # prevent collsion b/w jump 2 and obs
        if pygame.Rect.colliderect(self.jump2Rect, self.slideRect):
            self.jump2Y = random.randint(-1200, -600)

        if pygame.Rect.colliderect(self.jump2Rect, self.trainRect):
            self.jump2Y = random.randint(-1200, -600)

        if pygame.Rect.colliderect(self.jump2Rect, self.jumpRect):
            self.jump2Y = random.randint(-1200, -600)

        # prevent collsion b/w train 2 and obs
        if pygame.Rect.colliderect(self.train2Rect, self.slideRect):
            self.train2Y = random.randint(-1200, -600)

        if pygame.Rect.colliderect(self.train2Rect, self.trainRect):
            self.train2Y = random.randint(-1200, -600)

        if pygame.Rect.colliderect(self.train2Rect, self.jumpRect):
            self.jump2Y = random.randint(-1200, -600)

        # collision with boosters
        if self.jetpackRect.colliderect(self.trainRect):
            self.jetpackY = - 6000
            self.jetpackX = random.choice(self.jetpackXChoices)
        
        if self.extraLifeRect.colliderect(self.train2Rect):
            self.extraLifeY = - 3000
            self.extraLifeX = random.choice(self.extraLifeXChoices)

        # coin collsion detection
        if self.coinY < 750 and self.state == "gameStateHard" or self.coinY < 750 and self.state == "gameStateNormal":
            self.coinY += 20 + gameSpeed * 1.5
            self.coinRect = self.coin.get_rect(topleft = (self.coinX, self.coinY))
        elif self.coinY >= 750 and self.state == "gameStateHard" or self.coinY >= 750 and self.state == "gameStateNormal":
            self.coinY = random.randint(-300, 0)
            self.coinX = random.choice(self.coinXChoices)

        if self.coin2Y < 750 and self.state == "gameStateHard" or self.coin2Y < 750 and self.state == "gameStateNormal":
            self.coin2Y += 20 + gameSpeed * 1.5
            self.coin2Rect = self.coin2.get_rect(topleft = (self.coin2X, self.coin2Y))
        elif self.coin2Y >= 750 and self.state == "gameStateHard" or self.coin2Y >= 750 and self.state == "gameStateNormal":
            self.coin2Y = random.randint(-300, 0)
            self.coin2X = random.choice(self.coin2XChoices)

        if self.coin3Y < 750 and self.state == "gameStateHard" or self.coin3Y < 750 and self.state == "gameStateNormal":
            self.coin3Y += 20 + gameSpeed * 1.5
            self.coin3Rect = self.coin3.get_rect(topleft = (self.coin3X, self.coin3Y))
        elif self.coin3Y >= 750 and self.state == "gameStateHard" or self.coin3Y >= 750 and self.state == "gameStateNormal":
            self.coin3Y = random.randint(-300, 0)
            self.coin3X = random.choice(self.coin3XChoices)

        if self.coin4Y < 750 and self.state == "gameStateHard" or self.coin4Y < 750 and self.state == "gameStateNormal":
            self.coin4Y += 20 + gameSpeed * 1.5
            self.coin4Rect = self.coin4.get_rect(topleft = (self.coin4X, self.coin4Y))
        elif self.coin4Y >= 750 and self.state == "gameStateHard" or self.coin4Y >= 750 and self.state == "gameStateNormal":
            self.coin4Y = random.randint(-300, 0)
            self.coin4X = random.choice(self.coin4XChoices)

        # boosters
        if self.jetpackY < 750 and self.state == "gameStateHard":
            self.jetpackY += 20 + gameSpeed * 2
            self.jetpackRect = self.jetpack.get_rect(topleft = (self.jetpackX, self.jetpackY))
        elif self.jetpackY >=750 and self.state == "gameStateHard":
            self.jetpackY = -1000
            self.jetpackX = random.choice(self.jetpackXChoices)

        if self.extraLifeY < 750 and self.state == "gameStateHard":
            self.extraLifeY += 20 + gameSpeed * 2
            self.extraLifeRect = self.extraLife.get_rect(topleft = (self.extraLifeX, self.extraLifeY))
        elif self.extraLifeY >= 750 and self.state == "gameStateHard":
            self.extraLifeY = -1000
            self.extraLifeX = random.choice(self.extraLifeXChoices)

        if self.trainY < 750:
            self.trainY += 20 + gameSpeed
            self.trainRect = self.trainObs.get_rect(topleft = (self.trainX, self.trainY - 10))
        else:
            self.trainY = -600
            self.trainX = random.choice(self.trainXChoices)

        if self.state == "gameStateHard" and self.train2Y < 800:
            self.train2Y += 20 + gameSpeed * 2
            self.train2Rect = self.train2Obs.get_rect(topleft = (self.train2X, self.train2Y - 10))
        elif self.state == "gameStateHard" and self.train2Y >= 800:
            self.train2Y = random.randint(-1200, -600)
            self.train2X = random.choice(self.train2XChoices)

        if self.jumpY < 750:
            self.jumpY += 20 + gameSpeed
            self.jumpRect = self.jumpObs.get_rect(topleft = (self.jumpX, self.jumpY))
        else:
            self.jumpY = -600 
            self.jumpX = random.choice(self.jumpXChoices)

        if self.state == "gameStateHard" and self.jump2Y < 800:
            self.jump2Y += 20 + gameSpeed * 2
            self.jump2Rect = self.jump2Obs.get_rect(topleft = (self.jump2X, self.jump2Y - 10))
        elif self.state == "gameStateHard" and self.jump2Y >= 800:
            self.jump2Y = random.randint(-1200, -600)
            self.jump2X = random.choice(self.jump2XChoices)

        if self.state == "gameStateNormal" and self.jump2Y < 800:
            self.jump2Y += 20 + gameSpeed * 1.5
            self.jump2Rect = self.jump2Obs.get_rect(topleft = (self.jump2X, self.jump2Y - 10))
        elif self.state == "gameStateNormal" and self.jump2Y >= 800:
            self.jump2Y = random.randint(-1200, -600)
            self.jump2X = random.choice(self.jump2XChoices)

        if self.slideY < 750:
            self.slideY += 20 + gameSpeed
            self.slideRect = self.sliding.get_rect(topleft = (self.slideX + 5, self.slideY - 30))
        else:
            self.slideY = -750
            self.slideX = random.choice(self.slideXChoices)

        if self.state == "gameStateHard" and self.slide2Y < 800:
            self.slide2Y += 20 + gameSpeed * 2
            self.slide2Rect = self.slide2Obs.get_rect(topleft = (self.slide2X, self.slide2Y - 10))
        elif self.state == "gameStateHard" and self.slide2Y >= 800:
            self.slide2Y = random.randint(-1200, -600)
            self.slide2X = random.choice(self.slide2XChoices)

        if self.state == "gameStateNormal" and self.slide2Y < 800:
            self.slide2Y += 20 + gameSpeed * 1.5
            self.slide2Rect = self.slide2Obs.get_rect(topleft = (self.slide2X, self.slide2Y - 10))
        elif self.state == "gameStateNormal" and self.slide2Y >= 800:
            self.slide2Y = random.randint(-1200, -600)
            self.slide2X = random.choice(self.slide2XChoices)

        screen.blit(background, (0, 0)) # coordinates x1 y1

        screen.blit(self.trainObs, (self.trainX, self.trainY))
        if self.state == "gameStateHard":
            screen.blit(self.train2Obs, (self.train2X, self.train2Y))
        if self.state == "gameStateHard" or self.state == "gameStateNormal":
            screen.blit(self.jump2Obs, (self.jump2X, self.jump2Y))
        if self.state == "gameStateHard" or self.state == "gameStateNormal":
            screen.blit(self.slide2Obs, (self.slide2X, self.slide2Y))

        screen.blit(self.jumpObs, (self.jumpX, self.jumpY))
        if self.state == "gameStateNormal" or self.state == "gameStateHard":
            screen.blit(self.coin, (self.coinX, self.coinY))
            screen.blit(self.coin, (self.coin2X, self.coin2Y))
            screen.blit(self.coin, (self.coin3X, self.coin3Y))
            screen.blit(self.coin, (self.coin4X, self.coin4Y))

        if self.state == "gameStateHard":
            screen.blit(self.jetpack, (self.jetpackX, self.jetpackY))
            screen.blit(self.extraLife, (self.extraLifeX, self.extraLifeY))

        self.linkSlides.draw(screen)
        self.linkRun.draw(screen)
        self.linkRun.update(140, 70)
        self.slidingLink.update()
        screen.blit(self.slideObs, (self.slideX, self.slideY))

        if self.jets == True:
            pygame.draw.rect(screen, (200, 255, 255), (25, 50, 50, 50))
            # self.jetCounter()
            screen.blit(self.jetButton, (100, 50))
        if self.lives == True:
            pygame.draw.rect(screen, (255, 200, 255), (25, 100, 50, 50))
            self.lifeCount()
            screen.blit(self.extraButton, (100, 100))

        pygame.draw.rect(screen, (255, 255, 255), (width - 175, 40, 150, 75))
        self.scoring()
        if self.state == "gameStateNormal" or self.state == "gameStateHard":
            self.coinTotal()
        pygame.display.update()
        pygame.display.flip() # make running look more smoother

    def stateControl(self):
        if self.state == "start":
            self.startPage()
        if self.state == "gameStateEasy":
            self.game()
        if self.state == "gameStateNormal":
            self.game()
        if self.state == "gameStateHard":
            self.game()
        if self.state == "over":
            self.gameOverPage()
        if self.state == "shop":
            self.shop()

# general setup
width = 500
height = 800
score = 0
gameSpeed = 0
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
backSound = pygame.mixer.Sound("background.mp3")
# backSound.play()
pygame.display.set_caption("Metro Maniacs")
# intro background through image
background = pygame.image.load("purple.png")
# game call
gameState1 = gameState()

# intro variables
introBackground = pygame.Surface((width, height))
introBackground.fill((252, 238, 117))
introText = pygame.image.load("metroManiacs.png")

# outro variables
gameBackground = pygame.Surface((width, height))
gameBackground.fill((255, 255, 102))

# coin variables
coins = 0

# main loop
running = True
while running:
    # print(pygame.mouse.get_pos())
    gameState1.stateControl()
    clock.tick(15)

