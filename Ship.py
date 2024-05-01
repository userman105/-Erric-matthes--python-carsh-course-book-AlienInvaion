import pygame


class Ship:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.position = self.rect.x
        self.x = float(self.rect.x)
        self.rect.midbottom = self.screen.get_rect().midbottom
        # MOVEMENT KEYS
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.movement_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= (self.settings.movement_speed + 0.50)
        self.rect.x = self.x
