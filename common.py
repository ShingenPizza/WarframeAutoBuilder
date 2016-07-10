# -*- coding: utf-8 -*-

class OverMaxRank(Exception):
    def __str__(self):
        return 'rank higher than max'

    def __unicode__(self):
        return u'rank higher than max'

    def __repr__(self):
        return repr('rank higher than max')

weapon_type_dependencies = {
    'ASS_RIFLE': ['RIFLE'],
    'BOW': ['RIFLE'],
    'SNIPER': ['RIFLE'],
    'LAUNCHER': ['ASS_RIFLE'],
}

stat_dependencies = {
    'burst_dps': ['avg_dmg', 'fire_rate', 'atk_spd'],
    'reload_dps': ['burst_dps', 'mag_size', 'reload'],
    'avg_dmg': ['sum_dmg', 'crit_chance', 'crit_mult'],
    'crit_dmg': ['avg_dmg'],
    'base_dmg': ['avg_dmg'],
    'sum_dmg': ['phys_dmg', 'elem_dmg'],
    'phys_dmg': ['dmg', 'impact', 'punct', 'slash'],
    'elem_dmg': ['dmg', 'heat', 'cold', 'electr', 'toxin'],
    'dmg': ['damage', 'multishot'],
    'stat_chance': ['multishot']
}

def get_list_from_dict(name, dictionary):
    result = []
    awaiting = [name]
    while awaiting:
        tmp = []
        for aw_name in awaiting:
            if aw_name in result:
                continue
            result.append(aw_name)
            if aw_name not in dictionary:
                continue
            tmp += dictionary[aw_name]
        awaiting = tmp
    return result

def sum_dmg(stats):
    dmg = 0
    for elem in ('impact', 'punct', 'slash', 'heat', 'cold', 'electr', 'toxin', 'gas', 'magnetic', 'corrosive', 'blast', 'rad', 'viral'):
        if elem in stats:
            dmg += stats[elem]
    return dmg

stat_names = {
    'accuracy': 'Accuracy',
    'crit_chance': 'Crit chance',
    'crit_mult': 'Crit multiplier',
    'fire_rate': 'Fire rate',
    'mag_size': 'Magazine',
    'reload': 'Reload',
    'stat_chance': 'Status',

    'atk_spd': 'Attack speed',

    'impact': 'Impact',
    'punct': 'Punct',
    'slash': 'Slash',
    'phys_dmg': 'Physical dmg',
    'heat': 'Heat',
    'cold': 'Cold',
    'electr': 'Electricity',
    'toxin': 'Toxin',
    'corrosive': 'Corrosive',
    'blast': 'Blast',
    'gas': 'Gas',
    'magnetic': 'Magnetic',
    'rad': 'Radiation',
    'viral': 'Viral',
    'elem': 'Elemental',
    'elem_dmg': 'Elemental dmg',

    'drain_sum_max': 'Base drain',
    'drain_sum_min': 'Min drain',
    'drain_sum_effective': 'Effective drain',
    'sum_dmg': 'Sum dmg/shot',
    'base_dmg': 'Base dmg/shot',
    'crit_dmg': 'Crit dmg/shot',
    'avg_dmg': 'Average dmg/shot',
    'burst_dps': 'Burst DPS',
    'reload_dps': 'Reload DPS',
}

max_label_length = max(len(stat_names[n]) for n in stat_names)

stat_order = ('accuracy', 'atk_spd', 'crit_chance', 'crit_mult', 'fire_rate', 'mag_size', 'reload', 'stat_chance',
              'impact', 'punct', 'slash', 'phys_dmg', 'heat', 'cold', 'electr', 'toxin', 'gas', 'magnetic', 'corrosive', 'blast', 'rad', 'viral', 'elem_dmg',
              'drain_sum_max', 'drain_sum_min', 'drain_sum_effective', 'sum_dmg', 'base_dmg', 'crit_dmg', 'avg_dmg', 'burst_dps', 'reload_dps')

def pretty_print_stats(data):
    stats = data['stats']
    base_stats = data['base_stats']
    for stat in stat_order:
        if stat not in stats or stats[stat] == 0:
            continue
        if stat == 'base_dmg' and stats['base_dmg'] == stats['sum_dmg']:
            continue
        stat_name = stat_names[stat] if stat in stat_names else stat
        if stat in ('crit_chance', 'stat_chance'):
            print '%-*s %.2f%%%s' % (max_label_length, stat_name, stats[stat] * 100, ' (%.1f%%)' % (stats[stat] / base_stats[stat] * 100) if stat in base_stats else '')
        elif isinstance(stats[stat], float):
            print '%-*s %.2f%s' % (max_label_length, stat_name, stats[stat], ' (%.1f%%)' % (stats[stat] / base_stats[stat] * 100) if stat in base_stats else '')
        else:
            print '%-*s %d%s' % (max_label_length, stat_name, stats[stat], ' (%.1f%%)' % (stats[stat] / base_stats[stat] * 100) if stat in base_stats else '')

def save_results(data, base_stats, weapon, personal, primed, corrupted, factions, sortby):
    fout = file('results/%s %s %s %s %s %s.txt' % (weapon.name, 'personal' if personal else 'best', 'P' if primed else 'NP', 'C' if corrupted else 'NC', 'F' if factions else 'NF', sortby), 'w')
    for res in data:
        stats = res['stats']
        mods = res['mods']
        labels = []
        values = []
        appendix = []
        for stat in stat_order:
            if stat not in stats or stats[stat] == 0:
                continue
            if stat == 'base_dmg' and stats['base_dmg'] == stats['sum_dmg']:
                continue
            labels.append('%s' % (stat_names[stat] if stat in stat_names else stat))
            if stat in ('crit_chance', 'stat_chance'):
                values.append('%.2f%%' % (stats[stat] * 100))
            elif isinstance(stats[stat], float):
                values.append('%.2f' % stats[stat])
            else:
                values.append('%d' % stats[stat])
            appendix.append(' (%.1f%%)' % (stats[stat] / base_stats[stat] * 100) if stat in base_stats else '')

        max_value_length = max(len(v) for v in values)
        lines = ['%s | %s | %s | %s | sorted by %s' % (weapon.name, 'personal' if personal else 'best', 'primed' if primed else 'no primed', 'factions' if factions else 'no factions', sortby)]
        for l, v, a in zip(labels, values, appendix):
            lines.append('%-*s %-*s%s' % (max_label_length, l, max_value_length, v, a))
        lines.append('used mods: %s' % str(mods))
        lines.append('')

        for line in lines:
            print line
        fout.writelines(['%s\n' % line for line in lines])
    fout.close()

def effective_drain(mods, weap_pols):
    if not weap_pols:
        return sum(mod.drain for mod in mods)
    aaa = {}
    weap_pols = list(weap_pols)
    for mod in mods:
        if mod.polarity not in aaa:
            aaa[mod.polarity] = []
        aaa[mod.polarity].append(mod.drain)
    for pol in aaa:
        aaa[pol].sort(reverse=True)
    used = []
    sum_drain = 0
    for pol in weap_pols:
        if pol in aaa and aaa[pol]:
            drain = aaa[pol].pop(0)
            sum_drain += int(round(drain / 2.0))
            used.append(pol)

    # for pol in used:
    #     weap_pols.remove(pol)

    for pol in aaa:
        for drain in aaa[pol]:
            sum_drain += drain

    # TODO wrong polarity -> more drain
    return sum_drain
