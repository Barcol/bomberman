from obstacle import Obstacle
import math


class ObstaclePlacer:
    def __init__(self):
        pass

    def get_number_obstacles_x(self, game_settings, obstacle_width, tabulator):
        available_space_x = game_settings.screen_width - obstacle_width
        number_obstacles_x = int(math.ceil(available_space_x / (2 * obstacle_width)))
        if not tabulator:
            number_obstacles_x += 1
        return number_obstacles_x

    def get_number_rows(self, game_settings, obstacle_height):
        available_space_y = game_settings.screen_height
        number_rows = int(available_space_y / obstacle_height)
        return number_rows

    def create_obstacle(self, game_settings, screen, obstacles, obstacle_number, row_number, tabulator, spirit):
        obstacle = Obstacle(game_settings, screen, spirit)
        obstacle_width = obstacle.rect.width
        obstacle.x = tabulator + 2 * obstacle_width * obstacle_number
        obstacle.rect.x = obstacle.x
        obstacle.rect.y = obstacle.rect.height * row_number
        obstacles.add(obstacle)

    def create_hard_obstacles(self, game_settings, screen, obstacles):
        obstacle = Obstacle(game_settings, screen, "hard_obstacle.bmp")
        obstacle_width = obstacle.rect.width
        number_rows = self.get_number_rows(game_settings, obstacle.rect.height)
        for row_number in range(math.floor(number_rows / 2)):
            for obstacle_number in range(self.get_number_obstacles_x(game_settings, obstacle_width, 0) - 1):
                self.create_obstacle(game_settings, screen, obstacles, obstacle_number, 1 + (2 * row_number),
                                     obstacle_width, "hard_obstacle.bmp")

    def create_obstacles(self, game_settings, screen, obstacles):
        obstacle = Obstacle(game_settings, screen, "obstacle.bmp")
        obstacle_width = obstacle.rect.width
        number_rows = self.get_number_rows(game_settings, obstacle.rect.height)
        for row_number in range(number_rows):
            if (row_number % 2) != 0:
                tabulator = 0
            else:
                tabulator = obstacle.rect.height
            for obstacle_number in range(self.get_number_obstacles_x(game_settings, obstacle_width, tabulator)):
                if (row_number == 0) or (row_number == 1):
                    obstacle_number += 1
                if (row_number == number_rows - 1) or (row_number == (number_rows - 2)):
                    obstacle_number -= 1
                self.create_obstacle(game_settings, screen, obstacles, obstacle_number, row_number, tabulator,
                                     "obstacle.bmp")