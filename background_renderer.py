import moderngl as gl
import numpy
from pyrr import Matrix44
from game_object import GameObject
from resource_manager import ResourceManger

class BackgroundRenderer():
    def __init__(self, 
                 shader,
                 ctx: gl.Context,
                 wnd_size):
        self.prog = shader

        background = GameObject((0, 0), wnd_size)
        self.prog['pos'].write(numpy.array(background.position).astype('f4'))
        self.prog['size'].write(numpy.array(background.size).astype('f4'))
        self.prog['color'].write(numpy.array(background.color).astype('f4'))

        vertices = numpy.array([
            0.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 1.0,
            1.0, 0.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 1.0])      
        vbo = ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = ctx.vertex_array(self.prog, vbo, 'vertex')

        texture = ResourceManger.get_texture('background')
        self.prog['image'] = 1
        texture.use(1)

    
    def draw(self):
        self.vao.render(gl.TRIANGLE_STRIP)
    

