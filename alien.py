import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, ai_settings, screen):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/ufo.png')
        self.rect = self.image.get_rect()
        
        # Start each new alien near the top lever of the screen.
        self.rect.x = self.rect.width/2
        self.rect.y = self.rect.height/2
        
        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # (direction > 1) => right movement; left for negative
        self.direction = 1
        
    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Return True if alien is at edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Move the alien right of left"""
        self.x += (self.ai_settings.alien_speed_factor * self.direction)
        self.rect.x = self.x
        