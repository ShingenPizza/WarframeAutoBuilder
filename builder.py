# -*- coding: utf-8 -*-

from datetime import datetime
from itertools import combinations, product

from common import pretty_print_stats, save_results, effective_drain, weapon_type_dependencies, get_list_from_dict
from csv_readers import get_item, get_mods, get_incompatible

def calculate(sett):
    wep_type = sett['weapon']
    use_personal = sett['use_personal']
    use_primed = sett['use_primed']
    use_corrupted = sett['use_corrupted']
    use_faction = sett['use_faction']
    sortby = sett['sortby']
    num_of_top_results = sett['num_of_top_results']
    point_limit = sett['point_limit']

    builder_start = datetime.now()
    wep = get_item(wep_type)
    mod_types = get_list_from_dict(wep.type, weapon_type_dependencies)

    pers_mods = {}
    if use_personal:
        personal_mods = sett['personal_mods']
        for m_t in mod_types:
            if m_t not in personal_mods:
                continue
            pers_mods.update(personal_mods[m_t])
        mods_data = get_mods({'name': [name for name in pers_mods]})
    else:
        mods_data = get_mods({'type': mod_types})

    mods_data = dict((name, mod) for name, mod in mods_data.iteritems() if (use_primed or not mod.primed) and (use_corrupted or not mod.corrupted) and (use_faction or not mod.faction))

    if sett['use_mods_smart']:
        from common import stat_dependencies
        wanted_stats = get_list_from_dict(sortby, stat_dependencies)
        mods_data = dict((name, mod) for name, mod in mods_data.iteritems() if set(mod.s) & set(wanted_stats))

    if use_personal:
        all_mods = dict((name, [mod.get_ranked(rank) for rank in pers_mods[name]]) for name, mod in mods_data.iteritems())
    else:
        all_mods = dict((name, [mod.get_ranked(-1)]) for name, mod in mods_data.iteritems())

    incompatible_mods = get_incompatible({'type': mod_types})

    for inc_mod in incompatible_mods:
        if inc_mod[1] not in all_mods:
            continue
        if inc_mod[0] not in all_mods:
            all_mods[inc_mod[0]] = []
        all_mods[inc_mod[0]] += all_mods[inc_mod[1]]
        del all_mods[inc_mod[1]]

    num_of_mods = range(sett['num_of_mods_min'], sett['num_of_mods_max'] + 1)

    custom_polarities = sett['custom_polarities']
    if wep_type in custom_polarities:
        weap_pols = custom_polarities[wep_type]
        wep.set_polarities(weap_pols)
    else:
        weap_pols = wep.polarities
    print 'polarities:', weap_pols
    print 'mods:', all_mods
    all_stats = []

    mod_dict = all_mods

    mod_classes = sorted(mod_cls for mod_cls in mod_dict)
    poss_mods = tuple(all_mods[name] for name in mod_classes)

    for tmp_num_of_mods in num_of_mods:
        start = datetime.now()

        all_possible = 0
        mod_sets = []
        for mod_comb in combinations(poss_mods, tmp_num_of_mods):
            for prod in product(*mod_comb):
                mod_sets.append(prod)
                all_possible += 1

        end = datetime.now()
        if point_limit is not None:
            mod_sets = [mods for mods in mod_sets if effective_drain(mods, weap_pols) <= point_limit]
        end2 = datetime.now()

        m_s_len = len(mod_sets)
        print '%d mod combinations to try: %d (out of %d, eligible: %.2f%%, took: %s, took2: %s)' % (tmp_num_of_mods, m_s_len, all_possible, 0 if all_possible == 0 else 100.0 * float(m_s_len) / all_possible, end - start, end2 - start)
        # continue
        for i, mods in enumerate(mod_sets):
            if i % 100000 == 0 and i != 0:
                print 'i:', i
                all_stats.sort(key=lambda s: -s['stats'][sortby])
                all_stats = all_stats[:num_of_top_results]
            stats = wep.mod_with(mods, sett['limit_fr_of_non_auto'])
            all_stats.append({'stats': stats, 'mods': mods, 'base_stats': wep.s})

    all_stats.sort(key=lambda s: -s['stats'][sortby])
    all_stats = all_stats[:num_of_top_results]

    save_results(all_stats, wep.s, wep, use_personal, use_primed, use_corrupted, use_faction, sortby)

    print '%s | %s | %s | %s | %s | sorted by %s | av. pt. %s' % (wep.name, 'personal' if use_personal else 'best', 'primed' if use_primed else 'no primed', 'corrupted' if use_corrupted else 'no corrupted', 'faction' if use_faction else 'no faction', sortby, point_limit)
    print '############ BEST:'
    if len(all_stats) > 0:
        pretty_print_stats(all_stats[0])
        print 'used mods:', all_stats[0]['mods']
    else:
        print 'none :('

    builder_end = datetime.now()
    print '### builder took: %s' % (builder_end - builder_start)

