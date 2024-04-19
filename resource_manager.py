from moderngl_window import resources
from moderngl_window.meta import (
    TextureDescription, 
    ProgramDescription,
    DataDescription)
from os import path
import freetype
import pyglet

class ResourceManger():
    _resource_dir = None
    _shaders = {}
    _textures = {}
    _audio = {}

    @classmethod
    def initialize(cls, resource_dir):
        cls._resource_dir = resource_dir
        # resources.register_dir(Path(resource_dir))
        resources.register_dir(resource_dir)
        pyglet.resource.path = [path.join(resource_dir, "audio"), 
                                path.join(resource_dir, "levels")]

    @classmethod
    def load_all_resources(cls):
        # background shader
        cls._shaders['background'] = ResourceManger._load_program(
            vertex_shader="shaders/background.vs",
            fragment_shader="shaders/background.fs")

        # sprite shader
        cls._shaders['sprite']  = ResourceManger._load_program(
            vertex_shader="shaders/sprite.vs",
            fragment_shader="shaders/sprite.fs")
        
        # particle shader
        cls._shaders['particle'] = ResourceManger._load_program(
            vertex_shader="shaders/particle.vs",
            fragment_shader="shaders/particle.fs")

        # postprocess shader
        cls._shaders['postprocess'] = ResourceManger._load_program(
            vertex_shader="shaders/process.vs",
            fragment_shader="shaders/process.fs")
        
        # text shader
        cls._shaders['text'] = ResourceManger._load_program(
            vertex_shader="shaders/text.vs",
            fragment_shader="shaders/text.fs")
        
        # background texture
        cls._textures['background'] = ResourceManger._load_texture_2d(
            "textures/background.jpg")
        
        # paddle texture
        cls._textures['paddle'] = ResourceManger._load_texture_2d(
            "textures/paddle.png")
        
        # block_solid texture
        cls._textures['block_solid'] = ResourceManger._load_texture_2d(
            "textures/block_solid.png")
        
        # block texture
        cls._textures['block'] = ResourceManger._load_texture_2d(
            "textures/block.png")
        
        # ball texture
        cls._textures['ball'] = ResourceManger._load_texture_2d(
            "textures/ball.png")
        
        # particle texture
        cls._textures['particle'] = ResourceManger._load_texture_2d(
            "textures/particle.png")
        
        # sounds
        cls._audio['breakout'] = pyglet.resource.media("breakout.mp3", False)
        cls._audio['solid'] = pyglet.resource.media("solid.wav", False)
        cls._audio['non-solid'] = pyglet.resource.media("bleep.mp3", False)
        cls._audio['powerup'] = pyglet.resource.media("powerup.wav", False)
        cls._audio['wall'] = pyglet.resource.media("bleep.wav", False)
        
    @classmethod
    def get_shader(cls, name):
        return cls._shaders[name]
    
    @classmethod
    def get_texture(cls, name):
        return cls._textures[name]
    
    @classmethod
    def get_audio(cls, name):
        return cls._audio[name]
    
    @classmethod
    def load_game_level(cls, filename: str):
        data = []
        with pyglet.resource.file(filename) as f:
            for line in f:
                row = list(map(int, line.split()))
                data.append(row)
        return data
    
    @classmethod
    def load_font(cls, fontname, height):
        font_path = path.join(cls._resource_dir, "fonts", fontname)
        face = freetype.Face(font_path)
        face.set_pixel_sizes(0, height)
        return face
    
    @classmethod
    def _load_program(cls,
                     vertex_shader=None, 
                     geometry_shader=None, 
                     fragment_shader=None):
        prog = resources.programs.load(ProgramDescription(
            vertex_shader=vertex_shader,
            geometry_shader=geometry_shader,
            fragment_shader=fragment_shader))
        return prog

    @classmethod
    def _load_texture_2d(cls, path: str):
        texture = resources.textures.load(TextureDescription(path=path))
        return texture
    
    @classmethod
    def _load_data(cls, path: str, kind='text'):
        data = resources.data.load(DataDescription(path=path , kind=kind))
        return data
    
