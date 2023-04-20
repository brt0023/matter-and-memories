import random
import sys

import pygame
from pygame.sprite import Group

import memories.constants as constants
from memories.sprites import BackgroundStar, StatusBarUnit, PlayerShip, Fire, EnemyFire, \
    Enemy0, Enemy1, Enemy2, Enemy3, BossShip0, BossShip1, Explosion, HugeExplosion


class Game:
    """The game itself"""
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.display.set_caption('Matter and Memories')
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

        self.stage_number = 1

        self.stars = []
        for _ in range(150):
            layer = random.randrange(1, 4)
            x = random.randrange(0, constants.SCREEN_WIDTH)
            y = random.randrange(0, constants.SCREEN_HEIGHT)
            star = BackgroundStar(x, y, layer)
            self.stars.append(star)
        self._star_update_counter = 0

        self.ship = PlayerShip()
        self.fires = []
        self.fire_cooldown_timer = 0
        self.fire_left = True

        self.enemy_fires = []
        self.enemy_fire_cooldown_timer = constants.ENEMY_FIRE_MAX_COOLDOWN_TIME

        self.enemies = []
        self.enemy_appearance_timer = constants.STAGE_INTRO_TIMER * 2
        self.stage_intro_timer = constants.STAGE_INTRO_TIMER
        self.title_timer = constants.STAGE_INTRO_TIMER

        self.explosions = []
        self.explosion_cooldown_timer = 0

        self.ammo_counter = constants.MAX_AMMO
        self.ammo_recharge_timer = constants.AMMO_RECHARGE_TIME

        self.lives_counter = constants.LIVES
        self.life_cooldown_timer = constants.LIFE_COOLDOWN_TIMER

        self.health_counter = constants.MAX_HEALTH

        self.score_counter = 0

        self.boss_ship = None
        self.boss_ship_0_defeated = False
        self.boss_ship_1_defeated = False
        self.boss_ship_present = False
        self.boss_ship_group = Group()

        self.boss_ship_movement_timer = constants.BOSS_SHIP_MOVEMENT_TIMER

        pygame.font.init()
        self.small_font = pygame.font.Font('assets/helvetica-bold.ttf', 12)
        self.ammo_counter_label = self.small_font.render('AMMO', True, (255, 255, 255))
        self.ammo_counter_label_rect = self.ammo_counter_label.get_rect()
        self.ammo_counter_label_rect.x = constants.AMMO_BAR_X
        self.ammo_counter_label_rect.y = constants.STATUS_BAR_LABEL_Y

        self.lives_counter_label = self.small_font.render('LIVES', True, (255, 255, 255))
        self.lives_counter_label_rect = self.lives_counter_label.get_rect()
        self.lives_counter_label_rect.x = constants.LIVES_BAR_X
        self.lives_counter_label_rect.y = constants.STATUS_BAR_LABEL_Y

        self.health_bar_label = self.small_font.render('HEALTH', True, (255, 255, 255))
        self.health_bar_label_rect = self.health_bar_label.get_rect()
        self.health_bar_label_rect.x = constants.HEALTH_BAR_X
        self.health_bar_label_rect.y = constants.STATUS_BAR_LABEL_Y

        self.score_counter_label = self.small_font.render('SCORE', True, (255, 255, 255))
        self.score_counter_label_rect = self.score_counter_label.get_rect()
        self.score_counter_label_rect.x = constants.SCORE_BAR_X
        self.score_counter_label_rect.y = constants.STATUS_BAR_LABEL_Y

        self.boss_health_label = self.small_font.render('BOSS', True, (255, 255, 255))
        self.boss_health_label_rect = self.boss_health_label.get_rect()
        self.boss_health_label_rect.x = constants.AMMO_BAR_X
        self.boss_health_label_rect.y = constants.BOSS_HEALTH_BAR_LABEL_Y

        self.medium_font = pygame.font.Font('assets/helvetica-bold.ttf', 24)
        self.instructions_1_label = self.medium_font.render('MOVE: WASD or arrow keys', True, (255, 255, 255))
        self.instructions_2_label = self.medium_font.render('FIRE: space bar', True, (255, 255, 255))

        self.instructions_1_label_rect = self.instructions_1_label.get_rect()
        self.instructions_1_label_rect.x = (constants.SCREEN_WIDTH / 2) - (self.instructions_1_label_rect.width / 2)
        self.instructions_1_label_rect.y = constants.SCREEN_HEIGHT * 0.66

        self.instructions_2_label_rect = self.instructions_2_label.get_rect()
        self.instructions_2_label_rect.x = (constants.SCREEN_WIDTH / 2) - (self.instructions_2_label_rect.width / 2)
        self.instructions_2_label_rect.y = self.instructions_1_label_rect.y + self.instructions_2_label_rect.height

        self.large_font = pygame.font.Font('assets/helvetica-bold.ttf', 36)
        self.stage_1_label = self.large_font.render('STAGE 1', True, (255, 255, 255))
        self.stage_1_label_rect = self.stage_1_label.get_rect()
        self.stage_1_label_rect.x = (constants.SCREEN_WIDTH / 2) - (self.stage_1_label_rect.width / 2)
        self.stage_1_label_rect.y = (constants.SCREEN_HEIGHT / 2) - (self.stage_1_label_rect.height / 2)

        self.stage_2_label = self.large_font.render('STAGE 2', True, (255, 255, 255))
        self.stage_2_label_rect = self.stage_2_label.get_rect()
        self.stage_2_label_rect.x = (constants.SCREEN_WIDTH / 2) - (self.stage_2_label_rect.width / 2)
        self.stage_2_label_rect.y = (constants.SCREEN_HEIGHT / 2) - (self.stage_2_label_rect.height / 2)

        self.game_over_label = self.large_font.render('GAME OVER', True, (255, 255, 255))
        self.game_over_label_rect = self.game_over_label.get_rect()
        self.game_over_label_rect.x = (constants.SCREEN_WIDTH / 2) - (self.game_over_label_rect.width / 2)
        self.game_over_label_rect.y = (constants.SCREEN_HEIGHT / 2) - (self.game_over_label_rect.height / 2)

        self.you_won_label = self.large_font.render('YOU WON', True, (255, 255, 255))
        self.you_won_label_rect = self.you_won_label.get_rect()
        self.you_won_label_rect.x = (constants.SCREEN_WIDTH / 2) - (self.you_won_label_rect.width / 2)
        self.you_won_label_rect.y = (constants.SCREEN_HEIGHT / 2) - (self.you_won_label_rect.height / 2)

        self.huge_font = pygame.font.Font('assets/helvetica-bold.ttf', 48)
        self.game_title_label_1 = self.huge_font.render('MATTER', True, (255, 255, 255))
        self.game_title_label_2 = self.huge_font.render('AND', True, (255, 255, 255))
        self.game_title_label_3 = self.huge_font.render('MEMORIES', True, (255, 255, 255))

        # Center the three line label on screen starting with the middle one
        self.game_title_label_2_rect = self.game_title_label_2.get_rect()
        self.game_title_label_2_rect.x = (constants.SCREEN_WIDTH / 2) - (self.game_title_label_2_rect.width / 2)
        self.game_title_label_2_rect.y = (constants.SCREEN_HEIGHT / 2) - (self.game_title_label_2_rect.height / 2)

        self.game_title_label_3_rect = self.game_title_label_3.get_rect()
        self.game_title_label_3_rect.x = (constants.SCREEN_WIDTH / 2) - (self.game_title_label_3_rect.width / 2)
        self.game_title_label_3_rect.y = self.game_title_label_2_rect.y + self.game_title_label_3_rect.height

        self.game_title_label_1_rect = self.game_title_label_1.get_rect()
        self.game_title_label_1_rect.x = (constants.SCREEN_WIDTH / 2) - (self.game_title_label_1_rect.width / 2)
        self.game_title_label_1_rect.y = self.game_title_label_2_rect.y - self.game_title_label_1_rect.height

        # music
        pygame.mixer.music.load('assets/music.ogg')
        pygame.mixer.music.play(-1)

        # sound effects
        self.fire_sound = pygame.mixer.Sound('assets/fire.wav')
        self.enemy_fire_sound = pygame.mixer.Sound('assets/enemy_fire.wav')
        self.explosion_sound = pygame.mixer.Sound('assets/explosion.wav')
        self.boss_explosion_sound = pygame.mixer.Sound('assets/boss_explosion.wav')

    def game_loop(self):
        """Main game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # move ship when pressing arrows or WASD
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                self.ship.move_left()
            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                self.ship.move_right()
            if pressed[pygame.K_UP] or pressed[pygame.K_w]:
                self.ship.move_up()
            if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                self.ship.move_down()
            if pressed[pygame.K_SPACE] and self.ship.visible and self.fire_cooldown_timer == 0 and self.ammo_counter > 0:
                if self.fire_left:
                    fire = Fire(self.ship.x + 5, self.ship.y)
                    self.fire_left = False
                else:
                    fire = Fire(self.ship.x + 40, self.ship.y)
                    self.fire_left = True
                self.fires.append(fire)
                self.fire_cooldown_timer = constants.FIRE_COOLDOWN_TIMER
                self.ammo_counter -= 1
                self.ammo_recharge_timer = constants.AMMO_RECHARGE_TIME
                self.fire_sound.play()

            self.fire_cooldown_timer -= 1
            if self.fire_cooldown_timer == -1:
                self.fire_cooldown_timer = 0

            if self.ship.visible:
                self.ammo_recharge_timer -= 1
                if self.ammo_recharge_timer <= 0:
                    if self.ammo_counter < constants.MAX_AMMO:
                        self.ammo_counter += 1
                        self.ammo_recharge_timer = constants.AMMO_RECHARGE_TIME

            self.enemy_appearance_timer -= 1
            if self.enemy_appearance_timer <= 0 and self.ship.visible and self.boss_ship_present is False:
                if self.boss_ship_0_defeated is True and self.boss_ship_1_defeated is True:
                    pass
                else:
                    enemy_type = random.randrange(0, 4)
                    enemy = None
                    if enemy_type == 0:
                        enemy = Enemy0()
                    if enemy_type == 1:
                        enemy = Enemy1()
                    if enemy_type == 2:
                        enemy = Enemy2()
                    if enemy_type == 3:
                        enemy = Enemy3()
                    if enemy is not None:
                        self.enemies.append(enemy)
                    self.enemy_appearance_timer = random.randrange(constants.ENEMY_APPEARANCE_TIMER_MIN,
                                                                   constants.ENEMY_APPEARANCE_TIMER_MAX)

            # draw black background
            self.screen.fill((0, 0, 0))

            # draw stars
            for star in self.stars:
                star.draw(self.screen)
                # scroll the stars if the update counter is 10
                if self._star_update_counter == 8:
                    star.scroll()

            # update self._star_update_counter
            self._star_update_counter += 1
            if self._star_update_counter == 11:
                self._star_update_counter = 0

            # draw fires
            for fire in self.fires:
                fire.draw(self.screen)
                fire.move()
                if fire.y < -25:
                    self.fires.remove(fire)

            for fire in self.enemy_fires:
                fire.draw(self.screen)
                fire.move()
                if fire.y > constants.SCREEN_HEIGHT:
                    self.enemy_fires.remove(fire)

            # draw player ship
            if self.ship.visible:
                self.ship.draw(self.screen)

            # draw enemies
            for enemy in self.enemies:
                enemy.draw(self.screen)
                enemy.move()
                if enemy.y > constants.SCREEN_HEIGHT:
                    self.enemies.remove(enemy)

            # draw enemy fire
            for enemy in self.enemies:
                enemy.fire_cooldown_timer -= 1
                if enemy.fire_cooldown_timer == 0:
                    self.enemy_fires.append(EnemyFire(enemy.x + (enemy.width / 2), enemy.y + enemy.height))
                    enemy.fire_cooldown_timer = random.randrange(300, constants.ENEMY_FIRE_MAX_COOLDOWN_TIME)
                    self.enemy_fire_sound.play()

            # detect collision between fires and enemies
            for fire in self.fires:
                if self.enemies:
                    for enemy in self.enemies:
                        if fire.rect.colliderect(enemy.rect):
                            enemy_center_x = enemy.rect.center[0]
                            enemy_center_y = enemy.rect.center[1]
                            explosion = Explosion(enemy_center_x, enemy_center_y)
                            self.enemies.remove(enemy)
                            self.fires.remove(fire)
                            self.explosions.append(explosion)
                            self.explosion_sound.play()
                            self.score_counter += 1
                # detect collision between fires and boss ship
                if self.boss_ship_present:
                    if fire.rect.colliderect(self.boss_ship.rect):
                        if pygame.sprite.spritecollide(fire, self.boss_ship_group, False, pygame.sprite.collide_mask):
                            self.fires.remove(fire)
                            explosion = Explosion(fire.x, fire.y)
                            self.explosions.append(explosion)
                            self.explosion_sound.play()
                            self.boss_ship.health -= 1

            # detect collision between enemy fire and ship
            for fire in self.enemy_fires:
                if self.ship.visible and fire.rect.colliderect(self.ship.rect):
                    explosion = Explosion(fire.x + (fire.width / 2), fire.y + fire.height)
                    self.explosions.append(explosion)
                    self.explosion_sound.play()
                    self.enemy_fires.remove(fire)
                    self.health_counter -= 1
                    if self.health_counter == 0:
                        self.ship.visible = False
                        self.lives_counter -= 1
                        self.life_cooldown_timer = constants.LIFE_COOLDOWN_TIMER

            # detect collision between ship and enemies
            if self.ship.visible:
                for enemy in self.enemies:
                    if enemy.rect.colliderect(self.ship.rect):
                        ship_center_x = self.ship.rect.center[0]
                        ship_center_y = self.ship.rect.center[1]
                        explosion = Explosion(ship_center_x, ship_center_y)
                        self.explosions.append(explosion)
                        self.explosion_sound.play()
                        self.enemies.remove(enemy)
                        self.health_counter -= 1
                        if self.health_counter == 0:
                            self.ship.visible = False
                            self.lives_counter -= 1
                            self.life_cooldown_timer = constants.LIFE_COOLDOWN_TIMER

            if self.ship.visible is False:
                self.life_cooldown_timer -= 1
                if self.life_cooldown_timer == 0 and self.lives_counter > 0:
                    self.ship = PlayerShip()
                    self.life_cooldown_timer = constants.LIFE_COOLDOWN_TIMER
                    self.enemy_appearance_timer = constants.ENEMY_APPEARANCE_TIMER_MAX
                    self.ammo_counter = constants.MAX_AMMO
                    self.health_counter = constants.MAX_HEALTH

            # draw ammo bar
            self.screen.blit(self.ammo_counter_label, self.ammo_counter_label_rect)
            for i in range(self.ammo_counter):
                ammo_bar_unit = StatusBarUnit(constants.AMMO_BAR_X + (6 * i),
                                              constants.STATUS_BAR_Y, constants.AMMO_BAR_COLOR)
                ammo_bar_unit.draw(self.screen)

            # draw lives bar
            self.screen.blit(self.lives_counter_label, self.lives_counter_label_rect)
            for i in range(self.lives_counter):
                lives_bar_unit = StatusBarUnit(constants.LIVES_BAR_X + (6 * i), constants.STATUS_BAR_Y,
                                               constants.LIVES_BAR_COLOR)
                lives_bar_unit.draw(self.screen)

            # draw health bar
            self.screen.blit(self.health_bar_label, self.health_bar_label_rect)
            for i in range(self.health_counter):
                health_bar_unit = StatusBarUnit(constants.HEALTH_BAR_X + (6 * i), constants.STATUS_BAR_Y,
                                                constants.HEALTH_BAR_COLOR)
                health_bar_unit.draw(self.screen)

            # draw score bar
            self.screen.blit(self.score_counter_label, self.score_counter_label_rect)
            for i in range(self.score_counter):
                score_bar_unit = StatusBarUnit(constants.SCORE_BAR_X + (6 * i), constants.STATUS_BAR_Y,
                                               constants.SCORE_BAR_COLOR)
                score_bar_unit.draw(self.screen)

            # draw GAME OVER text if player has run out of lives
            if self.lives_counter == 0 and not self.explosions:
                self.screen.blit(self.game_over_label, self.game_over_label_rect)

            # draw boss ship if score threshold has been met
            if self.score_counter == constants.BOSS_0_SCORE_THRESHOLD and self.boss_ship_present is False:
                self.boss_ship = BossShip0()
                self.boss_ship_group.add(self.boss_ship)
                self.boss_ship_present = True

            if self.score_counter == constants.BOSS_1_SCORE_THRESHOLD and self.boss_ship_present is False:
                self.boss_ship = BossShip1()
                self.boss_ship_group.add(self.boss_ship)
                self.boss_ship_present = True

            # this giant mess controls the behavior of the boss ships
            if self.boss_ship is not None and self.boss_ship_present is True:
                self.boss_ship.draw(self.screen)
                self.boss_ship_movement_timer -= 1
                if self.boss_ship_movement_timer == 0:
                    self.boss_ship.move()
                    self.boss_ship_movement_timer = constants.BOSS_SHIP_MOVEMENT_TIMER
                self.screen.blit(self.boss_health_label, self.boss_health_label_rect)
                for i in range(self.boss_ship.health):
                    health_bar_unit = StatusBarUnit(constants.AMMO_BAR_X + (6 * i), constants.BOSS_HEALTH_BAR_Y,
                                                    constants.BOSS_HEALTH_BAR_COLOR)
                    health_bar_unit.draw(self.screen)
                if self.ship.visible:
                    self.enemy_fire_cooldown_timer -= 1
                if self.ship.visible and self.enemy_fire_cooldown_timer == 0:
                    if type(self.boss_ship) is BossShip0:
                        self.enemy_fires.append(EnemyFire(self.boss_ship.x + 208, self.boss_ship.y + 420))
                        self.enemy_fires.append(EnemyFire(self.boss_ship.x + 78, self.boss_ship.y + 440))
                    elif type(self.boss_ship) is BossShip1:
                        self.enemy_fires.append(EnemyFire(self.boss_ship.x + 18, self.boss_ship.y + 142))
                        self.enemy_fires.append(EnemyFire(self.boss_ship.x + 108, self.boss_ship.y + 420))
                        self.enemy_fires.append(EnemyFire(self.boss_ship.x + 126, self.boss_ship.y + 420))
                        self.enemy_fires.append(EnemyFire(self.boss_ship.x + 196, self.boss_ship.y + 420))
                        self.enemy_fires.append(EnemyFire(self.boss_ship.x + 214, self.boss_ship.y + 420))
                        self.enemy_fires.append(EnemyFire(self.boss_ship.x + 295, self.boss_ship.y + 142))
                    self.enemy_fire_cooldown_timer = random.randrange(100, constants.ENEMY_FIRE_MAX_COOLDOWN_TIME)
                    self.enemy_fire_sound.play()
                if self.boss_ship.health == 0:
                    self.explosions.append(HugeExplosion(self.boss_ship.x, self.boss_ship.y))
                    self.boss_ship_present = False
                    if type(self.boss_ship) is BossShip0:
                        self.boss_ship_0_defeated = True
                        self.boss_ship_group.remove(self.boss_ship)
                        self.enemy_appearance_timer = constants.STAGE_INTRO_TIMER
                        self.stage_intro_timer = constants.STAGE_INTRO_TIMER
                        self.stage_number = 2
                        self.boss_explosion_sound.play()
                    elif type(self.boss_ship) is BossShip1:
                        self.boss_ship_1_defeated = True
                        self.boss_ship_group.remove(self.boss_ship)
                        self.boss_explosion_sound.play()
                    self.score_counter += 1

            # draw explosions, advancing the frame in the game loop to avoid slowing the game down
            if self.explosions:
                self.explosion_cooldown_timer += 1
                for explosion in self.explosions:
                    explosion.draw(self.screen)
                    if self.explosion_cooldown_timer == 50:
                        explosion.current_image += 1
                        if explosion.current_image > 15:
                            self.explosions.remove(explosion)
                if self.explosion_cooldown_timer == 50:
                    self.explosion_cooldown_timer = 0

            # draw title card and instructions
            if self.title_timer > 0:
                self.title_timer -= 1
                self.screen.blit(self.game_title_label_1, self.game_title_label_1_rect)
                self.screen.blit(self.game_title_label_2, self.game_title_label_2_rect)
                self.screen.blit(self.game_title_label_3, self.game_title_label_3_rect)
                self.screen.blit(self.instructions_1_label, self.instructions_1_label_rect)
                self.screen.blit(self.instructions_2_label, self.instructions_2_label_rect)

            # draw stage intro
            if self.stage_intro_timer > 0 and self.title_timer == 0:
                self.stage_intro_timer -= 1
                if self.stage_number == 1:
                    self.screen.blit(self.stage_1_label, self.stage_1_label_rect)
                elif self.stage_number == 2:
                    self.screen.blit(self.stage_2_label, self.stage_2_label_rect)

            if self.boss_ship_0_defeated and self.boss_ship_1_defeated:
                self.screen.blit(self.you_won_label, self.you_won_label_rect)

            # flip video memory
            pygame.display.flip()
