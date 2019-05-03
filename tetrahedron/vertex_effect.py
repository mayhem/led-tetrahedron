import math
from random import random, randint, seed
from math import fmod, sin, pi
from time import sleep, time
from colorsys import hsv_to_rgb, rgb_to_hsv, rgb_to_hsv
import undulating_effect

import gradient
import palette
import effect

"""
Vertexes: 

0 - top
1 - tree 0
2 - tree 1 (tree + 1 clockwise)
3 - tree 2 (tree + 2 clockwise)

Segemnets:

0 - top -> tree 0
1 - top -> tree 1
2 - top -> tree 2
3 - tree 0 -> tree 1
4 - tree 1 -> tree 2
5 - tree 3 -> tree 0

"""
         


class VertexEffect(effect.Effect):

    def __init__(self, led_art, name):
        effect.Effect.__init__(self, led_art, name)
        self.palettes = []
        self.point_distance = .25
        self.hue = random()
        self.hue_increment = .01


    def setup(self, num_leds):
        self.num_leds = num_leds


    def set_color(self, color):
        pass


    def make_palettes(self, hues):
        ''' pass in 4 hues in vertex order '''

        palettes = [
            [ 0.0, hues[0], 1.0, hues[1] ],
            [ 0.0, hues[0], 1.0, hues[2] ],
            [ 0.0, hues[0], 1.0, hues[3] ],
            [ 0.0, hues[1], 1.0, hues[2] ],
            [ 0.0, hues[2], 1.0, hues[3] ],
            [ 0.0, hues[3], 1.0, hues[1] ],
        ]


    def create_analogous_palette(self, hue):
        s = random() / 14.0
        return (palette.make_hsv(hue),
                palette.make_hsv(fmod(hue - s + 1.0, 1.0)),
                palette.make_hsv(fmod(hue - (s * 2) + 1.0, 1.0)),
                palette.make_hsv(fmod(hue + s, 1.0)))


    def loop(self):

        hues = self.create_analogous_palette(self.hue)  
        palettes = self.make_palettes(hues)
        for i, pal in enumerate(palettes):
            strip = 1 << i
            try:
                g = gradient.Gradient(self.num_leds, pal)
                g.render(self.led_art, i) 
                self.led_art.show()
            except ValueError as err:
                pass

        self.hue += hue_increment
        sleep(.2)
