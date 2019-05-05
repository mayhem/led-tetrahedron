import math
from random import random, randint, seed
from math import fmod, sin, pi
from time import sleep, time
from colorsys import hsv_to_rgb, rgb_to_hsv, rgb_to_hsv
import undulating_effect

import gradient
import palette
import effect

MAPPING = [ 0, 1, 2, 3, 4, 5 ]

def parametric(value):
    return fmod(value + 1.0, 1.0)


class OppositesEffect(effect.Effect):

    def __init__(self, led_art, name):
        effect.Effect.__init__(self, led_art, name)
        self.points = []
        self.render_increment = .01
        self.hue = random()
        self.jitter = .05


    def setup(self, num_leds):
        self.num_leds = num_leds
        self.palettes = [
            list(palette.create_complementary_palette(self.hue)),
            list(palette.create_complementary_palette(parametric(self.hue - self.jitter))),
            list(palette.create_complementary_palette(parametric(self.hue + self.jitter)))
        ]
        self.step = 1.0 / float(num_leds)
        for strip in range(6):
            pal= strip // 2
            for _point in range(self.num_leds // 3):
                point = _point * 3 
                print(point)
                self.points.append( [ float(point * self.step), self.palettes[pal][ point % 2 ] ] )

        for p in self.points:
            print(p)

    def set_color(self, color):
        pass


    def loop(self):

        try:
            g = gradient.Gradient(self.num_leds, self.points)
            g.render(self.led_art, 0xFF) 
            self.led_art.show()
        except ValueError as err:
            pass

        # Move all the points down a smidge
        for i in range(len(self.palette)):
            self.palette[i] = [ self.palette[i][0] + self.render_increment, self.palette[i][1] ]

        # Has my closest point gone over 0.0? Time to insert a new point!
        if self.palette[0][0] > 0.0:
            self.palette.insert(0, [ self.palette[0][0] - self.point_distance, self.source[self.source_index]])
            self.source_index = (self.source_index + 1) % len(self.source)
        
            if not self.source:
                self.source = list(palette.create_random_palette())

            # clean up the point(s) that went out the other end
            try:
                while self.palette[-2][0] > 1.0:
                    self.palette.pop()
            except IndexError:
                pass

            if self.num_new_points == 10:
                self.source = list(palette.create_random_palette())
                self.source_index = 0
                self.num_new_points = 0

            self.num_new_points += 1

        sleep(.03)
