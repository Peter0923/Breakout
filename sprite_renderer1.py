import moderngl as gl
import numpy
from pyrr import Matrix44
from game_object import GameObject

class SpriteRenderer():
    def __init__(self, 
                 shader:gl.Program,
                 ctx: gl.Context):
        self.prog = shader

        vertices = numpy.array([
            0.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 1.0,
            1.0, 0.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 1.0])
        
        vbo = ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = ctx.vertex_array(self.prog, vbo, 'vertex')
    
    # Note: Matrix calculation is a CPU killer! 
    # 1. CPU drop from 370% to 55% when moving calculate mode-view matrix to GPU
    # 2. CPU drop from 55% to 25% when moving RST matrix generation to GPU
    # 3. CPU drops from 25% to 20% when using grid to detect collision
    def drawObject(self, object: GameObject):
        self.prog['pos'].write(numpy.array(object.position).astype('f4'))
        self.prog['size'].write(numpy.array(object.size).astype('f4'))
        self.prog['color'].write(numpy.array(object.color).astype('f4'))

        # bind texture
        self.prog['image'] = 0
        object.texture.use(0)

        # draw the object
        self.vao.render(gl.TRIANGLE_STRIP)
    
    # Draw multiple objects one time (instanced rendering)
    def drawObjects(self, texture, objects: list[GameObject]):
        positions, sizes, colors = [], [], []
        for object in objects:
            positions.append(object.position)
            sizes.append(object.size)
            colors.append(object.color)
        
        self.prog['pos'].write(numpy.array(positions).astype('f4'))
        self.prog['size'].write(numpy.array(sizes).astype('f4'))
        self.prog['color'].write(numpy.array(colors).astype('f4'))

        # bind texture
        self.prog['image'] = 0
        texture.use(0)

        # draw the object
        self.vao.render(gl.TRIANGLE_STRIP, instances=len(objects))
    

