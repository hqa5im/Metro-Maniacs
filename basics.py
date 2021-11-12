import pygame
from sys import exit

pygame.init()

# Assets: https://www.deviantart.com/tiozacdasgalaxias/art/Link-Sprite-Sheet-662562870

# Background: https://www.google.com/url?
# sa=i&url=https%3A%2F%2Fwww.crispedge.com
# %2Ffaq%2Fwhat-is-the-color-of-tan-brown&
# psig=AOvVaw3FbpRbdicm8yDhb1zNSfqh&ust=
# 1636791099622000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCLjSq5KwkvQCFQAAAAAdAAAAABAD

# Reference for side movement: 

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

    # controls the movement of the sprite 
    # such as changing of frames 
    # and going left and right
    def update(self, pressed_key):
        self.currentSprite += 1
        if self.currentSprite >= len(self.sprite):
            self.currentSprite = 0
        self.image = self.sprite[self.currentSprite]

        if pressed_key[pygame.K_a]:
            pygame.Rect.move_ip(self.rect, -70, 0)
        if pressed_key[pygame.K_d]:
            pygame.Rect.move_ip(self.rect, 70, 0)
        # if pressed_key[pygame.K_w]:
        #     pygame.Rect.move_ip(self.rect, 0, -50) ## to jump
        #     pygame.Rect.move_ip(self.rect, 0, 0)


width = 500
height = 800

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Metro Maniacs")

# background through image
background = pygame.image.load("brown.png")

# sprite pics
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
        
    screen.blit(background, (0, 0)) # coordinates x1 y1
    linkRun.draw(screen)
    linkRun.update(pygame.key.get_pressed())
    pygame.display.update()
    pygame.display.flip() # make running look more smoother
    clock.tick(15)





