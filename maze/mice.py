from maze import Maze
from maze.directions import directions
from maze.tiles import Wall_tile, Room_tile
from ui import graphics
import heapq
import settings
from ui.music import play_sound
import random


class Mouse:
    def __init__(self, x, y, dir = 0, speed=1):
        self.x, self.y = x, y
        self.size = 1 / 20 # доля тайла, тайлы 1x1
        self.speed = speed # тайлов в секунду
        self.dir = dir

    def draw(self):
        graphics.draw_circle("gray", self.x, self.y, self.size)

    def update(self, delta_time):
        # Ничего не умеет вообще
        pass


# немного интеллекта
class Mouse2(Mouse):
    def __init__(self, x, y, dir=0):
        super().__init__(x, y, dir)
        self.x, self.y = x, y
        self.size = 1 / 20  # доля тайла, тайлы 1x1
        self.speed = 1  # тайлов в секунду
        self.dir = dir

    def draw(self):
        graphics.draw_circle("gray", self.x, self.y, self.size)

    def update(self, delta_time):
        cur_tile = Maze.get_tile(self.x, self.y)
        if cur_tile is None:
            return
        dx, dy = directions[self.dir]
        self.x += dx * self.speed * delta_time
        self.y += dy * self.speed * delta_time
        next_tile = cur_tile.get_neighb_tile(self.dir)
        if cur_tile.dist_to_border(self.x, self.y, self.dir) < 0.2 and (
            next_tile is None or isinstance(next_tile, Wall_tile)):
            self.dir = (self.dir - 1) % 4


class SmartMouse(Mouse):
    def __init__(self, x, y, dir=1, speed=1):
        super().__init__(x, y, dir, speed)
        self.path = []
        self.target = None
        self.img1 = graphics.load_image("images/mouse1.png")
        self.img2 = graphics.load_image("images/mouse2.png")
        self.img3 = graphics.load_image("images/mouse3.png")
        self.img4 = graphics.load_image("images/mouse4.png")

    def update_image(self):
        self.img1 = graphics.load_image("images/mouse1.png")
        self.img2 = graphics.load_image("images/mouse2.png")
        self.img3 = graphics.load_image("images/mouse3.png")
        self.img4 = graphics.load_image("images/mouse4.png")

    def draw(self):
        if self.dir == 1:
            graphics.draw_image(self.img1, self.x-0.5, self.y-0.5)
        elif self.dir == 2:
            graphics.draw_image(self.img2, self.x-0.5, self.y-0.5)
        elif self.dir == 3:
            graphics.draw_image(self.img3, self.x-0.5, self.y-0.5)
        elif self.dir == 4:
            graphics.draw_image(self.img4, self.x-0.5, self.y-0.5)
        else:
            graphics.draw_image(self.img1, self.x-0.5, self.y-0.5)

    def goto_cheese(self, x_cheese, y_cheese):
        start = (int(self.x), int(self.y))
        goal = (int(x_cheese), int(y_cheese))
        self.path = self.a_star_search(start, goal)
        if self.path:
            self.path.append((x_cheese, y_cheese))
        self.target = (x_cheese, y_cheese)

    def a_star_search(self, start, goal):
        open_heap = [(0, start)]
        came_from = {}
        g_cost = {start: 0}

        while open_heap:
            current_cost, current = heapq.heappop(open_heap)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for dx, dy in directions:
                neighbor = (current[0] + dx, current[1] + dy)
                if not self.is_passable(neighbor):
                    continue

                new_cost = g_cost[current] + 1
                if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(open_heap, (priority, neighbor))
                    came_from[neighbor] = current

        return []

    def reconstruct_path(self, came_from, current):
        path = [self.get_tile_center(current)]
        while current in came_from:
            current = came_from[current]
            path.append(self.get_tile_center(current))
        return list(reversed(path))

    def get_tile_center(self, tile):
        return (tile[0] + 0.5, tile[1] + 0.5)

    def get_dir(self, dx, dy):
        if dx > 0:
            return 1
        if dx < 0:
            return 2
        if dy > 0:
            return 3
        if dy < 0:
            return 4

    def update(self, delta_time):
        if random.random() < settings.PIC_CHANCE:
            play_sound("sounds/mouse_short.mp3")
        if Maze.cheese:
            cheese_pos = (Maze.cheese.x, Maze.cheese.y)
            if not self.path or self.target != cheese_pos:
                self.goto_cheese(Maze.cheese.x, Maze.cheese.y)

        if self.path:
            target_x, target_y = self.path[0]
            dx = target_x - self.x
            dy = target_y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance <= self.speed * delta_time:
                self.x, self.y = target_x, target_y
                self.path.pop(0)
            else:
                self.x += dx / distance * self.speed * delta_time
                self.y += dy / distance * self.speed * delta_time

            self.dir = self.get_dir(dx, dy)

    @staticmethod
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def is_passable(pos):
        tile = Maze.get_tile(pos[0], pos[1])
        return isinstance(tile, Room_tile) if tile else False