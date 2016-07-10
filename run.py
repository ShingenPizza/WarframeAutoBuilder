# -*- coding: utf-8 -*-

import sys

try:
    from settings import weapon
except ImportError:
    weapon = 'Tonkor'
    print 'weapon not set, using default %s' % weapon

try:
    from settings import use_personal
except ImportError:
    use_personal = False
    print 'use_personal not set, using default %s' % use_personal

try:
    from settings import use_primed
except ImportError:
    use_primed = True
    print 'use_primed not set, using default %s' % use_primed

try:
    from settings import use_corrupted
except ImportError:
    use_corrupted = False
    print 'use_corrupted not set, using default %s' % use_corrupted

try:
    from settings import use_faction
except ImportError:
    use_faction = False
    print 'use_faction not set, using default %s' % use_faction

try:
    from settings import sortby
except ImportError:
    sortby = 'avg_dmg'
    print 'sortby not set, using default %s' % sortby

try:
    from settings import num_of_top_results
except ImportError:
    num_of_top_results = 10
    print 'num_of_top_results not set, using default %s' % num_of_top_results

try:
    from settings import point_limit
except ImportError:
    point_limit = None
    print 'point_limit not set, using default %s' % point_limit

try:
    from settings import num_of_mods_min
except ImportError:
    num_of_mods_min = 8
    print 'num_of_mods_min not set, using default %s' % num_of_mods_min

try:
    from settings import num_of_mods_max
except ImportError:
    num_of_mods_max = 8
    print 'num_of_mods_max not set, using default %s' % num_of_mods_max

try:
    from settings import personal_mods
except ImportError:
    personal_mods = {}
    print 'personal_mods not set, using default %s' % personal_mods

try:
    from settings import custom_polarities
except ImportError:
    custom_polarities = {}
    print 'custom_polarities not set, using default %s' % custom_polarities

try:
    from settings import use_mods_smart
except ImportError:
    use_mods_smart = True
    print 'use_mods_smart not set, using default %s' % use_mods_smart

try:
    from settings import limit_fr_of_non_auto
except ImportError:
    limit_fr_of_non_auto = 5
    print 'limit_fr_of_non_auto not set, using default %s' % limit_fr_of_non_auto

from builder import calculate

sett = {
    'weapon': weapon,
    'use_personal': use_personal,
    'use_primed': use_primed,
    'use_corrupted': use_corrupted,
    'use_faction': use_faction,
    'sortby': sortby,
    'num_of_top_results': num_of_top_results,
    'point_limit': point_limit,
    'num_of_mods_min': num_of_mods_min,
    'num_of_mods_max': num_of_mods_max,
    'personal_mods': personal_mods,
    'custom_polarities': custom_polarities,
    'use_mods_smart': use_mods_smart,
    'limit_fr_of_non_auto': limit_fr_of_non_auto,
}

calculate(sett)

if len(sys.argv) < 2 or sys.argv[1] != 'quit':
    raw_input('Waiting, so the console window doesn\'t close. Use \'quit\' parameter to skip it.\n')
