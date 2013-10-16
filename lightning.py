from pyglet.window import key
import glob
import pyglet
import random
import sys


class Harrassment(object):

    pause = False

    def __init__(self):
        self.song = pyglet.media.load('data/harrassment.wav', streaming=False)
        self.player = pyglet.media.Player()
        self.player.queue(self.song)

        # pre-load and scale all harrassment pictures
        self.pictures = []
        choices = []
        choices.extend(glob.glob('data/*.png'))
        choices.extend(glob.glob('data/*.jpg'))
        for choice in choices:
            img = pyglet.image.load(choice)
            sprite = pyglet.sprite.Sprite(img)
            scale_x = window.width / float(img.width)
            scale_y = window.height / float(img.height)
            sprite.scale = max([scale_x, scale_y])
            sprite.set_position(
                x=(window.width-sprite.width)/2,
                y=(window.height-sprite.height)/2)
            self.pictures.append(sprite)

    def start(self):
        self.pause = False
        self.player.play()
        self.show_picture = random.choice(self.pictures)

    def toggle_pause(self):
        self.pause = not self.pause
        if self.pause:
            self.player.pause()
        else:
            self.player.play()

    def stop(self):
        self.player.pause()

    def tick(self, dt):
        pass

    def draw(self):
        window.clear()
        self.show_picture.draw()


class Counter(object):

    pause = False

    def __init__(self, duration=10):
        self.duration = duration
        self.remaining = None

    def start(self):
        self.pause = True
        self.remaining = self.duration

    def stop(self):
        pass

    def toggle_pause(self):
        self.pause = not self.pause

    def draw(self):
        window.clear()

        # Background color
        color = (255, 255, 255)
        if self.remaining < 30:
            color = (255, 0, 0)
        elif self.remaining < 60:
            color = (255, 255, 0)
        pyglet.graphics.draw_indexed(
            4, pyglet.gl.GL_TRIANGLES,
            [0, 1, 2, 0, 2, 3],
            ('v2i', (0, 0,
                     window.width, 0,
                     window.width, window.height,
                     0, window.height)),
            ('c3B', color*4))

        pyglet.text.Label(
            '%i:%02i' % (self.remaining / 60, self.remaining % 60),
            font_name='Helvetica',
            font_size=500, color=(0, 0, 0, 255),
            x=window.width//2, y=window.height//2,
            anchor_x='center', anchor_y='center').draw()

    def tick(self, dt):
        if self.pause:
            return
        self.remaining -= dt
        if self.remaining < 0:
            switch_mode('harrassment')


# Main
def switch_mode(name):
    global mode
    if mode is not None:
        mode.stop()
    new = modes[name]
    new.start()
    mode = new

window = pyglet.window.Window(fullscreen=True)
mode = None


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.Q:
        pyglet.app.exit()
    if symbol in [key.R, key.MOTION_PREVIOUS_PAGE]:
        switch_mode('counter')
    if symbol in [key.SPACE, key.B]:
        mode.toggle_pause()

@window.event
def on_draw():
    if mode:
        mode.draw()


def tick(dt):
    if mode:
        mode.tick(dt)
pyglet.clock.schedule_interval(tick, 0.1)
modes = dict(
    counter=Counter(int(sys.argv[1])),
    harrassment=Harrassment())

switch_mode('counter')
pyglet.app.run()
