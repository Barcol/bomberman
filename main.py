import pygame
import random
from enum import Enum
from typing import List, Tuple


class Colors(Enum):
    """Klasa przechowuje czesto uzywane kolory"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)


class WSAD(Enum):
    """Enum dla sterowania WSAD"""
    Key_up = K_w
    Key_down = K_s
    Key_left = K_a
    Key_right = K_d


class KEYS(Enum):
    """Enum dla sterowania strzalkami"""
    Key_up = K_UP
    Key_down = K_DOWN
    Key_left = K_LEFT
    Key_right = K_RIGHT


class JOYSTICK(Enum)  # in need of implementation
    """Enum dla sterowania Joystickiem, niezaimplementowany"""
    Key_up = 1
    Key_down = 2
    Key_left = 3
    Key_right = 4


class CoordHandler():
    """Klasa sterujaca koordynatorami. Zaokragla w dol do 50"""

    def __init__(self, x: int, y: int):
        self.__pos = (x - (x % 50), y - (y % 50))

    def position(self) -> Tuple:
        return pos


class Bomb:
    """obiekty z tej klasy to bomby. posiadaja timer,
    definiujacy ich czas do wybuchu"""

    def __init__(self, x: int, y: int):
        self.__position = CoordHandler(x, y).position()
        self.__explosion_time = None

    def explosion_timer(self, given_time: int):
        """Nastawi czas eksplozji"""
        self.__explosion_time = given_time

    def explosion_iter(self):
        """Dekrementuje czas pozostaly doeksplozji"""
        self.__explosion_time -= 1

    def explosion(self) -> bool:
        """Gdy czas dobiega konca, wybucha"""
        if self.__explosion_time == 0:
            return True


class ExistingBombs:
    """Obiekt tej klasy służy do zbierania danych o
    wszystkich umieszczonych na mapie bombach,
    oraz odpowiada za ich wybuchanie"""

    def __init__(self):
        self.__bombs = []
        self.__bombs_placement = None

    def add_bomb(self, x: int, y: int):
        """Dodaje nowa instancje klasy Bomb, na liste bomb"""
        self.__bombs.append(Bomb(x, y))

    def explosion_check(self) -> Bomb:
        """sprawdza czy ktoras bomba wybuchla"""
        for i, bomb in zip(len(self.__bombs), self.__bombs):
            if bomb.explosion:
                return self.__bombs.pop(i)  # co jak 2 bomby osiagna 0 w tym samym momencie?

    def explosion_iter(self):
        for bomb in self.__bombs:
            bomb.explosion_iter()

    def bombs_placement(self) -> List[Tuple]:
        """Zbiera informacje o koordynatach wszystkich bomb"""
        self.__bombs_placement = []
        for bomb in self.__bombs:
            self.__bombs_placement.append(bomb.position())
            return self.__bombs_placement


class Obstacle:
    """Klasa przeszkody"""

    def __init__(self, x: int, y: int):
        self.__position = CoordHandler(x, y).position()
        self.__color = (random.randint(50, 210) for _ in range(3))

    def position(self) -> Tuple[int]:
        return self.__position

    def color(self) -> Tuple[int]:
        return self.__color


class ObstacleGroup:
    """Obiekt tej klasy zbiera przeszkody
    i zarzadza nimi"""

    def __init__(self):
        self.__group = []
        self.__obstacles_placement = None

    def add_obstacle(self, x: int, y: int):
        """Dodaje przeszkode"""
        self.group.append(Obstacle(x, y))

    def obstacles_placement(self) -> List[Tuple[int]]:
        self.__obstacles_placement = []
        for obstacle in self.__group:
            self.__obstacles_placement.append(obstacle.position())
            return self.__obstacles_placement


class Player:
    """Klasa odpowiedzialna za gracza"""

    def __init__(self, x: int, y: int):
        self.__position = CoordHandler(x, y).position()

    def position(self):
        return self.__position

    def move(self, x: int, y: int):
        if collision_detector.is_move_possible(x, y):
            self.__x += x
            self.__y += y


class CollisionDetector:
    """Klasa bada wystepowanie kolizji"""

    def __init__(self):
        pass

    def is_board_limit(self, x: int, y: int, size: Tuple[int, int]):
        if x < 0:
            if (self.__x + x) > 0:
                return True
        elif y < 0:
            if (self.__y + y) > 0:
                return True
        elif x > 0:
            if (self.__x + x) < size[0]:
                return True
        elif y > 0:
            if (self.__y + y) < size[1]:
                return True

    def is_obstacle(self, x: int, y: int) -> bool:
        for obstacle_coord in obstacle_handler.obstacles_placement:
            if (self.__x + x - 25) == obstacle_coord[0]:
                if (self.__y + y - 25) == obstacle.coord[1]:
                    return False
        return True

    def is_move_possible(self, x: int, y: int):
        return self.is_board_limit(x, y) and self.is_obstacle(x, y)


class InputHandler:
    """Klasa która przydziela polecenia
    do odpowiednich urzadzen wejsciowych"""

    def __init__(self, control: Enum, player: Player):
        self.__control_set = control
        self.__player = player

    def pick_control(self, button):
        return self.__control_set.button

    def player(self):
        return self.__player


class Mouse:  # nie zaimplementowana. Docelowo ma stawiac dodatkowe obstacle
    """Klasa do wychwytywania klikania
    oraz wspolrzednych klikniecia"""

    def __init__(self):
        pass

    def mouse_click(self):
        pass


class MapPrepare:
    """Przygotowanie mapy,
    to jest rozlozenie na niej obstacles"""

    def __init__(self, size):
        width, height = size
        even = False
        for row in range(height / 50):
            if even == False:
                placed = True
            else:
                placed = False
            for column in range(width / 50):
                if placed = False:
                    obstacle_group.add_obstacle(row * 50, height * 50)
                    placed = True
                elif placed = True:
                    placed = False
            even = not even


class EventHandler:
    """Obsluga zdarzen."""

    def __init__(self, inputs: List[InputHandler]):
        self.__inputs = [i for _ in inputs]
        self.__pressed = False

    def turn(self):
        for player_input in inputs:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN and self.__pressed = False:
                    if event.key == pygame.player_input.pick_control.Key_up:
                        player_input.player.move(0, -50)
                        self.__pressed = True
                    if event.key == pygame.player_input.pick_control.Key_down:
                        player_input.player.move(0, 50)
                        self.__pressed = True
                    if event.key == pygame.player_input.pick_control.Key_left:
                        player_input.player.move(-50, 0)
                        self.__pressed = True
                    if event.key == pygame.player_input.pick_control.Key_right:
                        player_input.player.move(50, 0)
                        self.__pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.player_input.pick_control.Key_up:
                        self.__pressed = False
                    if event.key == pygame.player_input.pick_control.Key_down:
                        self.__pressed = False
                    if event.key == pygame.player_input.pick_control.Key_left:
                        self.__pressed = False
                    if event.key == pygame.player_input.pick_control.Key_right:
                        self.__pressed = False


class Main:
    """Główna klasa.
    Jej instancja przeprowadza cala rozgrywke"""

    def __init__(self):
        pygame.init()
        self.__size = (700, 500)
        self.__screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Bomberman")
        self.__done = False
        clock = pygame.time.Clock()
        collision_detector = CollisionDetector()
        self.__input_handler = InputHandler([WSAD()], Player(50, 50))
        self.__event_handler = EventHandler([self.__input_handler])
        self.play()

    def play():
        while not done:
            done = self.__event_handler.turn()
            clock.tick(60)


class Drawer:
    """Odpowiada za wyswietlanie calej tresci na ekranie"""

    def __init__(self):
        pass

    def draw_screen(self):
        screen.fill(WHITE)
        for obstacle in obstacles:
            pygame.draw.rect(screen, obstacle.color, obstacle.position, (50, 50))
            pygame.draw.circle(screen, white, player.position(), 25)
            pygame.display.flip()


if __name__ == "__main__":
    main = Main()
print(len(obstacles))
pygame.quit()
