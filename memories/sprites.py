import random

import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface

import memories.constants as constants


class CustomSprite(Sprite):
    """Class from which all other sprites in the game inherit"""
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface = value

    def __init__(self, x, y, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.surface = Surface((self.width, self.height)).convert()

    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))


class BackgroundStar(CustomSprite):
    """Class for background stars with parallax scrolling"""
    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value

    def __init__(self, x, y, layer):
        width = 2
        height = 2
        super().__init__(x, y, width, height)
        self.layer = layer  # for parallax scrolling (1, 2, or 3 -- determines how fast star scrolls)
        self.surface.fill((255, 255, 255))

    def scroll(self):
        """Scroll the star towards the bottom of the screen. self.layer determines how fast the star scrolls."""
        if self.layer == 1:
            self.y += 1
        elif self.layer == 2:
            self.y += 2
        elif self.layer == 3:
            self.y += 3

        # move the star to the top of the screen if it has reached the bottom and choose a new x position
        if self.y > constants.SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randrange(0, constants.SCREEN_WIDTH)


class StatusBarUnit(CustomSprite):
    """One rectangular unit of the status bar"""
    def __init__(self, x, y, color):
        width = 4
        height = 8
        super().__init__(x, y, width, height)
        self.surface.fill(color)


class ImageSprite(CustomSprite):
    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def image_width(self):
        return self.image.get_width()

    @property
    def image_height(self):
        return self.image.get_height()

    @property
    def rect(self):
        rectangle = self._image.get_rect()
        rectangle.x = self.x
        rectangle.y = self.y
        return rectangle

    def __init__(self, x, y, image_filename):
        self._image = pygame.image.load(image_filename).convert_alpha()
        self._image = pygame.transform.scale(self.image, (self.image_width * 2, self.image_height * 2))
        super().__init__(x, y, self.image_width, self.image_height)
        self.mask = pygame.mask.from_surface(self._image)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class PlayerShip(CustomSprite):
    """Class for the ship"""
    @property
    def rect(self):
        rectangle = self._image_0.get_rect()
        rectangle.x = self.x
        rectangle.y = self.y
        return rectangle

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

    def __init__(self):
        self._image_0 = pygame.image.load('assets/ship0.png').convert_alpha()
        self._image_1 = pygame.image.load('assets/ship1.png').convert_alpha()
        self._image_size = self._image_0.get_size()
        self._image_0 = pygame.transform.scale(self._image_0,
                                               (int(self._image_size[0] * 2), (int(self._image_size[1] * 2))))
        self._image_1 = pygame.transform.scale(self._image_1,
                                               (int(self._image_size[0] * 2), (int(self._image_size[1] * 2))))
        width = self._image_0.get_width()
        height = self._image_0.get_height()
        x = ((constants.SCREEN_WIDTH / 2) - width / 2)
        y = constants.SCREEN_HEIGHT - 100
        super().__init__(x, y, width, height)
        self._frame = 0
        self._frame_counter = 0
        self._visible = True

    def draw(self, surface):
        self._frame_counter += 1
        if self._frame_counter == 100:
            self._frame_counter = 0
            if self._frame == 0:
                self._frame = 1
            else:
                self._frame = 0
        if self._frame == 0:
            image = self._image_0
        else:
            image = self._image_1
        surface.blit(image, (self.x, self.y))

    def move_left(self):
        self.x -= 1
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += 1
        if self.x > constants.SCREEN_WIDTH - self.width:
            self.x = constants.SCREEN_WIDTH - self.width

    def move_up(self):
        self.y -= 1
        if self.y < constants.SCREEN_HEIGHT / 2:
            self.y = constants.SCREEN_HEIGHT / 2

    def move_down(self):
        self.y += 1
        if self.y > constants.SCREEN_HEIGHT - 100:
            self.y = constants.SCREEN_HEIGHT - 100


class Fire(ImageSprite):
    def __init__(self, x, y):
        super().__init__(x, y, 'assets/fire.png')

    def move(self):
        self.y -= 1


class EnemyFire(ImageSprite):
    def __init__(self, x, y):
        super().__init__(x, y, 'assets/fire.png')
        self.image = pygame.transform.rotate(self.image, 180)

    def move(self):
        self.y += 1


class Enemy(ImageSprite):
    def __init__(self, x, y, image_filename):
        self.fire_cooldown_timer = random.randrange(300, constants.ENEMY_FIRE_MAX_COOLDOWN_TIME)
        super().__init__(x, y, image_filename)


class Enemy0(Enemy):
    def __init__(self):
        super().__init__(0, 0, 'assets/enemy_0.png')
        self.x = random.randrange(0, constants.SCREEN_WIDTH - self.image_width)
        self.y = 0 - self.image_height
        self._movement_cooldown_timer = 3

    def move(self):
        self._movement_cooldown_timer -= 1
        if self._movement_cooldown_timer == 0:
            self.y += 1
            self._movement_cooldown_timer = 3


class Enemy1(Enemy):
    def __init__(self):
        super().__init__(0, 0, 'assets/enemy_1.png')
        self.x = random.randrange(0, constants.SCREEN_WIDTH - self.image_width)
        self.y = 0 - self.image_height
        self._movement_cooldown_timer = 5
        self._x_movement_direction = 0

    def move(self):
        self._movement_cooldown_timer -= 1
        if self._movement_cooldown_timer == 0:
            self.y += 1
            if self._x_movement_direction == 0:
                self.x += 1
                if self.x == constants.SCREEN_WIDTH - self.image_width:
                    self._x_movement_direction = 1
            else:
                self.x -= 1
                if self.x == 0:
                    self._x_movement_direction = 0
            self._movement_cooldown_timer = 5


