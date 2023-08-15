import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    
    def __init__(self, ai_settings, screen, health = 1):
        """Initialize the alien and set its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/ufo.png')
        self.explosion = pygame.image.load('images/explosion.png')
        self.explosion_sound = pygame.mixer.Sound("images/explosion.wav")
        self.rect = self.image.get_rect()
        delete = False
        
        # Start each new alien near the top lever of the screen.
        self.rect.x = self.rect.width/2
        self.rect.y = self.rect.height/2
        
        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # (direction > 1) => right movement; left for negative
        self.direction = 1

        self.health = health
        self.exploded = 0

    def blitme(self, screen):
        """Draw the alien at its current location."""
        # self.screen.blit(self.image, self.rect)
        if self.health >= 1:
            h_box1 = (self.rect.x + 25, self.rect.y - 15, 10, 10)
            h_box2 = (h_box1[0] + 15, self.rect.y - 15, 10, 10)
            h_box3 = (h_box2[0] + 15, self.rect.y - 15, 10, 10)
            pygame.draw.rect(screen, (255*(self.health < 1),128*(self.health >= 1),0), h_box1)
            pygame.draw.rect(screen, (255*(self.health < 2),128*(self.health >= 2),0), h_box2)
            pygame.draw.rect(screen, (255*(self.health < 3),128*(self.health >= 3),0), h_box3)

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
        