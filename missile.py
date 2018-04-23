import pygame
from pygame.sprite import Sprite

class Missile(Sprite):
    """A class to manage bullets fired from the ship."""
    
    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        super(Missile, self).__init__()
        self.screen = screen
        
        # Load missile image and set its rect.
        self.image = pygame.image.load('images/missile.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # Store the bullet's position as decimal value.
        self.y = float(self.rect.y)
        
        self.speed_factor = ai_settings.missile_speed_factor
        
    
    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)