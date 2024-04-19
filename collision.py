from game_object import GameObject
from ball_object import BallObject
import enum
import numpy

class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

compass = [(Direction.UP, numpy.array((0.0, -1.0))),
           (Direction.RIGHT, numpy.array((1.0, 0.0))),
           (Direction.DOWN, numpy.array((0.0, 1.0))),
           (Direction.LEFT, numpy.array((-1.0, 0.0)))]

class Clash:
    def __init__(self,
                 is_clash = False,
                 direction = Direction.UP,
                 penetration = 0.0):
        self.is_clash = is_clash
        self.direction = direction
        self.penetration = penetration
    

class Collision:
    # @staticmethod
    # def _boxCheck(rec1: Rect, rec2: Rect):
    #     if rec1.right>rec2.left and \
    #        rec2.right>rec1.left and \
    #        rec1.bottom>rec2.top and \
    #        rec2.bottom>rec1.top:
    #         return True
    #     return False
    
    @staticmethod
    def box_box_check(one: GameObject, two: GameObject):
        collisionX = one.position[0]+one.size[0] >= two.position[0] and \
                     two.position[0]+two.size[0] >= one.position[0]
        collisionY = one.position[1]+one.size[1] >= two.position[1] and \
                     two.position[1]+two.size[1] >= one.position[1]
        return collisionX and collisionY


    @staticmethod
    def ball_box_check(one: BallObject, two: GameObject):
        circle_pos = numpy.array(one.position)
        circle_center = circle_pos + one.radius

        box_pos = numpy.array(two.position)
        box_half = numpy.array(two.size) / 2.0
        box_center = box_pos + box_half

        # get the point cloest to the ball
        dist = circle_center - box_center
        dist_clip = numpy.clip(dist, -box_half, box_half)
        closest_point = box_center + dist_clip
        closest_vec = closest_point - circle_center

        clash = Clash(False)
        closest_dist = numpy.linalg.norm(closest_vec)
        if closest_dist < one.radius:
            clash.is_clash = True
            clash.direction = Collision._clash_direction(closest_vec)
            if clash.direction==Direction.LEFT or clash.direction==Direction.RIGHT:
                clash.penetration = one.radius - abs(closest_vec[0])
            else:
                clash.penetration = one.radius - abs(closest_vec[1])
        return clash


    @staticmethod
    def _clash_direction(target):
        max = 0.0
        match = Direction.UP

        for dir in compass:
            dot_product = numpy.dot(target, dir[1])
            if dot_product > max:
                max = dot_product
                match = dir[0]
        return match

if __name__ == '__main__':
    t1 = numpy.array([1.0, 0.2])  #right
    t2 = numpy.array([0.1, -1.0]) #up
    t3 = numpy.array([-1.0, -0.1])  #left
    t4 = numpy.array([-0.1, 1.0]) #down
    print(Collision._clash_direction(t1))
    print(Collision._clash_direction(t2))
    print(Collision._clash_direction(t3))
    print(Collision._clash_direction(t4))
    


        


    