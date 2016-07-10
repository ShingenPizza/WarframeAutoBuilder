# -*- coding: utf-8 -*-

class Item(object):
    name = None
    type = None
    s = None
    all_mods = []
    polarities = ()

    def set_polarities(self, pols):
        self.polarities = pols
