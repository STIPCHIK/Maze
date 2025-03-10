import settings
from maze import Maze
from maze.Maze import cheese
from maze.tiles import Room_tile, Wall_tile
from settings import tile_size
from tasks import tasks
from ui import events
from ui import graphics
from ui import screen
from ui.graphics import load_image
from ui.music import play_music
import random

FPS = 60
running = True
clock = events.Clock()

dragx = 0
dragy = 0
update_tiles = 0
play_music("sounds/music.mp3")

while running:
    for event in events.get_event_queue():
        if tasks.handle_event(event):
            continue
        if event.type == events.QUIT:
           running = False
        if event.type == events.MOUSEBUTTONDOWN:
            if event.button == 1:
                if type(Maze.get_tile((event.pos[0]-settings.view_left_top[0]) / settings.tile_size[0], (event.pos[1]-settings.view_left_top[1]) / settings.tile_size[1])) == Wall_tile:
                    dragx = event.pos[0]
                    dragy = event.pos[1]
                elif type(Maze.get_tile((event.pos[0]-settings.view_left_top[0]) / settings.tile_size[0], (event.pos[1]-settings.view_left_top[1]) / settings.tile_size[1])) == Room_tile:
                    Maze.add_mouse((event.pos[0]-settings.view_left_top[0]) / settings.tile_size[0], (event.pos[1]-settings.view_left_top[1]) / settings.tile_size[1], speed=random.choice([1, 1.5, 2, 2.5, 3]))
            if event.button == 3:
                Maze.add_cheese((event.pos[0]-settings.view_left_top[0]) / settings.tile_size[0], (event.pos[1]-settings.view_left_top[1]) / settings.tile_size[1])

        if event.type == events.MOUSEMOTION and dragx:
            settings.view_left_top[0] -= dragx - event.pos[0]
            settings.view_left_top[1] -= dragy - event.pos[1]
            settings.view_left_top[0] = max(10 - len(Maze.maze[0])*tile_size[0], settings.view_left_top[0])
            settings.view_left_top[1] = max(10 - len(Maze.maze)*tile_size[1], settings.view_left_top[1])
            settings.view_left_top[0] = min(settings.view_left_top[0], screen.get_size()[0] - 10)
            settings.view_left_top[1] = min(settings.view_left_top[1], screen.get_size()[1] - 10)
            dragx = event.pos[0]
            dragy = event.pos[1]

        if event.type == events.MOUSEBUTTONUP:
            dragx = 0
            dragy = 0

        if event.type == events.MOUSEWHEEL:


            if update_tiles == 1:
                for row in range(len(Maze.maze)):
                    for column in range(len(Maze.maze[row])):
                        Maze.maze[row][column].update_image()
                try:
                    for mouse in Maze.mice:
                        mouse.update_image()
                except:
                    pass

            update_tiles %= 1
            update_tiles += 1
            if event.y > 0:
                tile_size[0] *= 1.02
                tile_size[1] *= 1.02
            else:
                tile_size[0] *= 0.98
                tile_size[1] *= 0.98



    graphics.fill("black")
    # рисуем лабиринт
    Maze.draw()
    tasks.check_tasks()
    graphics.flip()
    clock.tick(FPS)
    Maze.update(1 / FPS)
