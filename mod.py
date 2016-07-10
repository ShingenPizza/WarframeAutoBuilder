# -*- coding: utf-8 -*-

from common import OverMaxRank

class Mod(object):
    name = 'default'
    rank = -1
    max_rank = -1
    drain = 0
    min_drain = 0
    polarity = None
    s = None
    primed = False
    faction = False
    bow2xfr = False
    corrupted = False

    def get_ranked(self, rank):
        if self.rank != -1:
            raise Exception('get_ranked called for a ranked mod')
        if rank > self.max_rank:
            raise OverMaxRank
        if rank == -1:
            rank = self.max_rank
        mod = Mod()
        mod.name = self.name
        mod.rank = rank
        mod.max_rank = self.max_rank
        mod.drain = self.drain + rank
        mod.min_drain = int(round(mod.drain / 2.0))
        mod.polarity = self.polarity
        mod.s = dict((k, v * (rank + 1)) for k, v in self.s.iteritems())
        mod.primed = self.primed
        mod.faction = self.faction
        mod.bow2xfr = self.bow2xfr
        mod.corrupted = self.corrupted

        return mod

    def __str__(self):
        return '%s(%d)' % (self.name, self.rank)

    def __unicode__(self):
        return u'%s(%d)' % (self.name, self.rank)

    def __repr__(self):
        return '%s(%d)' % (self.name, self.rank)
