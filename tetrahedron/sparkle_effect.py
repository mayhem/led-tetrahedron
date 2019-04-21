from time import sleep
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


    def setup(self, num_leds):
        self.passes = 0
        self.dots = 0
        self.num_leds = num_leds


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

        pal = SparkleEffect.create_analogous_palette()
        for pss in range(self.PASSES):
            for dot in range(self.DOTS):
                for strip in range(self.led_art.NUM_STRIPS):
                    self.led_art.set_led_color(1 << strip, randint(0, self.num_leds-1), pal[randint(0, len(pal)-1)])

            self.led_art.show()
            for s in range(10):
                sleep(.05)

            for strip in range(self.led_art.NUM_STRIPS):
                for led in range(self.num_leds):
                    color = list(self.led_art.get_led_color(strip, led))
                    for j in range(3):
                        color[j] = int(float(color[j]) * self.FADE_CONSTANT)
                    self.led_art.set_led_color(1 << strip, led, (color[0], color[1], color[2]))
