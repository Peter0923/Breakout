from game_object import GameObject
from resource_manager import ResourceManger

class BallObject(GameObject):
    def __init__(self, position, radius, color, velocity):
        super().__init__(position, (radius*2, radius*2), color, velocity)
        self.radius = radius
        self.stuck = True
        self.pass_through = False
        self.speed_up = 1.0
    
    def move(self, dt, window_width):
        if not self.stuck:
            self.position[0] += self.velocity[0] * self.speed_up * dt
            self.position[1] += self.velocity[1] * self.speed_up * dt

            if self.position[0] < 0:    #left border
                ResourceManger.get_audio('wall').play()
                self.velocity[0] = -self.velocity[0]
                self.position[0] = 0
            elif self.position[0]+self.size[0] > window_width:   #right border
                ResourceManger.get_audio('wall').play()
                self.velocity[0] = -self.velocity[0]
                self.position[0] = window_width-self.size[0]

            if self.position[1] < 0:    #top border
                ResourceManger.get_audio('wall').play()
                self.velocity[1] = -self.velocity[1]
                self.position[1] = 0
        return self.position

    def reset(self, position, color, velocity):
        super().reset(position, color, velocity=velocity)
        self.stuck = True
        self.pass_through = False
        self.speed_up = 1.0

    
