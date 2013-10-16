import pyglet
from pyglet.window import key
import datetime
import os
import random


class Counter(object):

    DURATION = datetime.timedelta(seconds=5*60+1)

    def __init__(self):
        self.song = pyglet.media.load('fadeout.wav', streaming=False)
        self.player = pyglet.media.Player()
        self.player.queue(self.song)
        self.remaining = None
        self.reset()

    def reset(self):
        self.started = datetime.datetime.now()
        self.stopped = False

        # self.monster = None
        self.player.pause()     

    def silence(self):
        self.player.pause()       

    def check(self):
        if self.stopped:
            return
        completed = datetime.datetime.now() - self.started
        remaining = self.DURATION - completed
        self.remaining = max(remaining, datetime.timedelta(seconds=0)).seconds
        if not self.remaining:
            choices = os.listdir('images')
            img = pyglet.image.load('images/%s' % random.choice(choices))
            self.monster = pyglet.sprite.Sprite(img)
            scale_x = window.width / float(img.width)
            scale_y = window.height / float(img.height)
            self.monster.scale = max([scale_x, scale_y])
            self.monster.set_position(
                x=(window.width-self.monster.width)/2,
                y=(window.height-self.monster.height)/2)
            self.player.play()
            self.stopped = True

window = pyglet.window.Window(fullscreen=True)
label = pyglet.text.Label('0:00',
                          font_name='CookieMonster',
                          font_size=500, color=(0,0,0,255),
                          x=-150, y=250)

@window.event
def on_key_press(symbol, modifiers):
    global counter
    if symbol == key.Q:
        pyglet.app.exit()
    if symbol == key.R:
        counter.reset()
    if symbol == key.SPACE:
        counter.silence()


@window.event
def on_draw():
    window.clear()

    # Background color
    color = (255, 255, 255)
    if counter.remaining < 60:
        color = (255, 255, 0)
    if counter.remaining < 30:
        color = (255, 0, 0)
    pyglet.graphics.draw_indexed(4, pyglet.gl.GL_TRIANGLES,
        [0, 1, 2, 0, 2, 3],
        ('v2i', (0, 0,
                 window.width, 0,
                 window.width, window.height,
                 0, window.height)),
         ('c3B', color*4)
    )

    if not counter.stopped:
        label.draw()
    else:
        counter.monster.draw()

def update(dt):
    counter.check()
    minutes = counter.remaining / 60
    seconds = counter.remaining % 60 
    label.text = '%2i:%02i' % (minutes, seconds)

pyglet.clock.schedule_interval(update, 0.1)

counter = Counter()
pyglet.app.run()
