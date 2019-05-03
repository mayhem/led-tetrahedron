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

Segments:
3 - top -> tree 0
1 - top -> tree 1
0 - top -> tree 2
4 - tree 0 -> tree 1
5 - tree 1 -> tree 2
2 - tree 2 -> tree 0

"""

class VertexEffect(effect.Effect):

    def __init__(self, led_art, name):
        effect.Effect.__init__(self, led_art, name)
        self.palettes = []
        self.point_distance = .25
        self.hue = random()
        self.hue_increment = .005

    def setup(self, num_leds):
        self.num_leds = num_leds

    def set_color(self, color):
        pass

    def make_palettes(self, hues):
        ''' pass in 4 hues in vertex order '''

        return [                                # segment
            [ (0.0, hues[0]), (1.0, hues[3]) ], # 0
            [ (0.0, hues[0]), (1.0, hues[2]) ], # 1
            [ (0.0, hues[1]), (1.0, hues[3]) ], # 2
            [ (0.0, hues[0]), (1.0, hues[1]) ], # 3
            [ (0.0, hues[1]), (1.0, hues[2]) ], # 4
            [ (0.0, hues[2]), (1.0, hues[3]) ], # 5
        ]


    def create_analogous_palette(self, hue):
        s = random() / 2.0
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
                g.render(self.led_art, 1 << i) 
            except ValueError as err:
                pass

        self.led_art.show()

        self.hue += self.hue_increment
        sleep(5)
