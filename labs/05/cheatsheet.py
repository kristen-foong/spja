import sys

import pygame
from utils import Cooldown, load_image

# (pseudo-)random numbers
import random

r = random.Random()
r.random()  # random number between in range (0, 1)
r.randint(3, 5)  # random number in range [3, 5]
r.choice([1, 2, 3])  # randomly select item from collection

# X coordinate is increasing from left to right
# Y coordinate is increasing from top to bottom

# sprite groups
# https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group
g = pygame.sprite.Group()  # group of sprites
e = Enemy(...)  # create sprite
g.add(e)  # add sprite to group
g.update(arg1, arg2, ...)  # call .update(arg1, arg2, ...) on all sprites in group
e.kill()  # automatically remove sprite from all groups

# rectangles
# https://www.pygame.org/docs/ref/rect.html
r = pygame.Rect(xleft, ytop, width, height)
r = pygame.Rect((xleft, ytop), (width, height))
r.topleft  # coordinates of topleft point
r.topleft = (5, 0)  # move rectangle so that topleft point is at (5, 0)
# topleft, center, bottomleft, ...

# images and drawing
img = load_image('images/...')  # load image
rect = img.get_rect()  # get image rectangle
rect.center = (50, 50)  # set image center to (50, 50)

# surface is a Surface object
surface.blit(img, rect)  # draw `img` at position specified by rectangle `rect`
pygame.draw.rect(surface, color, rect)  # draw a rectangle
for sprite in g:  # draw all sprites from group
    g.draw(surface)

# colors
# https://www.pygame.org/docs/ref/color.html
c = pygame.Color(255, 0, 0)  # Create a color (R, G, B), each in interval [0, 255]

engine.screen  # window screen
engine.screen.get_width()  # window width
engine.screen.get_height()  # window height

# delta
clock = pygame.time.Clock()  # create a delta clock
delta = clock.tick(60) / 1000  # calculate delta in each update frame
rect = rect.move(500 * delta, 0)  # move rectangle in X axis by 500 * delta

# cooldown
cd = Cooldown(500)  # 500 ms cooldown
cd.update(delta)  # update cooldown in every frame
if cd.reset_if_ready():  # returns True if CD is ready and resets it if its ready
    pass

# react to some key event
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()
    else:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pass

# collisions
# return all sprites from collection `items` that collide with `player`
collisions = pygame.sprite.spritecollide(player, items, False)
if collisions:
    for item in collisions:  # remove all items that collided with `player`
        item.kill()
