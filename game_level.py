from game_object import GameObject
from resource_manager import ResourceManger
from brick_settings import BrickSettings
import os

power_duration = 10

class GameLevel():
    def __init__(self):
        self.bricks = []
        self.grid = dict()

    def load_data(self, file, level_width, level_height):
        self.bricks.clear()
        data = ResourceManger.load_game_level(file)
        width = len(data[0])
        height = len(data)
        self.unitWidth = level_width/width
        self.unitHeight = level_height/height

        for y in range(height):
            for x in range(width):
                number = data[y][x]
                if number < 1:
                    continue

                pos = (self.unitWidth*x, self.unitHeight*y)
                size = (self.unitWidth, self.unitHeight)

                brick = GameObject(pos, size)
                brick.texture = BrickSettings.get_texture(number)
                brick.color = BrickSettings.get_color(number)
                brick.is_solid = BrickSettings.is_solid(number)
                brick.powerup = BrickSettings.get_powerup(number)

                self.bricks.append(brick)
                self.grid[(x, y)] = brick

    # def drawBricks(self, renderer):
    #     solid_blocks = []
    #     blocks = []
    #     for brick in self.bricks:
    #         if not brick.destroyed:
    #             if brick.is_solid is True:
    #                 solid_blocks.append(brick)
    #             else:
    #                 blocks.append(brick)
        
    #     solid_texture = ResourceManger.get_texture('block_solid')
    #     renderer.drawObjects(solid_texture, solid_blocks)

    #     block_texture = ResourceManger.get_texture('block')
    #     renderer.drawObjects(block_texture, blocks)
    
    def is_complete(self):
        for brick in self.bricks:
            if (brick.is_solid==False) and (brick.destroyed==False):
                return False
        return True
    
    def reset(self):
        for brick in self.bricks:
            brick.destroyed = False

if __name__ == '__main__':
    # test level data
    resource_dir = os.path.normpath(os.path.join(__file__, '../resource'))
    ResourceManger.initialize(resource_dir)
    data = ResourceManger.load_game_level("one.lvl")
    for row in data:
        print(row)
    

