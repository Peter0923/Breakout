import moderngl
import numpy

class PostProcessor(object):
    def __init__(self, 
                 ctx: moderngl.Context, 
                 shader: moderngl.Program, 
                 window_size):
        self.ctx = ctx
        self.shader = shader

        # off screen framebuffer
        self.texture = self.ctx.texture(window_size, components=4)
        self.fbo = self.ctx.framebuffer(self.texture)

        self.shader['scene'] = 0
        self.texture.use(0)

        # off screen vao
        vertices = numpy.array([-1.0, 1.0, 0.0, 1.0, -1.0, -1.0, 0.0, 0.0,
                                1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 0.0])
        vbo = self.ctx.buffer(vertices.astype('f4'))
        self.vao = self.ctx.vertex_array(self.shader, vbo, 'in_vert')

        # disable powerup status
        self.shake = False
        self.confuse = False
        self.chaos = False

        # effect parameters
        offset = 1.0 /300.0
        offsets = numpy.array([[-offset, offset], [0.0, offset], [offset, offset],
                               [-offset, 0.0], [0.0, 0.0], [offset, 0.0], 
                               [-offset, -offset], [0.0, -offset], [offset, -offset]])
        blur_kernel = numpy.array([1.0 / 16, 2.0 / 16, 1.0 / 16,
                                   2.0 / 16, 4.0 / 16, 2.0 / 16,
                                   1.0 / 16, 2.0 / 16, 1.0 / 16])
        edge_kernel = numpy.array([-1, -1, -1, -1,  8, -1, -1, -1, -1])

        self.shader['offsets'].write(offsets.astype('f4'))
        self.shader['blur_kernel'].write(blur_kernel.astype('f4'))
        self.shader['edge_kernel'].write(edge_kernel.astype('i4'))


    def beginRender(self):
        # switch to off-screen framebuffer
        self.fbo.use()
        self.ctx.screen.clear(0.0, 0.0, 0.0)
    
    def endRender(self):
        # switch to default framefuffer
        self.ctx.screen.use()
        self.ctx.screen.clear(0.0, 0.0, 0.0)
    
    def render(self, time: float):
        self.shader['shake'] = self.shake
        self.shader['confuse'] = self.confuse
        self.shader['chaos'] = self.chaos
        self.shader['time'] = time
        self.vao.render(moderngl.TRIANGLE_STRIP)