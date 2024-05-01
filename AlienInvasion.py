import sys

import pygame

from Ship import *
from Settings import *
from Bullets import *
from Alien import *


class AlienInvasion:
    def __init__(self):

        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1360, 768))
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bg_color = (90, 155, 255)
        self._create_fleet()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width = 70
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 *alien_width)

        for alien_number in range(number_aliens_x):
            alien = Alien(self)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            self.aliens.add(alien)


    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_height = alien.rect.height
        alien_width = alien.rect.width
        alien.x = 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _bullet_update(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

    def run_game(self):
        while True:
            self.ship.update()
            self._update_screen()
            self._check_events()
            self._bullet_update()
            self._update_aliens()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.allowed_bullets:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.ship.image, self.ship.rect)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += 20
        self.settings.fleet_direction *= -1