class Enemy2(Enemy):
    def __init__(self):
        super().__init__(0, 0, 'assets/enemy_2.png')
        self.x = random.randrange(0, constants.SCREEN_WIDTH - self.image_width)
        self.y = 0 - self.image_height
        self._movement_cooldown_timer = 4

    def move(self):
        self._movement_cooldown_timer -= 1
        if self._movement_cooldown_timer == 0:
            self.y += 1
            self.x += random.randrange(-3, 4)
            self._movement_cooldown_timer = 4
        if self.x < 0:
            self.x = 0
        if self.x > constants.SCREEN_WIDTH - self.image_width:
            self.x = constants.SCREEN_WIDTH - self.image_width


class Enemy3(Enemy):
    def __init__(self):
        super().__init__(0, 0, 'assets/enemy_3.png')
        self.x = random.randrange(0, constants.SCREEN_WIDTH - self.image_width)
        self.y = 0 - self.image_height
        self._movement_cooldown_timer = 6

    def move(self):
        self._movement_cooldown_timer -= 1
        if self._movement_cooldown_timer == 0:
            self.y += 1
            self._movement_cooldown_timer = 4
        if self.x < 0:
            self.x = 0
        if self.x > constants.SCREEN_WIDTH - self.image_width:
            self.x = constants.SCREEN_WIDTH - self.image_width


class BossShip(ImageSprite):
    def __init__(self, x, y, image_filename):
        super().__init__(x, y, image_filename)
        self.x = (constants.SCREEN_WIDTH / 2) - (self.image_width / 2)
        self.y = -5 - self.image_height
        self.movement_direction = 0

    def move(self):
        if self.y < 35:
            self.y += 1
        else:
            if self.movement_direction == 0:
                self.x -= 1
                if self.x == 10:
                    self.movement_direction = 1
            else:
                self.x += 1
                if self.x == constants.SCREEN_WIDTH - self.image_width - 10:
                    self.movement_direction = 0


class BossShip0(BossShip):
    def __init__(self):
        super().__init__(0, 0, 'assets/boss_ship_0.png')
        self.health = constants.BOSS_0_HEALTH


class BossShip1(BossShip):
    def __init__(self):
        super().__init__(0, 0, 'assets/boss_ship_1.png')
        self.health = constants.BOSS_1_HEALTH


class Explosion(CustomSprite):
    @property
    def rect(self):
        rectangle = self._image_1.get_rect()
        rectangle.x = self.x
        rectangle.y = self.y
        return rectangle

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, value):
        self._images = value

    @property
    def current_image(self):
        return self._current_image

    @current_image.setter
    def current_image(self, value):
        self._current_image = value

    def __init__(self, x, y):
        self._image_1 = pygame.image.load('assets/explosion/1.png').convert_alpha()
        self._image_2 = pygame.image.load('assets/explosion/2.png').convert_alpha()
        self._image_3 = pygame.image.load('assets/explosion/3.png').convert_alpha()
        self._image_4 = pygame.image.load('assets/explosion/4.png').convert_alpha()
        self._image_5 = pygame.image.load('assets/explosion/5.png').convert_alpha()
        self._image_6 = pygame.image.load('assets/explosion/6.png').convert_alpha()
        self._image_7 = pygame.image.load('assets/explosion/7.png').convert_alpha()
        self._image_8 = pygame.image.load('assets/explosion/8.png').convert_alpha()
        self._image_9 = pygame.image.load('assets/explosion/9.png').convert_alpha()
        self._image_10 = pygame.image.load('assets/explosion/10.png').convert_alpha()
        self._image_11 = pygame.image.load('assets/explosion/11.png').convert_alpha()
        self._image_12 = pygame.image.load('assets/explosion/12.png').convert_alpha()
        self._image_13 = pygame.image.load('assets/explosion/13.png').convert_alpha()
        self._image_14 = pygame.image.load('assets/explosion/14.png').convert_alpha()
        self._image_15 = pygame.image.load('assets/explosion/15.png').convert_alpha()
        self._image_16 = pygame.image.load('assets/explosion/16.png').convert_alpha()
        center_x = x - (self._image_1.get_width() / 2)
        center_y = y - (self._image_1.get_height() / 2)
        super().__init__(center_x, center_y, self._image_1.get_width(), self._image_1.get_height())
        self._images = [self._image_1, self._image_2, self._image_3, self._image_4, self._image_5, self._image_6,
                        self._image_7, self._image_8, self._image_9, self._image_10, self._image_11, self._image_12,
                        self._image_13, self._image_14, self._image_15, self._image_16]
        self._current_image = 0

    def draw(self, surface):
        surface.blit(self.images[self.current_image], (self.x, self.y))


class HugeExplosion(Explosion):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.new_images = []
        for image in self.images:
            transformed_image = pygame.transform.scale(image, (int(image.get_width() * 10), (int(image.get_height() * 10))))
            self.new_images.append(transformed_image)
        self.images = self.new_images