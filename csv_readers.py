# -*- coding: utf-8 -*-

import csv
from items import Weapon, Rifle, AssaultRifle, SniperRifle, Bow, Shotgun, Pistol, Melee
from polarities import *

item_types = {
    'RIFLE': Rifle,
    'LAUNCHER': Rifle,
    'ASS_RIFLE': AssaultRifle,
    'SNIPER': SniperRifle,
    'BOW': Bow,
    'SHOTGUN': Shotgun,
    'PISTOL': Pistol,
    'MELEE': Melee,
}

polarity_names = {
    'Madurai': Madurai,
    'Vazarin': Vazarin,
    'Naramon': Naramon,
    'Zenurik': Zenurik,
    'Penjaga': Penjaga,
    'Koneksi': Koneksi,
    'Unairu': Unairu,
    'M': Madurai,
    'V': Vazarin,
    'N': Naramon,
    'Z': Zenurik,
    'P': Penjaga,
    'K': Koneksi,
    'U': Unairu,
}

def get_data(files, filters):
    all_found = []
    for filename in files:
        with open(filename, 'rb') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if all(row[col] in filters[col] for col in filters):
                    all_found.append(row)

    return all_found

def get_mods(filters):
    from mod import Mod

    all_mod_data = get_data(('data/gun_mods.csv', 'data/melee_mods.csv'), filters)
    mods = {}
    for mod_data in all_mod_data:
        mod = Mod()
        mod.s = {}
        for stat in mod_data:
            if stat == 'name':
                mod.name = mod_data[stat]
            elif stat == 'type':
                pass
            elif stat == 'polarity':
                mod.polarity = polarity_names[mod_data[stat]]
            elif stat == 'drain':
                mod.drain = int(mod_data[stat])
            elif stat == 'max_rank':
                mod.max_rank = int(mod_data[stat])
            elif stat == 'primed':
                mod.primed = mod_data[stat] == 'True'
            elif stat == 'bow2xfr':
                mod.bow2xfr = mod_data[stat] == 'True'
            elif stat == 'corrupted':
                mod.corrupted = mod_data[stat] == 'True'
            elif mod_data[stat] != '':
                mod.s[stat] = float(mod_data[stat])
                if stat == 'damage_faction':
                    mod.faction = True
        mods[mod.name] = mod
    return mods

def get_item(name):
    item_data = get_data(('data/guns.csv', 'data/melee.csv'), {'name': [name]})[0]
    # print item_data
    item_type = item_types[item_data['type']]
    item = item_type()
    item.s = {}
    if item_data['name']:
        item.name = item_data['name']
    if item_data['type']:
        item.type = item_data['type']
    if item_data['polarities']:
        item.polarities = [] if item_data['polarities'] == '-' else [polarity_names[pol_name] for pol_name in item_data['polarities'].split(',')]
    if isinstance(item, Weapon):
        if item_data['trigger']:
            item.trigger = item_data['trigger']
    columns = ('accuracy', 'crit_chance', 'crit_mult', 'fire_rate', 'mag_size', 'ammo', 'reload', 'stat_chance', 'impact', 'punct', 'slash', 'heat', 'cold', 'electr', 'toxin', 'corrosive', 'blast', 'gas', 'magnetic', 'rad', 'viral')
    for name in columns:
        if name not in item_data:
            continue
        if not item_data[name]:
            continue
        item.s[name] = float(item_data[name])

    if isinstance(item, Weapon):
        item.sum_dmg()
    return item

def get_incompatible(filters):
    inc_mods_data = get_data(('data/incompatible_mods.csv',), filters)
    return [(line['mod1'], line['mod2']) for line in inc_mods_data]
