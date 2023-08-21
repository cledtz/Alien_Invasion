class GameStats():
    """Track statistics for Alien Invasion."""
    

    xcount = 0

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.score = 0
        self.ai_settings = ai_settings
        self.reset_stats()
        # Start Alien Invasion in an active state.
        self.game_active = False
        self.has_won = True
        self.games_won = 0
        # High score should never be reset.
        self.high_score = 0
        
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1