# -*- coding: utf-8 -*-

from math import pow, floor
from items_main import Item

class Weapon(Item):
    base_dmg = None
    trigger = None

    def sum_dmg(self):
        self.base_dmg = 0
        for name in ('impact', 'punct', 'slash', 'heat', 'cold', 'electr', 'toxin', 'gas', 'magnetic', 'corrosive', 'blast', 'rad', 'viral'):
            self.base_dmg += self.s[name] if name in self.s else 0

    @staticmethod
    def get_proper_fire_rate(val):
        return val

    def _stage1(self, mods, bonuses):
        for mod in mods:
            for name in mod.s:
                if name not in bonuses:
                    bonuses[name] = 0
                if name == 'fire_rate' and mod.bow2xfr:
                    bonuses['fire_rate'] += self.get_proper_fire_rate(mod.s['fire_rate'])
                else:
                    bonuses[name] += mod.s[name]

    def _stage2(self, mods, stats):
        stats['drain_sum_max'] = sum(mod.drain for mod in mods)
        stats['drain_sum_min'] = sum(mod.min_drain for mod in mods)
        # stats['drain_sum_effective'] = effective_drain(mods, self.polarities)

    def _stage3(self, stats, bonuses, base_dmg):
        # FIXME HOW THE FUCK DOES SERRATION WORK
        for name in ('impact', 'punct', 'slash'):
            if name in stats:
                stats[name] *= 1 + bonuses['damage'] + (bonuses[name] if name in bonuses else 0)

        for name in ('heat', 'cold', 'electr', 'toxin', 'gas', 'magnetic', 'corrosive', 'blast', 'rad', 'viral'):
            if name not in stats:
                if name not in bonuses:
                    continue
                stats[name] = 0
            stats[name] = (1 + bonuses['damage']) * (stats[name] + base_dmg * (bonuses[name] if name in bonuses else 0))

    def _stage4(self, stats, bonuses):
        if 'multishot' in bonuses:
            for name in ('impact', 'punct', 'slash', 'heat', 'cold', 'electr', 'toxin', 'gas', 'magnetic', 'corrosive', 'blast', 'rad', 'viral'):
                if name in stats:
                    stats[name] *= 1 + bonuses['multishot']

        if 'damage_faction' in bonuses:
            for name in ('impact', 'punct', 'slash', 'heat', 'cold', 'electr', 'toxin', 'gas', 'magnetic', 'corrosive', 'blast', 'rad', 'viral'):
                if name in stats:
                    stats[name] *= 1 + bonuses['damage_faction']

        for name in ('crit_chance', 'crit_mult', 'stat_chance', 'fire_rate', 'atk_spd', 'mag_size'):
            if name in stats and name in bonuses:
                stats[name] *= 1 + bonuses[name]

        if 'mag_size' in stats:
            stats['mag_size'] = int(round(stats['mag_size']))

    def _stage5(self, stats, bonuses):
        if stats['stat_chance'] > 1.0:
            stats['stat_chance'] = 1.0
        elif 'multishot' in bonuses:
            stats['stat_chance'] = 1 - pow(1 - stats['stat_chance'], 1 + bonuses['multishot'])
            if stats['stat_chance'] > 1.0:
                stats['stat_chance'] = 1.0

        if 'reload' in stats and 'reload' in bonuses:
            stats['reload'] /= (1 + bonuses['reload'])

        # TODO accuracy, ammo, noise, pellet number

    def _stage6(self, stats, limit_fr_of_non_auto):
        stats['phys_dmg'] = 0
        for name in ('impact', 'punct', 'slash'):
            if name in stats:
                stats['phys_dmg'] += stats[name]
        stats['elem_dmg'] = 0
        for name in ('heat', 'cold', 'electr', 'toxin', 'gas', 'magnetic', 'corrosive', 'blast', 'rad', 'viral'):
            if name in stats:
                stats['elem_dmg'] += stats[name]
        stats['sum_dmg'] = dmg = stats['phys_dmg'] + stats['elem_dmg']

        if stats['crit_chance'] <= 1:
            stats['base_dmg'] = dmg
            stats['crit_dmg'] = dmg * stats['crit_mult']
            stats['avg_dmg'] = dmg * ((1 - stats['crit_chance']) + stats['crit_mult'] * stats['crit_chance'])
        else:  # red crits
            crit_lvl = floor(stats['crit_chance'])
            tmp_chance = stats['crit_chance'] - crit_lvl
            crit_mult1 = (crit_lvl * stats['crit_mult']) - (crit_lvl - 1)
            crit_mult2 = ((crit_lvl + 1) * stats['crit_mult']) - crit_lvl
            stats['base_dmg'] = dmg * crit_mult1
            stats['crit_dmg'] = dmg * crit_mult2
            stats['avg_dmg'] = dmg * (crit_mult1 * (1 - tmp_chance) + crit_mult2 * tmp_chance)

        if 'fire_rate' in stats:
            if self.trigger in ('SEMI', 'CHARGE', 'BURST') and limit_fr_of_non_auto is not None and stats['fire_rate'] > limit_fr_of_non_auto:
                stats['burst_dps'] = stats['avg_dmg'] * limit_fr_of_non_auto
                mag_empty_time = stats['mag_size'] / limit_fr_of_non_auto
                stats['reload_dps'] = (stats['avg_dmg'] * stats['mag_size']) / (mag_empty_time + stats['reload'])
            else:
                stats['burst_dps'] = stats['avg_dmg'] * stats['fire_rate']
                mag_empty_time = stats['mag_size'] / stats['fire_rate']
                stats['reload_dps'] = (stats['avg_dmg'] * stats['mag_size']) / (mag_empty_time + stats['reload'])

        elif 'atk_spd' in stats:
            stats['reload_dps'] = stats['burst_dps'] = stats['avg_dmg'] * stats['atk_spd']

    def mod_with(self, mods, limit_fr_of_non_auto):
        bonuses = {'damage': 0}

        base_dmg = self.base_dmg
        stats = self.s.copy()

        self._stage1(mods, bonuses)
        self._stage2(mods, stats)
        self._stage3(stats, bonuses, base_dmg)
        self._stage4(stats, bonuses)
        self._stage5(stats, bonuses)
        self._stage6(stats, limit_fr_of_non_auto)

        return stats

class Rifle(Weapon):
    pass

class AssaultRifle(Rifle):
    pass

class Bow(Rifle):

    @staticmethod
    def get_proper_fire_rate(val):
        return 2 * val

class SniperRifle(Rifle):
    pass

class Shotgun(Weapon):
    pass

class Pistol(Weapon):
    pass

class Melee(Weapon):
    pass
