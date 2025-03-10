from maze import Maze
from maze.directions import directions
from maze.tiles import Wall_tile, Room_tile
from ui import graphics

class Cheese:
    def __init__(self,x,y):
        self.x, self.y = x, y
        self.size = 1/20
        self.speed = 1
        self.image = graphics.load_image('images/cheese.png')

    def draw(self):
        self.update_image()
        graphics.draw_image(self.image, self.x-0.5, self.y-0.5)


    def update_image(self):
        self.image = graphics.load_image('images/cheese.png')