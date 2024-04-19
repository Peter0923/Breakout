import moderngl as gl
import moderngl_window as glw
from moderngl_window.conf import settings
from moderngl_window.timers.clock import Timer
from resource_manager import ResourceManger
import game
import pyglet
import os

# Create Window
settings.WINDOW = {
    "class": "moderngl_window.context.pyglet.Window",
    "gl_version": (3, 3),
    "title": "Breakout",
    "size": (800, 600),
    "fullscreen": False,
    "resizable": True, 
    "vsync": True
}
window = glw.create_window_from_settings()

# OpenGL context configuration
ctx = window.ctx
ctx.enable(gl.BLEND | gl.CULL_FACE)
ctx.blend_func = ctx.SRC_ALPHA, ctx.ONE_MINUS_SRC_ALPHA

# Load OpenGL resource
resource_dir = os.path.normpath(os.path.join(__file__, '../resource'))
ResourceManger.initialize(resource_dir)
ResourceManger.load_all_resources()

# Init game state and event handler
breakout = game.Game(window.size, ctx)
window.key_event_func = lambda key, action, modifiers:(
    getattr(breakout, 'process_key_event')(window, key, action)
)

timer = Timer()
timer.start()

while not window.is_closing:
    # time, dt = timer.next_frame()
    # handle scheduling events
    dt = pyglet.clock.tick()
    pyglet.app.platform_event_loop.dispatch_posted_events()

    # process user inputs  
    breakout.process_motion_event(window, dt)
    breakout.update(dt)

    # render and dispatch Window events
    # window.clear()
    breakout.render(timer.time)
    window.swap_buffers()

timer.stop()
window.destroy()
