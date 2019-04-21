from math import pi, sin
from colorsys import hsv_to_rgb, rgb_to_hsv, rgb_to_hsv


import gradient
import palette
import effect


class UndulatingEffect(effect.Effect):

    def __init__(self, led_art, name):
        effect.Effect.__init__(self, led_art, name)
        self.colors = [(255, 0, 128), (255, 128, 0)]


    def setup(self, num_leds):
        self.color_index = 0
        self.uoap_index = 0
        self.uaop_steps = 50
        self.uoap_increment = 1.0 / self.uaop_steps 
        self.num_leds = num_leds 


    def set_color(self, color):
        if color in self.colors:
            return

        self.colors[self.color_index] = color
        self.color_index = (self.color_index + 1) % 2


    def loop(self):
        t = self.uoap_index * 2 * pi
        jitter = sin(t) / 4
        p = [ (0.0, self.colors[0]), 
              (0.45 + jitter, self.colors[1]),
              (0.65 + jitter, self.colors[1]),
              (1.0, self.colors[0])
        ]
        g = gradient.Gradient(self.num_leds, p)
        g.render(self.led_art, 1 | 2 | 4)

        p = [ (0.0, self.colors[0]), 
              (0.65 - jitter, self.colors[1]),
              (0.45 - jitter, self.colors[1]),
              (1.0, self.colors[0])
        ]
        g = gradient.Gradient(self.num_leds, p)
        g.render(self.led_art, 8 | 16 | 32)

        self.led_art.show()

        self.uoap_index += self.uoap_increment
        if self.uoap_index > 1.0:
            self.uoap_index = 0.0
