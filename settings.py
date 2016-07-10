# -*- coding: utf-8 -*-

from names import *
from polarities import *

# The weapon that you're trying to find a mod combination for.
weapon = 'Tonkor'

# Use your own mods. Needs filling personal_mods list below.
use_personal = False

# Use Primed mods, Corrupted mods, and mods with +dmg to a specific faction.
use_primed = True
use_corrupted = True
use_faction = False

# Sort cryterium.
# Examples:
# phys_dmg - physical damage per shot, good for elemental enhancement Sorties
# crit_dmg - damage of a critical hit (may result in e.g. a tiny red crit chance)
# avg_dmg - average total damage per shot
# burst_dps - damage per second
# reload_dps - damage per second, counting reload time
sortby = 'reload_dps'

# Number of the top results displayed after calculations.
num_of_top_results = 10

# The drain limit for mods. Set to None if you don't want it to be limited (if you want to check the best possible build).
point_limit = None

# The minimum and maximum number of mods in a combination that you want to check.
num_of_mods_min = 1
num_of_mods_max = 8

# Skip mods which don't affect your desired stat. Results in faster calculations.
# For example, if you are looking for highest possible fire_rate, Serration (damage mod) won't be taken into consideration
use_mods_smart = True

# Set a limit on shots per second of non-automatic weapons. Set to None if you don't want to limit it, but don't expect to get achieveable results if it goes over 6.
limit_fr_of_non_auto = 5

# You can write down your mods for each weapon type, to check which build will maximize your stats in your current situation.
# Has no effect if use_personal = False
# Usage:
# personal_mods = {
#     weapon_type: {
#         mod_name: list_of_available_levels,
#         mod_name2: list_of_available_levels,
#     },
# }
# Example:
# personal_mods = {
#     'RIFLE': {
#         'Serration': [0, 6, 10],
#         'SplitChamber': [5],
#     },
#     'SHOTGUN': {
#         'PointBlank': [5],
#         'PrimedPointBlank': [8],
#     },
# }
personal_mods = {
    'RIFLE': {},
    'ASS_RIFLE': {},
    'SNIPER': {},
    'BOW': {},
    'SHOTGUN': {},
    'PISTOL': {},
    'MELEE': {},
}

# You can set custom polarities of your forma'ed weapons, to use them instead of their default polarities.
# Has no effect if point_limit = None
# Example:
# custom_polarities = {
#     'Tonkor': [Madurai, Madurai, Madurai, Naramon],
#     'Skana': [Vazarin],
# }
custom_polarities = {
}
