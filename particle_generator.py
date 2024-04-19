import random
import numpy
import moderngl
from game_object import GameObject

particle_amount = 800
particle_updates = 2
particle_scale = 10.0

class Particle(object):
    def __init__(self, 
                 positon=[0.0, 0.0], 
                 velocity=[0.0, 0.0], 
                 color=[0.0, 0.0, 0.0, 1.0], 
                 life=0.0):
        self.position = positon
        self.velocity = velocity
        self.color = color
        self.life = life

class ParticleGenerator(object):
    def __init__(self,
                 ctx, 
                 shader,
                 texture):
        self.ctx = ctx  
        self.texture = texture
        self.shader = shader
        self.shader['scale'].value = particle_scale

        # init particles
        self.particles = [Particle() for i in range(particle_amount)]
        self.last_used = 0

        # rendering VBO
        quad = numpy.array([
            0.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 1.0,
            1.0, 0.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 1.0], 
            dtype='f4')
        self.vbo = self.ctx.buffer(quad)
        self.vao = self.ctx.vertex_array(self.shader, self.vbo, 'vertex')

        # instanced VBO
        self.vbo1 = self.ctx.buffer(reserve=particle_amount*24, dynamic=True)
        self.vao.bind(self.shader['offset'].location, cls='f', buffer=self.vbo1, 
                      fmt='2f', offset=0, stride=24, divisor=1)
        self.vao.bind(self.shader['color'].location, cls='f', buffer=self.vbo1,
                      fmt='4f', offset=8, stride=24, divisor=1)
        
        # bind texture
        self.shader['sprite'] = 3
        self.texture.use(3)
        
    def update(self, dt:float, object:GameObject, offset):
        # update particles
        for i in range(particle_updates):
            unused = self._firstUnusedParticle()
            if unused == -1:
                break
            self._respawnParticle(self.particles[unused], 
                                  object.position,
                                  offset,
                                  object.velocity)
        
        for i in range(particle_amount):
            p = self.particles[i]
            p.life -= dt
            if p.life > 0.0:
                p.position[0] -= p.velocity[0] * dt
                p.position[1] -= p.velocity[1] * dt
                p.color[3] -= dt * 2.5
    
    def draw(self):
        # prepare buffer
        instance_data = []
        for particle in self.particles:
            if particle.life > 0.0:
                instance_data.extend(particle.position)
                instance_data.extend(particle.color)
        count = int(len(instance_data)/6)
    
        # update buffer
        instance_data = numpy.array(instance_data, dtype='f4')
        self.vbo1.write(instance_data)

        # rendering
        self.ctx.blend_func = self.ctx.SRC_ALPHA, self.ctx.ONE
        self.vao.render(moderngl.TRIANGLE_STRIP, instances = count)
        self.ctx.blend_func = self.ctx.SRC_ALPHA, self.ctx.ONE_MINUS_SRC_ALPHA
    
    def reset(self):
        for particle in self.particles:
            particle.life = 0.0
        self.last_used = 0

    def _firstUnusedParticle(self):
        for i in range(self.last_used, particle_amount):
            if self.particles[i].life <= 0.0:
                self.last_used = i
                return i
        
        for i in range(self.last_used):
            if self.particles[i].life <= 0.0:
                self.last_used = i
                return i
        
        self.last_used = 0
        return -1
    
    def _respawnParticle(self, particle: Particle, position, offset, velocity):
        r_pos = random.uniform(-5, 5)
        r_color = random.uniform(0.5, 1.5)
        particle.position = [position[0] + offset + r_pos, 
                             position[1] + offset + r_pos]
        particle.color = [r_color, r_color, r_color, 1.0]
        particle.life = 1.0
        particle.velocity = [velocity[0]*0.1, velocity[1]*0.1]