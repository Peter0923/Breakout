import enum
import numpy
import moderngl as gl
from moderngl_window import BaseWindow
from game_object import GameObject
from resource_manager import ResourceManger
from game_level import GameLevel
from ball_object import BallObject
from sprite_renderer import SpriteRenderer
from pyrr import Matrix44
from collision import Collision, Direction
from particle_generator import ParticleGenerator
from post_processor import PostProcessor
from text_renderer import TextRenderer, TextContent
from background_renderer import BackgroundRenderer

# paddle
paddle_size = (100, 20)
paddle_velocity = 500.0

# ball
ball_init_velocity = (100.0, -350.0)
ball_radius = 13.5
ball_color = (135/255.0, 206/255.0, 245/255.0)

# powerup
powerup_speed = 1.5
powerup_duration = 10
shake_time = 0.02

# game lives
max_life = 3

class GameState(enum.Enum):
    kGameMenu = 0
    kGameActive = 1
    kGamePause = 2
    kGameWin = 3

class Game(object):
    def __init__(self, wnd_size,
                 ctx: gl.Context):
        self.ctx = ctx
        self.width = wnd_size[0]
        self.height = wnd_size[1]
        self.state = GameState.kGameMenu
        self.life = max_life
       
        projection = Matrix44.orthogonal_projection(
            0.0, self.width, 
            self.height, 0.0, 
            -1.0, 1.0)
        
        # init background renderer
        background_shader = ResourceManger.get_shader('background')
        background_shader['projection'].write(projection.astype('f4'))
        self.background_renderer = BackgroundRenderer(background_shader, self.ctx, wnd_size)
        
        # init sprite renderer
        sprite_shader = ResourceManger.get_shader('sprite')
        sprite_shader['projection'].write(projection.astype('f4'))
        self.sprite_renderer = SpriteRenderer(sprite_shader, self.ctx)

        # init particle renderer
        particle_shader = ResourceManger.get_shader('particle')
        particle_shader['projection'].write(projection.astype('f4'))
        particle_texture = ResourceManger.get_texture('particle')
        self.particle_generator = ParticleGenerator(self.ctx, particle_shader, particle_texture)

        # init post processor
        postprocess_shader = ResourceManger.get_shader('postprocess')
        self.post_processor = PostProcessor(self.ctx, postprocess_shader, wnd_size)
        self.shake_time = 0.0
        self.power_duration = 0.0

        # init text processor
        text_shader = ResourceManger.get_shader('text')
        text_shader['projection'].write(projection.astype('f4'))
        self.text_renderer = TextRenderer(self.ctx, text_shader)
        self.text_renderer.load("OCRAEXT.TTF", 24)

        # init background object
        self.background = GameObject((0, 0), (self.width, self.height))
        self.background.texture = ResourceManger.get_texture('background')

        # init paddle object
        paddle_pos = [self.width/2-paddle_size[0]/2, self.height-paddle_size[1]]
        self.paddle = GameObject(paddle_pos, paddle_size)
        self.paddle.texture = ResourceManger.get_texture('paddle')

        # init levels
        self.levels = [GameLevel() for i in range(4)]
        self.levels[0].load_data('one.lvl', self.width, self.height/2)
        self.levels[1].load_data('two.lvl', self.width, self.height/2)
        self.levels[2].load_data('three.lvl', self.width, self.height/2)
        self.levels[3].load_data('four.lvl', self.width, self.height/2)
        self.level = 0

        # init ball
        ball_pos = [paddle_pos[0] + paddle_size[0]/2 - ball_radius, 
                    paddle_pos[1] - ball_radius*2]
        self.ball = BallObject(ball_pos, ball_radius, ball_color, ball_init_velocity)
        self.ball.texture = ResourceManger.get_texture('ball')

        # play background music
        audio = ResourceManger.get_audio('breakout')
        self.audioPlayer = audio.play()
        self.audioPlayer.loop = True
        self.audioPlayer.volume = 0.5
        
    def render(self, time: float):
        # off-screen rendering
        self.post_processor.beginRender()

        # draw background
        self.background_renderer.draw()

        # draw particles
        if not self.ball.stuck:
            self.particle_generator.draw()

        # draw scene (paddle, ball and blocks)
        self.sprite_renderer.draw()

        # render scene to screen as a texture
        self.post_processor.endRender()
        self.post_processor.render(time)

        # render texts
        self.text_renderer.render()
        
    def process_motion_event(self, wnd: BaseWindow, dt):
        if self.state == GameState.kGameActive:
            velocity = paddle_velocity * dt
            if wnd.is_key_pressed(wnd.keys.A):
                paddle_pos_x = self.paddle.position[0]
                self.paddle.position[0] -= velocity
                if self.paddle.position[0] < 0:
                    self.paddle.position[0] = 0
                if self.ball.stuck is True:
                    self.ball.position[0] += (self.paddle.position[0]-paddle_pos_x)
            if wnd.is_key_pressed(wnd.keys.D):
                paddle_pos_x = self.paddle.position[0]
                self.paddle.position[0] += velocity
                if self.paddle.position[0] > self.width-self.paddle.size[0]:
                    self.paddle.position[0] = self.width-self.paddle.size[0]
                if self.ball.stuck is True:
                    self.ball.position[0] += (self.paddle.position[0]-paddle_pos_x)
    
    def process_key_event(self, wnd: BaseWindow, key, action):
        if action == wnd.keys.ACTION_RELEASE:
            if key == wnd.keys.M:
                if self.audioPlayer.playing is True:
                    self.audioPlayer.pause()  #pause music
                else:
                    self.audioPlayer.play()   #resume music
            elif self.state == GameState.kGameMenu:
                if key == wnd.keys.ENTER:
                    self.state = GameState.kGameActive
                    self.life = max_life
                elif key==wnd.keys.W or key==wnd.keys.UP:
                    self.level = (self.level+1) % len(self.levels)
                elif key==wnd.keys.S or key==wnd.keys.DOWN:
                    self.level = self.level-1 if self.level>0 else len(self.levels)-1
            elif self.state == GameState.kGameActive:
                if key == wnd.keys.SPACE:
                    self.ball.stuck = False
                elif key == wnd.keys.P:
                    self.state = GameState.kGamePause
            elif self.state == GameState.kGamePause:
                if key == wnd.keys.ENTER:
                    self.state = GameState.kGameActive
            elif self.state == GameState.kGameWin:
                if key == wnd.keys.ENTER:
                    self.state = GameState.kGameActive
                    
    def update(self, dt):
        # pause game
        if self.state == GameState.kGamePause:
            self.updateText()
            return
        
        # move ball
        self.ball.move(dt, self.width)

        if not self.ball.stuck:
            self.doCollisions() # collision detection
            self.particle_generator.update(dt, self.ball, ball_radius/2.0) #update particles
        
        # shaking
        if self.shake_time > 0.0:
            self.shake_time -= dt
            if self.shake_time <= 0.0:
                self.post_processor.shake = False
        
        # update powerup
        if self.power_duration > 0.0:
            self.power_duration -= dt
            if self.power_duration <= 0.0:
                self.resetPowerups()

        # pass or lose
        if self.ball.position[1] >= self.height: #lose
            self.life -= 1
            if self.life == 0:
                self.levels[self.level].reset()
                self.state = GameState.kGameMenu
            self.resetPowerups()
            self.resetPlayer()
        elif self.levels[self.level].is_complete() is True: #pass level
            self.levels[self.level].reset()
            self.level = (self.level+1) % len(self.levels)
            self.state = GameState.kGameWin
            self.resetPowerups()
            self.resetPlayer()
        
        # update scene objects
        self.updateScene()
        
        # update text
        self.updateText()
    
    def doCollisions(self):
        self.collision_with_bricks()
        self.collision_with_paddle()

    def collision_with_paddle(self):
        clash = Collision.ball_box_check(self.ball, self.paddle)
        if clash.is_clash is True:
            # check hit point
            halfSize = self.paddle.size[0] / 2.0
            centerBoard = self.paddle.position[0] + halfSize
            centerBall = self.ball.position[0] + self.ball.radius
            ratio = (centerBall-centerBoard) / halfSize

            # update velocity
            velocity_len = numpy.linalg.norm(self.ball.velocity)
            self.ball.velocity[0] = ball_init_velocity[0] * ratio * 2.0
            self.ball.velocity[1] = -self.ball.velocity[1]
            velocity_new_len = numpy.linalg.norm(self.ball.velocity)
            self.ball.velocity[0] = velocity_len*self.ball.velocity[0]/velocity_new_len
            self.ball.velocity[1] = velocity_len*self.ball.velocity[1]/velocity_new_len

            # move ball to avoid sticky
            self.ball.position[1] -= clash.penetration
    
    def collision_with_bricks(self):
        bricks = self._check_bricks_in_grid()
        self._collision_with_bricks(bricks)

    # check surrounding four bricks
    def _check_bricks_in_grid(self):
        bricks = []
        grid = self.levels[self.level].grid
        unitWidth = self.levels[self.level].unitWidth
        unitHeight = self.levels[self.level].unitHeight
        grid_x = self.ball.position[0]//unitWidth
        grid_y = self.ball.position[1]//unitHeight

        if (grid_x, grid_y) in grid:  # top left
            bricks.append(grid[(grid_x, grid_y)])
        if (grid_x+1, grid_y) in grid: # top right
            bricks.append(grid[(grid_x+1, grid_y)])
        if (grid_x+1, grid_y+1) in grid: # bottom right
            bricks.append(grid[(grid_x+1, grid_y+1)])
        if (grid_x, grid_y+1) in grid: # bottom left
            bricks.append(grid[(grid_x, grid_y+1)])
        return bricks  

    def _collision_with_bricks(self, bricks):
        for brick in bricks:
            if brick.destroyed is True:
                continue

            clash = Collision.ball_box_check(self.ball, brick)
            if not clash.is_clash:
                continue

            self.showPowerup(brick)

            if (self.ball.pass_through is True) and (brick.is_solid is False):
                continue
                   
            # 1.set rebound direction
            # 2.move ball out of box
            if clash.direction==Direction.LEFT or clash.direction==Direction.RIGHT:
                self.ball.velocity[0] = -self.ball.velocity[0]
                if clash.direction == Direction.LEFT:
                    self.ball.position[0] += clash.penetration
                else:
                    self.ball.position[0] -= clash.penetration
            else:
                self.ball.velocity[1] = -self.ball.velocity[1]
                if clash.direction == Direction.UP:
                    self.ball.position[1] += clash.penetration
                else:
                    self.ball.position[1] -= clash.penetration

    def showPowerup(self, brick):
        if brick.is_solid:
            self.shake_time = shake_time
            self.post_processor.shake = True
            ResourceManger.get_audio('solid').play()
        else:
            brick.destroyed = True
            if not brick.powerup:
                ResourceManger.get_audio('non-solid').play()
            else:
                ResourceManger.get_audio('powerup').play()   
                if brick.powerup == "confuse":
                    self.power_duration = powerup_duration
                    self.post_processor.confuse = True
                    self.post_processor.chaos = False
                elif brick.powerup == "chaos":
                    self.power_duration = powerup_duration
                    self.post_processor.chaos = True
                    self.post_processor.confuse = False
                elif brick.powerup == "speed":
                    self.power_duration = powerup_duration
                    self.ball.speed_up = powerup_speed
                elif brick.powerup == "pad-resize":
                    self.power_duration = powerup_duration
                    self.paddle.resize(50)
                elif brick.powerup == "pass-through":
                    self.power_duration = powerup_duration/2
                    self.ball.pass_through = True
    
    def updateScene(self):
        self.sprite_renderer.resetBuffer()
        self.sprite_renderer.updateBuffer([self.paddle], 0)
        self.sprite_renderer.updateBuffer([self.ball], 1)

        solid_blocks = []
        blocks = []
        for brick in self.levels[self.level].bricks:
            if not brick.destroyed:
                if brick.is_solid is True:
                    solid_blocks.append(brick)
                else:
                    blocks.append(brick)
        
        self.sprite_renderer.updateBuffer(blocks, 2)
        self.sprite_renderer.updateBuffer(solid_blocks, 3)
    
    def updateText(self):
        texts = []
        texts.append(TextContent(f"Lives:{self.life}", 5, 20))
        texts.append(TextContent(f"Level:{self.level+1}", self.width-110, 20))

        if self.state == GameState.kGameMenu:
            texts.append(TextContent("Press ENTER to start", 250, self.height/2))
            texts.append(TextContent("Press W or S to select level", 245, self.height/2 + 20, 0.75))
        elif self.state == GameState.kGameWin:
            texts.append(TextContent("You WIN !!!", 320, self.height/2, 1.0, (0.0, 1.0, 0.0)))
            texts.append(TextContent("Press ENTER to continue", 240, self.height/2+20, 0.9, (1.0, 1.0, 0.0)))
        elif self.state == GameState.kGamePause:
            texts.append(TextContent("Game paused !", 300, self.height/2, 1.0, (0.0, 1.0, 0.0)))
            texts.append(TextContent("Press ENTER to continue", 240, self.height/2+20, 0.9, (1.0, 1.0, 0.0)))      
        self.text_renderer.updateBuffers(texts)

    def resetPlayer(self):
        paddle_pos = [self.width/2-paddle_size[0]/2, self.height-paddle_size[1]]
        self.paddle.reset(paddle_pos, (1.0, 1.0, 1.0), paddle_size)
        ball_pos = [paddle_pos[0] + paddle_size[0]/2 - ball_radius, 
                    paddle_pos[1] - ball_radius*2]
        self.ball.reset(ball_pos, ball_color, ball_init_velocity)
        self.particle_generator.reset()
    
    def resetPowerups(self):
        self.post_processor.confuse = False
        self.post_processor.chaos = False
        self.ball.pass_through = False
        self.ball.speed_up = 1.0
        self.paddle.resize(0)