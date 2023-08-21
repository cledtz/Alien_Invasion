import datetime

class Settings():
    """A class to store all settings for Alien Invasion"""
    
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        #self.bg_color = (230, 230, 230)
        self.bg_color = (0, 0, 255)
        #self.bg_color = (0, 0, 0)
        
        # Ship settings.
        self.ship_limit = 3
        
        # Bullet settings.
        self.bullet_width = 4
        self.bullet_height = 10
        self.bullet_color = (250, 0 , 0)
        self.bullets_allowed = 5
        
        # Missile settings.
        self.missiles_allowed = 2
        
        # Alien settings.
        self.fleet_drop_speed = 50
        
        # How quickly the game speeds up
        self.speedup_scale = 1
        # How quickly the alien point values increase
        self.score_scale = 2
        
        self.initialize_dynamic_settings()
        
    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 5
        self.alien_speed_factor = 0.5
        self.bullet_speed_factor = 8
        self.missile_speed_factor = 16
        
        # Scoring
        self.alien_points = 35

        self.alien_bullets_allowed = 0
        
    
    def increase_speed(self):
        """Increases speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.missile_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)