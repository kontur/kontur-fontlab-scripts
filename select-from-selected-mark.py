#FLM: Select all from selected mark

# Script to select all glyphs with similar marking
# Johannes 'kontur' Neumeier, 2015
#

from FL import *
from robofab.world import CurrentGlyph

print ""

# TODO replace this RoboFab dependency with FL native selected
glyph = CurrentGlyph() 

if glyph.mark:
	for g in font:
		if g.mark and g.mark is glyph.mark:
			fl.Select(g.name)