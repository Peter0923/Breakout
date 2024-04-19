import ctypes
import numpy
import moderngl
from OpenGL import GL
from os import path
from resource_manager import ResourceManger

# Optimized text rendering:
# 1. One time draw to render all text
# 2. Use Texture array to store all font images

texture_width = 64
texture_height = 64
texture_layers = 64

all_text = "0123456789Lives:Level:PressENTERtostartPressWorStoselectlevelYouWIN!continueGamepaused "

class Character(object):
    def __init__(self, layer, size, bearing, advance):
        self.layer = layer
        self.size = size
        self.bearing = bearing
        self.advance = advance

class TextContent(object):
    def __init__(self, text, x, y, scale=1.0, color=(1.0, 1.0, 1.0)):
        self.text = text
        self.x = x
        self.y = y
        self.scale = scale
        self.color = color

class TextRenderer(object):
    def __init__(self,
                 ctx: moderngl.Context,
                 shader: moderngl.Program):
        self.ctx = ctx
        self.shader = shader
        self.shader['textColor'] = (1.0, 1.0, 1.0)

        self.vbo = self.ctx.buffer(reserve=6*5*4*texture_layers, dynamic=True)
        self.vao = self.ctx.vertex_array(self.shader, self.vbo, 'vertex', 'texcoords')

        # create texture array
        self.textures = self.ctx.texture_array((texture_width, texture_height, texture_layers), 1)
        self.shader['text4'] = 4
        self.textures.use(4)
        self.chars = dict()

    def load(self, fontname, height):
        self.face = ResourceManger.load_font(fontname, height)

        layer = 0
        for c in all_text:
            if c in self.chars:
                continue

            self.face.load_char(c)
            width = self.face.glyph.bitmap.width
            height = self.face.glyph.bitmap.rows
            data = numpy.array(self.face.glyph.bitmap.buffer).astype(numpy.uint8)
            self.textures.write(data, viewport=(0, 0, layer, width, height, 1))
        
            self.chars[c] = Character(
                layer, (width, height),
                (self.face.glyph.bitmap_left, self.face.glyph.bitmap_top),
                self.face.glyph.advance.x)
            layer += 1
    
    def updateBuffers(self, texts):
        vertices = []
        for text in texts:
            x = text.x
            y = text.y
            for c in text.text:
                ch = self.chars[c]
                xpos = x + ch.bearing[0] * text.scale
                ypos = y + (ch.size[1] - ch.bearing[1]) * text.scale
                w = ch.size[0] * text.scale
                h = ch.size[1] * text.scale
                rw = ch.size[0] / texture_width    #remap texture x
                rh = ch.size[1] / texture_height   #remap texture y
                vertices.extend([
                    xpos, ypos-h, 0.0, 0.0, ch.layer,
                    xpos, ypos, 0.0, 1.0*rh, ch.layer,
                    xpos+w, ypos-h, 1.0*rw, 0.0, ch.layer,
                    xpos+w, ypos-h, 1.0*rw, 0.0, ch.layer,
                    xpos, ypos, 0.0, 1.0*rh, ch.layer,
                    xpos+w, ypos, 1.0*rw, 1.0*rh, ch.layer])
                x += (ch.advance >> 6) * text.scale
        
        self.vbo.clear()
        self.vbo.write(numpy.array(vertices).astype(numpy.float32))

    def render(self):
        self.vao.render(moderngl.TRIANGLES)

if __name__ == '__main__':
    resource_path = path.normpath(path.join(__file__, '../resource'))
    ResourceManger.initialize(resource_path)
    face = ResourceManger.load_font("arial.ttf", 16)
    face.load_char('S')
    print("width: ", face.glyph.bitmap.width)
    print("height: ", face.glyph.bitmap.rows)
    print("bearingX: ", face.glyph.bitmap_left)
    print("bearingY: ", face.glyph.bitmap_top)
    print("advance: ",  face.glyph.advance.x)
    print("buffer: ", face.glyph.bitmap.buffer)
