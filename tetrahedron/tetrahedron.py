#!/usr/bin/env python3

import abc
import sys
import socket
import json
import math
import traceback
from random import random, randint, seed
from math import fmod, sin, pi
from time import sleep, time
from colorsys import hsv_to_rgb, rgb_to_hsv, rgb_to_hsv
import opc

#import solid_effect
import sparkle_effect
import undulating_effect
#import colorcycle_effect
#import bootie_call_effect
#import strobe_effect
import test_effect


class Tetrahedron(object):

    NUM_STRIPS           = 6
    NUM_STRIPS_FC        = 8
    NUM_LED_PER_STRIP    = 60
    NUM_LED_PER_STRIP_FC = 64

    STRIP_0 = 1
    STRIP_1 = 2
    STRIP_2 = 4
    STRIP_3 = 8
    STRIP_4 = 16
    STRIP_5 = 32
    STRIP_ALL = 63

    def __init__(self):
        self.state = False
        self.brightness = 128
        self.effect_list = []
        self.current_effect = None

        self.client = opc.Client('localhost:7890')
        self.pixels = [ (0, 0, 0) ] * self.NUM_STRIPS_FC * self.NUM_LED_PER_STRIP_FC

    def set_state(self, state):
        self.state = state

    def set_color(self, strips, col):
        for led in range(self.NUM_LED_PER_STRIP):
            for strip in range(self.NUM_STRIPS):
                if strips & (1 << strip):
                    self.pixels[((strip + 2) * self.NUM_LED_PER_STRIP_FC) + led] = col  


    def set_led_color(self, strips, led, col):
        for strip in range(self.NUM_STRIPS):
            if strips & (1 << strip):
                self.pixels[((strip + 2) * self.NUM_LED_PER_STRIP_FC) + led] = col  


    def get_led_color(self, strip, led):
        ''' strip should be the strip index, not the strips bitmap '''
        return self.pixels[((strip + 2) * self.NUM_LED_PER_STRIP_FC) + led]


    def clear(self, strips=STRIP_ALL):
        self.set_color(strips, (0,0,0))
        self.show()


    def show(self):
        self.client.put_pixels(self.pixels)


    def set_brightness(self, brightness):
        self.brightness = brightness

    def set_random_effect(self):
        while True:
            next_effect = randint(0, len(self.effect_list)-1)
            if self.effect_list[next_effect] != self.current_effect:
                break

        print(next_effect)
        self.set_effect(self.effect_list[next_effect].effect_name)

    def set_effect(self, effect_name):
        for effect in self.effect_list:
            if effect.name == effect_name:
                saved_state = self.state
                self.state = False
                self.current_effect = effect 
                self.current_effect.setup(self.NUM_LED_PER_STRIP)
                self.state = saved_state
                break

    def add_effect(self, effect):
        self.effect_list.append(effect)
        if len(self.effect_list) == 1:
            self.set_effect(str(effect.name))

    def test(self):
        for i in range(self.NUM_STRIPS):
            self.set_color(1 << i, (255, 0, 0))
            self.show()
            sleep(.5)
            self.set_color(1 << i, (0, 255, 0))
            self.show()
            sleep(.5)
            self.set_color(1 << i, (0, 0, 255))
            self.show()
            sleep(.5)

        self.clear()

    def startup(self):
        colors = ( (128, 0, 128), (128, 80, 0) )
        for i in range(4):
            for j in range(self.NUM_LED_PER_STRIP):
                self.set_led_color(0xFF, j, colors[(i + j) % 2])
            self.show()
            sleep(.1)

        self.clear()

    def setup(self):
        self.startup()
        self.set_brightness(self.brightness)


    def loop(self):
        if self.current_effect and self.state:
            self.current_effect.loop()



if __name__ == "__main__":
    seed()
    a = Tetrahedron()
    a.add_effect(sparkle_effect.SparkleEffect(a, "sparkle"))
    a.add_effect(undulating_effect.UndulatingEffect(a, "undulating colors"))
    a.add_effect(test_effect.TestEffect(a, "test color cycle"))
#   a.add_effect(colorcycle_effect.ColorCycleEffect(a, "color cycle"))
#   a.add_effect(solid_effect.SolidEffect(a, "solid color"))
#   a.add_effect(bootie_call_effect.BootieCallEffect(a, "slow bootie call", .0005))
#   a.add_effect(bootie_call_effect.BootieCallEffect(a, "fast bootie call", .005))
#   a.add_effect(strobe_effect.StrobeEffect(a, "slow strobe", 2, .02))
#   a.add_effect(strobe_effect.StrobeEffect(a, "fast strobe", 8, .03))
    a.setup()
    a.set_state(True)
    try:
        while True:
            a.set_random_effect()
            timeout = time() + 5
            while timeout > time():
                a.loop()


    except KeyboardInterrupt:
        a.clear()
