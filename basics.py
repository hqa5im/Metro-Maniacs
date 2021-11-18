from os import name
import pygame
import random
from sys import exit

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
# high score method: 

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
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        self.i = 0

        self.sliding = pygame.image.load("linkSlide.png")
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
        # player variables !!!!
        self.name = "Link"
        self.linkRun = pygame.sprite.Group()
        self.runningLink = Running(width/2, height - 100, self.name)
        self.linkRun.add(self.runningLink) # add the sprites at this position

        self.state = "start"
        # train variables
        self.trainXChoices = [30, 185, 320]
        self.trainX = random.choice(self.trainXChoices)
        self.trainY = -600
        self.trainObs = pygame.image.load("obstacles/train.png")
        self.trainRect = self.trainObs.get_rect(topleft = (self.trainX, self.trainY))

        # jump obstacles variables
        # make a jumpY in a list with the second obstacle 
        # just a few pixels behind it
        self.jumpXChoices = [60, 195, 350]
        self.jumpX = random.choice(self.jumpXChoices)
        self.jumpY = -600
        self.jumpObs = pygame.image.load("obstacles/jumpObs.png")
        self.jumpRect = self.jumpObs.get_rect(topleft = (self.jumpX, self.jumpY))
        self.collideJump = False

        # slide obstacel variables
        self.slideXChoices = [43, 180, 330]
        self.slideX = random.choice(self.slideXChoices)
        self.slideY = -400
        self.slideObs = pygame.image.load("obstacles/slideObs.png")
        self.slideRect = self.slideObs.get_rect(topleft = (self.slideX, self.slideY))
        self.collideSlide = False

        # button variables
        self.easyButton = pygame.image.load("buttons/easy.png")
        self.normalButton = pygame.image.load("buttons/normal.png")
        self.hardButton = pygame.image.load("buttons/hard.png")
        self.shopButton = pygame.image.load("buttons/shop.png")

        self.rectEasy = self.easyButton.get_rect(topleft = (170, 469))
        self.rectNormal = self.normalButton.get_rect(topleft = ((170, 564)))
        self.rectHard = self.hardButton.get_rect(topleft = ((170, 664)))
        self.rectShop = self.shopButton.get_rect(topleft = ((170, 764)))
        self.click = False
        self.clickSound = pygame.mixer.Sound("click.mp3")

        # shop buttons
        self.linkButton = pygame.image.load("buttons/Link.png")
        self.sonicButton = pygame.image.load("buttons/Sonic.png")

        self.rectLink = self.linkButton.get_rect(topleft = (153, 452))
        self.rectSonic = self.sonicButton.get_rect(topleft = (153, 555))

        # playerRect
        self.x = width/2
        self.y = height - 100
        self.sliding = pygame.image.load("linkSlide.png")
        self.rect = self.sliding.get_rect(midbottom = (self.x, self.y))

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


    def scoring(self):
        global score, gameSpeed
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

    def collision(self):
        global coins
        # running sprite
        if self.trainRect.colliderect(rectRun):
            self.state = "over"

        # sliding sprite
        if self.slideRect.colliderect(rectRun) and self.collideSlide != True:
            self.state = "over"
        
        # jump sprite
        if self.jumpRect.colliderect(rectRun) and self.collideJump != True:
            self.state = "over"

        # coin collision
        if self.coinRect.colliderect(rectRun):
            self.coinY = random.randint(-300, 0)
            self.coinX = random.choice(self.coinXChoices)
            coins += 1

        if self.coin2Rect.colliderect(rectRun):
            self.coin2Y = random.randint(-300, 0)
            self.coin2X = random.choice(self.coin2XChoices)
            coins += 1

        if self.coin3Rect.colliderect(rectRun):
            self.coin3Y = random.randint(-300, 0)
            self.coin3X = random.choice(self.coin3XChoices)
            coins += 1

        if self.coin4Rect.colliderect(rectRun):
            self.coin4Y = random.randint(-300, 0)
            self.coin4X = random.choice(self.coin4XChoices)
            coins += 1

        
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
            self.shopButtons()

        screen.blit(gameBackground, (0, 0))
        screen.blit(self.linkButton, (150, 450))
        screen.blit(self.sonicButton, (150, 550))
        pygame.display.update()
        pygame.display.flip()

    def shopButtons(self):
        if self.rectLink.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.name = "Link"
                self.linkRun = pygame.sprite.Group()
                self.runningLink = Running(width/2, height - 100, self.name)
                self.linkRun.add(self.runningLink) # add the sprites at this position
                print("link selected!")
                self.state = "start"
                self.clickSound.play()
        if self.rectSonic.collidepoint(pygame.mouse.get_pos()) and self.click == False:
            if pygame.mouse.get_pressed()[0] == 1:
                self.click = True
                self.name = "sonic"
                self.linkRun = pygame.sprite.Group()
                self.runningLink = Running(width/2, height - 100, self.name)
                self.linkRun.add(self.runningLink) # add the sprites at this position
                print("sonic selected!")
                self.state = "start"
                self.clickSound.play()
        if pygame.mouse.get_pressed()[0] == False:
            self.click = False


    def gameOverPage(self): ##FOR EASY VERSION
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
        # need to add restart button - takes tom enu page

    def gameEasy(self):
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

                if event.unicode == "s":
                    slidingLink.slide = True
                    self.collideSlide = True

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
            self.coinY = random.randint(-300, 0)
            self.coinX = random.choice(self.coinXChoices)

        if self.coin2Y < 750:
            self.coin2Y += 20 + gameSpeed
            self.coin2Rect = self.coin2.get_rect(topleft = (self.coin2X, self.coin2Y))
        else:
            self.coin2Y = random.randint(-300, 0)
            self.coin2X = random.choice(self.coin2XChoices)

        if self.coin3Y < 750:
            self.coin3Y += 20 + gameSpeed
            self.coin3Rect = self.coin3.get_rect(topleft = (self.coin3X, self.coin3Y))
        else:
            self.coin3Y = random.randint(-300, 0)
            self.coin3X = random.choice(self.coin3XChoices)

        if self.coin4Y < 750:
            self.coin4Y += 20 + gameSpeed
            self.coin4Rect = self.coin4.get_rect(topleft = (self.coin4X, self.coin4Y))
        else:
            self.coin4Y = random.randint(-300, 0)
            self.coin4X = random.choice(self.coin4XChoices)
        
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
            self.slideRect = self.sliding.get_rect(topleft = (self.slideX + 5, self.slideY - 30))
        else:
            # spawn slides in random location
            self.slideY = -750
            self.slideX = random.choice(self.slideXChoices)

        screen.blit(background, (0, 0)) # coordinates x1 y1

        screen.blit(self.trainObs, (self.trainX, self.trainY))
        screen.blit(self.jumpObs, (self.jumpX, self.jumpY))

        screen.blit(self.coin, (self.coinX, self.coinY))
        screen.blit(self.coin, (self.coin2X, self.coin2Y))
        screen.blit(self.coin, (self.coin3X, self.coin3Y))
        screen.blit(self.coin, (self.coin4X, self.coin4Y))

        linkSlides.draw(screen)
        self.linkRun.draw(screen)
        screen.blit(self.slideObs, (self.slideX, self.slideY))
        self.linkRun.update(140, 70)
        slidingLink.update()

        # pygame.draw.rect(screen, (0, 255, 0), self.slideRect)  ##########
        pygame.draw.rect(screen, (255, 255, 255), (width - 175, 40, 150, 50))
        self.scoring()
        pygame.display.update()
        pygame.display.flip() # make running look more smoother

    def stateControl(self):
        if self.state == "start":
            self.startPage()
        if self.state == "gameStateEasy":
            self.gameEasy()
        if self.state == "gameStateNormal": ##make
            self.gameNormal()
        if self.state == "gameStateHard": ##make
            self.gameHard()
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

# coin variables
coins = 0

# sliding sprite pics
linkSlides = pygame.sprite.GroupSingle()
slidingLink = Slide(width/2, height - 100)
linkSlides.add(linkSlides)

# main loop
running = True
while running:
    gameState1.stateControl()
    clock.tick(15)

