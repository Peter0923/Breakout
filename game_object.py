import moderngl as gl
# from sprite_renderer import SpriteRenderer

class GameObject():
    def __init__(self,
                 position, size,
                 color = (1.0, 1.0, 1.0),
                 velocity = (0.0, 0.0),
                 rotation = 0.0,
                 is_solid = False,
                 destroyed = False):
        self.position = position
        self.size = list(size)
        self.color = color
        self.velocity = list(velocity)
        self.rotation = rotation
        self.is_solid = is_solid
        self.destroyed = destroyed
        self.powerup = None
        self.texture = None
        self.add_length = 0
    
    def resize(self, add_length):
        self.size[0] -= self.add_length
        self.add_length = add_length
        self.size[0] += self.add_length

    def reset(self, postion, color, size = None, velocity = None):
        self.position = postion
        self.color = color
        self.add_length = 0
        if size is not None:
            self.size = list(size)
        if velocity is not None:
            self.velocity = list(velocity)
        

    

