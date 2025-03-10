import settings
from maze.mice import SmartMouse
from maze.tiles import Room_tile, Wall_tile
from maze.cheese import Cheese
import random
from ui.music import play_sound

maze = []
mice = []
cheese = None
##########################################################
# Грузим карту
with open(settings.map_file) as f:
    map_txt = f.readlines()
# Строим карту из настоящих объектных тайлов
for row, line in enumerate(map_txt):
    maze.append([])
    for column, tile_type in enumerate(line[:-1]):
        if tile_type == "0":
            maze[row].append(Room_tile(row, column))
        else:
            maze[row].append(Wall_tile(row, column))
###########################################################


# Рисуем все: и тайлы и мышей
def draw():
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            maze[row][column].draw()

    if cheese is not None:
        cheese.draw()

    for mouse in mice:
        mouse.draw()


# Получаем тайл по координатам лабиринта
def get_tile(x, y):
    if 0 <= y <= len(maze) and 0 <= x <= len(maze[0]):
        tile_column, tile_row = int(x), int(y)

        try:
            return maze[tile_row][tile_column]
        except:
            return 1
    else:
        return None


def find_random_empty_tile():
    empty_tiles = [(row, col) for row in range(len(maze)) for col in range(len(maze[row])) if isinstance(maze[row][col], Room_tile)]
    return random.choice(empty_tiles) if empty_tiles else None

def update(delta_time):
    global cheese
    for mouse in mice:
        mouse.update(delta_time)
        if cheese and abs(mouse.x - cheese.x) < mouse.size and abs(mouse.y - cheese.y) < mouse.size:
            empty_tile = find_random_empty_tile()
            if empty_tile:
                play_sound("sounds/eat.mp3")
                cheese = Cheese(empty_tile[1] + 0.5, empty_tile[0] + 0.5)


def add_mouse(x, y, speed):
    mice.append(SmartMouse(int(x)+0.5, int(y)+0.5, speed=speed))
    play_sound("sounds/mouse.mp3")

def add_cheese(x, y, playsound=True):
    global cheese
    cheese = Cheese(int(x)+0.5, int(y)+0.5)
    if playsound:
        play_sound("sounds/cheese.mp3")
