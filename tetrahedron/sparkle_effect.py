from time import sleep, time
from random import random, randint
import palette
import effect
from math import fmod


class SparkleEffect(effect.Effect):

    def __init__(self, led_art, name):
        effect.Effect.__init__(self, led_art, name)
        self.FADE_CONSTANT = .65
        self.PASSES = 35
        self.DOTS = 10
        
        self.pss = 0
        self.palette = []
        self.next_update = 0
        self.update_interval = .7


    def setup(self, num_leds):
        self.passes = 0
        self.dots = 0
        self.num_leds = num_leds
        self.init_clear = False


    def set_color(self, color):
        pass


    @staticmethod
    def create_analogous_palette():
        r = random()
        s = random() / 14.0
        return (palette.make_hsv(r),
                palette.make_hsv(fmod(r - s + 1.0, 1.0)),
                palette.make_hsv(fmod(r - (s * 2) + 1.0, 1.0)),
                palette.make_hsv(fmod(r + s, 1.0)),
                palette.make_hsv(fmod(r + (s * 2), 1.0)))


    def loop(self):

        if not self.init_clear:
            self.init_clear = True
            self.led_art.clear()
            sleep(.2)

        if self.pss == 0:
            self.palette = SparkleEffect.create_analogous_palette()

        if self.next_update < time():
            self.next_update = time() + self.update_interval

            for dot in range(self.DOTS):
                for strip in range(self.led_art.NUM_STRIPS):
                    self.led_art.set_led_color(1 << strip, randint(0, self.num_leds-1), self.palette[randint(0, len(self.palette)-1)])

            self.led_art.show()

            for strip in range(self.led_art.NUM_STRIPS):
                for led in range(self.num_leds):
                    color = list(self.led_art.get_led_color(strip, led))
                    for j in range(3):
                        color[j] = int(float(color[j]) * self.FADE_CONSTANT)
                    self.led_art.set_led_color(1 << strip, led, (color[0], color[1], color[2]))

            self.pss = (self.pss + 1) % self.PASSES  
