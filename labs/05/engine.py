import sys
from random import Random

import pygame
from pygame.locals import KEYDOWN, KEYUP, K_DOWN, K_LEFT, K_RIGHT, K_UP
from utils import load_image, Cooldown

EVENT_SPAWN_ENEMY = pygame.USEREVENT

"""
Implement the following functionality into the game (5 points):

Enemies
Each enemy has an initial amount of health and some amount of score that it is worth. 
Periodically spawn an enemy above the window (@Engine.spawn_enemy).
The starting X position of the enemy should be random (and within the window width).
The enemy will move down in every frame according to its speed and delta.
When the enemy moves out of the window, kill the enemy, decrease player health and increase
player's score according to the score of the enemy.
When the enemy hits the player, kill the enemy and decrease player health.
Bonus:
 - use a randomly selected image for each spawned enemy (images/enemyX.gif)
 - assign different starting health and score to the enemy according to its image
 - draw a HP bar above the enemy

Player
Store health for the player and draw it in every frame below the score.
When the player presses space, create a missile at the location of the player (@Player.handle_keys).
When player health reaches zero, end the program.

Missiles
Each missile has some amount of damage that it inflicts to enemies.
The missile will move up in every frame.
When the missile hits an enemy, decrease the enemy's health according to the missile's damage.
If this kills the enemy, remove the enemy and add its score to the player.
Remove the missile after it hits an enemy or leaves the window.
Bonus:
    - add cooldown to the missile firing (e.g. you can only fire once every 100 ms)
    - play a sound when an enemy explodes
    - add an explosion animation to the game for a few seconds when an enemy explodes

Use the delta time in update method for all movements and animations.

Documentation: https://www.pygame.org/docs/index.html
"""


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        """
        :type image: pygame.SurfaceType
        :param pos: Center of the image
        :type pos: Tuple[int, int]

        Example:
            g = GameObject(utils.load_image("images/bullet.gif"), (0, 0))
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self, engine, delta):
        pass

    def draw(self, surface):
        """
        Draws the image of the object onto the given surface.
        """
        surface.blit(self.image, self.rect)

    def move(self, x, y):
        """
        Moves the object by a given amount in x and y axes.
        """
        self.rect = self.rect.move(x, y)


"""
TODO: create new game objects for enemies and missiles

For missiles you can use images/bullet.gif as an image, for enemies you can select from
images/enemy1.gif, enemy2.gif, ...
"""


class Player(GameObject):
    def __init__(self, engine, pos):
        super().__init__(load_image('images/plane.gif'), pos)

        self.image_straight = self.image
        self.image_left = load_image('images/plane_turning_right_1.gif')
        self.image_right = load_image('images/plane_turning_left_1.gif')

        self.engine = engine
        self.speed = [0, 0]  # [x, y]
        self.score = 0
        self.font = pygame.font.Font(None, 36)

        self.key = {
            K_RIGHT: False,
            K_LEFT: False,
            K_UP: False,
            K_DOWN: False,
        }

        """
        TODO: store a list of missiles
        """

    def handle_keys(self, event):
        if event.type not in (KEYDOWN, KEYUP):
            return

        speed_value = 500

        if event.key in self.key:
            self.key[event.key] = event.type == KEYDOWN
        image = self.image
        speed = [0, 0]
        if self.key[K_RIGHT]:
            speed[0] = speed_value
            image = self.image_right
        if self.key[K_LEFT]:
            speed[0] = -speed_value
            image = self.image_left
        if self.key[K_UP]:
            speed[1] = -speed_value
        if self.key[K_DOWN]:
            speed[1] = speed_value
        if not self.key[K_RIGHT] and not self.key[K_LEFT]:
            image = self.image_straight

        self.speed = speed
        self.image = image

    def update(self, engine, delta):
        x, y = self.speed
        self.move(x * delta, y * delta)

        width, height = engine.screen.get_width(), engine.screen.get_height()

        if self.rect.left < 0:
            self.move(abs(self.rect.left), 0)
        if self.rect.right >= width:
            self.move(width - self.rect.right, 0)
        if self.rect.top < 0:
            self.move(0, -self.rect.top)
        if self.rect.bottom >= height:
            self.move(0, height - self.rect.bottom)

        """
        TODO: update all missiles, fire missile if the user is firing
        """

    def draw(self, surface):
        super().draw(surface)
        self.draw_status(surface)

        """
        TODO: draw all missiles
        """

    def draw_status(self, screen):
        if pygame.font:
            # draw score
            text = self.font.render('Score: {}'.format(self.score), 1,
                                    (255, 0, 0))
            textpos = text.get_rect(centerx=screen.get_width() / 2)
            screen.blit(text, textpos)

            """
            TODO: draw health of the player
            """


class Engine:
    def __init__(self, width=640, height=480):
        pygame.init()

        pygame.display.set_caption('SPJA invaders')
        pygame.key.set_repeat(100, 30)

        # create a custom event that will occur every 3 seconds
        pygame.time.set_timer(EVENT_SPAWN_ENEMY, 3000)

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.player = Player(self, (self.width / 2, self.height - 20))
        self.enemies = pygame.sprite.Group()
        self.random = Random()

        self.spawn_enemy()

    def main_loop(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))

        while True:
            self.handle_keys()
            self.update()
            self.draw()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == EVENT_SPAWN_ENEMY:
                self.spawn_enemy()
            else:
                self.player.handle_keys(event)

    def update(self):
        delta = self.clock.tick(60) / 1000
        self.player.update(self, delta)

        for enemy in self.enemies:
            enemy.update(self, delta)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

        # finish drawing the frame
        pygame.display.flip()

    def spawn_enemy(self):
        pass

    def end(self):
        print("GAME OVER")
        exit(0)


if __name__ == '__main__':
    engine = Engine()
    engine.main_loop()
