from time import sleep, time
from random import random, randint
import palette
import effect
from math import fmod
from colorsys import hsv_to_rgb


class RainbowEffect(effect.Effect):

    def __init__(self, led_art, name):
        effect.Effect.__init__(self, led_art, name)
        
        self.hue = random()
        self.next_update = 0
        self.update_interval = .1
        self.hue_increment = .01


    def setup(self, num_leds):
        self.num_leds = num_leds


    def set_color(self, color):
        pass


    def loop(self):

        if self.next_update < time():
            self.next_update = time() + self.update_interval

            self.led_art.set_color(0xff, palette.make_hsv(self.hue, 1.0, 1.0))
            self.led_art.show()

            self.hue += self.hue_increment 
