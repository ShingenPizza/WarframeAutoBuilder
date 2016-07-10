It's a program for Warframe players.

It's designed to find the mod build that will result in the highest possible value of a chosen stat of a weapon, mostly damage calculated in one of the ways.
There is at least one website out there that lets you apply any mods to any weapon and see the results, but what I needed is something that will check every combination of mods and just tell me which is the best one.
It allows to find both the best mod build overall, as well as one taking into consideration currently available points and mods (especially helpful for new players).

USAGE:
1. Set your settings by editing settings.py (more info there)
2. Run run.py (you need Python 2.7)
3. Wait for results

It's a work in progress.
It works properly (AFAIK) with the data it has, but misses plenty of weapons and some mods. I want to add PVP mods and Archwing weapons in the future.

If you want to use it for weapons/mods that are not yet in the data/*.csv files, you can try to add them yourself, and they should work, as long as you fill all required fields.

NOTE:
This program calculates raw damage, without taking armor or damage modifiers (like bonus to slash damage vs flesh) into consideration.
Weapons with AOE are calculated in a pretty arbitrary fashion, showing damage of a direct hit on a single target.

I am of course not responsible for you wasting Formas and such.

Warframe belongs to Digital Extremes, blah blah blah, I am in no way affiliated with them.
It's a project by a fan, for fans.
