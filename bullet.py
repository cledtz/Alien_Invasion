import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    
    def __init__(self, ai_settings, screen, ship, direction = 1, bullet_speed = 0):
        """Create a bullet object at the ship's current position."""
        super(Bullet, self).__init__()
        self.screen = screen
        
        # Load bullet image and set its rect.
        self.image = pygame.image.load('images/missile.png')
        self.rect = self.image.get_rect()
        
        # Create a bullet rect at (0, 0) and then correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.color = ai_settings.bullet_color
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # Store the bullet's position as decimal value.
        self.y = float(self.rect.y)
        
        if bullet_speed == 0:
            self.speed_factor = direction * ai_settings.bullet_speed_factor
        else:
            self.speed_factor = direction * bullet_speed
        
    
    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y
        
    
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
