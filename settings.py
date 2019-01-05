class Settings():
    def __init__(self):
        self.screen_width = 1241
        self.screen_height = 825
        self.bg_color = (41, 193, 49)

        self.character_speed = 4

        self.bomb_width = 10
        self.bomb_height = 10
        self.bomb_color = 60, 60, 60
        self.bomb_speed_factor = 1
        self.bombs_allowed = 3

        self.explosion_size = 150
        self.explosion_width = 20

        self.character_speed_boost = 0.4
        self.explosion_boost = 25
        self.bombs_allowed_boost = 1