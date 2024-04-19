import moderngl as gl
import numpy
from pyrr import Matrix44
from game_object import GameObject
from resource_manager import ResourceManger

max_instances = 128
layer_width, layer_height, layers = 512, 128, 4

class SpriteRenderer():
    def __init__(self, 
                 shader:gl.Program,
                 ctx: gl.Context):
        self.prog = shader
        self.instance_count = 0

        # vertex buffer
        vertices = numpy.array([
            0.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 1.0,
            1.0, 0.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 1.0])
        vbo = ctx.buffer(vertices.astype('f4').tobytes())
        self.vao = ctx.vertex_array(self.prog, vbo, 'vertex')

        # instanced vertex buffer
        self.vbo_instance = ctx.buffer(reserve=40*max_instances)
        self.vao.bind(self.prog['pos'].location, cls='f', buffer=self.vbo_instance,
                      fmt='2f', offset=0, stride=40, divisor=1)
        self.vao.bind(self.prog['size'].location, cls='f', buffer=self.vbo_instance,
                      fmt='2f', offset=8, stride=40, divisor=1)
        self.vao.bind(self.prog['color'].location, cls='f', buffer=self.vbo_instance,
                      fmt='3f', offset=16, stride=40, divisor=1)
        self.vao.bind(self.prog['layer'].location, cls='f', buffer=self.vbo_instance,
                      fmt='3f', offset=28, stride=40, divisor=1)

        # texture array
        textures = ctx.texture_array((layer_width, layer_height, layers), 4)

        # paddle: layer = 0
        paddle = ResourceManger.get_texture('paddle')
        buffer = ctx.buffer(reserve=paddle.width * paddle.height * 4)
        paddle.read_into(buffer)
        textures.write(buffer, viewport=(0, 0, 0, paddle.width, paddle.height, 1))

        # ball: layer = 1
        ball = ResourceManger.get_texture('ball')
        buffer = ctx.buffer(reserve=ball.width * ball.height * 4)
        ball.read_into(buffer)
        textures.write(buffer, viewport=(0, 0, 1, ball.width, ball.height, 1))

        # block: layer = 2
        block = ResourceManger.get_texture('block')
        buffer = ctx.buffer(reserve=block.width * block.height * 4)
        block.read_into(buffer)
        textures.write(buffer, viewport=(0, 0, 2, block.width, block.height, 1))

        # solid block: layer = 3
        block = ResourceManger.get_texture('block_solid')
        buffer = ctx.buffer(reserve=block.width * block.height * 4)
        block.read_into(buffer)
        textures.write(buffer, viewport=(0, 0, 3, block.width, block.height, 1))

        # bind textures
        self.prog['image'] = 2
        textures.use(2)

    def resetBuffer(self):
        self.instance_count = 0    

    def updateBuffer(self, objects: list[GameObject], layout):
        data = []
        for object in objects:
            data.extend(object.position)
            data.extend(object.size)
            data.extend(object.color)
            data.extend([object.texture.width/layer_width,
                         object.texture.height/layer_height,
                         layout])
        self.vbo_instance.write(numpy.array(data).astype('f4'), 40*self.instance_count)
        self.instance_count += len(objects)
    
    def draw(self):
        self.vao.render(gl.TRIANGLE_STRIP, instances=self.instance_count)