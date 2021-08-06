class Settings:
    """A class to store settings for Alien Invasion game"""
    def __init__(self) -> None:
        """Initialize the game setting"""
        # Screen setting
        self.screen_width = 600
        self.screen_height = 400
        self.bg_color = (250, 250, 250)

        # ship settings
        self.ship_speed = 0.2
        
        # Bullet settings
        self.bullet_speed = 0.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 0)

        # Alien settings
        self.alien_speed = 0.05
        self.fleet_drop_speed = 10
        # fleet direction: 
        # right : 1
        # left: -1
        self.fleet_direction = 1

        

        