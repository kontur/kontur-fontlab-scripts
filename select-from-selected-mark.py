#FLM: Select all glyphs with similar marking as selected

# Script to select all glyphs with similar marking as the 
# currently selected glyph(s)
#
# Johannes 'kontur' Neumeier, 2015
# <hello@johannesneumeier.com>
#
# Note: Treats unmarked glyphs as one group of marked glyphs
#
# Example: 
# - Open a Font and select one glyph with Red marking
# - All other Red marked glyphs will be selected
#
# - Open a Font and select several glyphs, one with no marking 
#	and one with Red marking
# - All other unmarked and Red glyphs will be selected

from FL import *
from sets import Set

glyphs = fl.font.glyphs
selected = []
noneSelected = "Select some existing glyph(s) to select similarly marked glyphs"

# retrieve all selected glyphs
def getSelected(font, glyph, gindex):
	selected.append(glyph)
fl.ForSelected(getSelected)

if selected is not None and len(selected) > 0: # exclude iterating over nothing

	# for all selected glyphs, gather their marks
	marks = Set([])
	for glyph in selected:
		if glyph is not None:
			if hasattr(glyph, "mark"): # marked glyph
				marks.add(glyph.mark)
			else: # unmakred but existing glyph
				marks.add(None)
		else:
			if glyph is None: # non-existing glyph (i.e. in Font window but no data)
				print noneSelected

	for g in glyphs:
		if g.mark and g.mark in marks: # selecting of similar marks
			fl.Select(g.name)
		elif not g.mark and 0 in marks: # selecting other unselected
			fl.Select(g.name)

else: # if no existing glyphs at all were among the selected
	print noneSelected