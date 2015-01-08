__author__ = 'cirreth'

import logging
import time
from plugins.SHomePlugin import SHomePlugin
from libs.ledstrip import *

class LedStripPlugin(SHomePlugin):

    _ledstrip = None
    _cur_r=0
    _cur_g=0
    _cur_b=0

    def __init__(self, parameters):
        self._ledstrip = RGB()

    def call(self, reference, values={}):
        """
            #000000 set instantly
            #000000:x smoothly, interval: x (float)
        """
        logging.debug('Ledstrip plugin: '+reference)
        spl = reference.split(':')
        color = spl[0], float(spl[1]) if len(spl)==2 else 0
        try:
            self.set_color(color)
        except Exception as e:
            logging.error(e)
            self._ledstrip = RGB()
            self.set_color(color)


    def set_color(self, color: 'hex str (#000000)', interval=0):
        rn = int(color[1:3], 16)
        gn = int(color[3:5], 16)
        bn = int(color[5:], 16)
        if interval:
            dr = (rn - self._cur_r)
            dg = (gn - self._cur_g)
            db = (bn - self._cur_b)
            nsteps = max(abs(dr), abs(dg), abs(db))
            stepdur = interval/nsteps
            if stepdur<0.075:
                stepdur = 0.075
                nsteps=int(interval/0.075)
            dr /= nsteps
            dg /= nsteps
            db /= nsteps
            for i in range(0, nsteps):
                self._ledstrip.setColor(self.rgb_to_hex(self._cur_r+dr*i, self._cur_g+dg*i, self._cur_b+db*i))
                time.sleep(stepdur)
        self._cur_r = rn
        self._cur_g = gn
        self._cur_b = bn
        self._ledstrip.setColor(color)

    @staticmethod
    def rgb_to_hex(r, g, b):
        return '#'+format(int(r), '02x')+format(int(g), '02x')+format(int(b), '02x')

    def list(self, reference=''):
        return '#000000 set instantly\n#000000:0.0 set in interval 0.0'
