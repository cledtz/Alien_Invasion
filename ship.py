import pygame
from pygame.sprite import Sprite
import datetime

class Ship(Sprite):
    
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.center_ship()
        
        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)
        
        # Movement flags.
        self.moving_right = False
        self.moving_left = False
        now = datetime.datetime.now()
        diff = datetime.timedelta(seconds=10)
        self.misiles_time = [now - diff] * 3
    
    def center_ship(self):
        """Put a ship in the initial position."""
        self.rect.centerx = self.screen_rect.centerx
        self.center = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 50
        
    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor
        
        # Update rect object form self.center.
        self.rect.centerx = self.center
        
    def blitme(self):
        """"Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)