#-*- coding: utf-8 -*-

from fftt_scroller.constants import MALE, FEMALE

class FFTTScroller:

    def __init__(self, base_uri):
        self.base_uri = base_uri


    def get_player_by_name(self, name, firstname=None, sex=MALE):

