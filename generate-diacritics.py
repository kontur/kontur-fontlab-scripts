#FLM: Generate diacritcs (options prompt)

# Diacritics generation script
#
# Johannes 'kontur' Neumeier, 2015
# <hello@johannesneumeier.com>
#
# TODO implement dialog and possibility to retain component scale
# TODO solve how to implement multiple component diacritics

from FL import *
from robofab.world import CurrentFont
from robofab.world import CurrentGlyph
from robofab.interface.all.dialogs import *
import re

# global variables

# preliminary list of diacritics from
# https://github.com/robofab-developers/robofab/blob/master/Lib/robofab/tools/glyphConstruction.py
diacritics = {
	'AEacute': ['AE', ['acute']],
	'AEmacron': ['AE', ['macron']],
	'Aacute': ['A', ['acute']],
	'Abreve': ['A', ['breve']],
	'Abreveacute': ['A', ['breve']],
	'Abrevedotaccent': ['A', ['breve', 'dot']],
	'Abrevegrave': ['A', ['breve']],
	'Abrevetilde': ['A', ['breve']],
	'Acaron': ['A', ['caron']],
	'Acircumflex': ['A', ['circumflex']],
	'Acircumflexacute': ['A', ['circumflex', 'acute']],
	'Acircumflexdotaccent': ['A', ['circumflex', 'dotaccent']],
	'Acircumflexgrave': ['A', ['circumflex', 'grave']],
	'Acircumflextilde': ['A', ['circumflex', 'tilde']],
	'Adblgrave': ['A', ['dblgrave']],
	'Adieresis': ['A', ['dieresis']],
	'Adieresismacron': ['A', ['dieresis', 'macron']],
	'Adotaccent': ['A', ['dotaccent']],
	'Adotaccentmacron': ['A', ['dotaccent', 'macron']],
	'Agrave': ['A', ['grave']],
	'Amacron': ['A', ['macron']],
	'Aogonek': ['A', ['ogonek']],
	'Aring': ['A', ['ring']],
	'Aringacute': ['A', ['ring', 'acute']],
	'Atilde': ['A', ['tilde']],
	'Bdotaccent': ['B', ['dotaccent']],
	'Cacute': ['C', ['acute']],
	'Ccaron': ['C', ['caron']],
	'Ccedilla': ['C', ['cedilla']],
	'Ccedillaacute': ['C', ['cedilla', 'acute']],
	'Ccircumflex': ['C', ['circumflex']],
	'Cdotaccent': ['C', ['dotaccent']],
	'Dcaron': ['D', ['caron']],
	'Dcedilla': ['D', ['cedilla']],
	'Ddotaccent': ['D', ['dotaccent']],
	'Eacute': ['E', ['acute']],
	'Ebreve': ['E', ['breve']],
	'Ecaron': ['E', ['caron']],
	'Ecedilla': ['E', ['cedilla']],
	'Ecedillabreve': ['E', ['cedilla', 'breve']],
	'Ecircumflex': ['E', ['circumflex']],
	'Ecircumflexacute': ['E', ['circumflex', 'acute']],
	'Ecircumflexdotaccent': ['E', ['circumflex', 'dotaccent']],
	'Ecircumflexgrave': ['E', ['circumflex', 'grave']],
	'Ecircumflextilde': ['E', ['circumflex', 'tilde']],
	'Edblgrave': ['E', ['dblgrave']],
	'Edieresis': ['E', ['dieresis']],
	'Edotaccent': ['E', ['dotaccent']],
	'Egrave': ['E', ['grave']],
	'Emacron': ['E', ['macron']],
	'Emacronacute': ['E', ['macron', 'acute']],
	'Emacrongrave': ['E', ['macron', 'grave']],
	'Eogonek': ['E', ['ogonek']],
	'Etilde': ['E', ['tilde']],
	'Fdotaccent': ['F', ['dotaccent']],
	'Gacute': ['G', ['acute']],
	'Gbreve': ['G', ['breve']],
	'Gcaron': ['G', ['caron']],
	'Gcedilla': ['G', ['cedilla']],
	'Gcircumflex': ['G', ['circumflex']],
	'Gcommaaccent': ['G', ['commaaccent']],
	'Gdotaccent': ['G', ['dotaccent']],
	'Gmacron': ['G', ['macron']],
	'Hcaron': ['H', ['caron']],
	'Hcedilla': ['H', ['cedilla']],
	'Hcircumflex': ['H', ['circumflex']],
	'Hdieresis': ['H', ['dieresis']],
	'Hdotaccent': ['H', ['dotaccent']],
	'Iacute': ['I', ['acute']],
	'Ibreve': ['I', ['breve']],
	'Icaron': ['I', ['caron']],
	'Icircumflex': ['I', ['circumflex']],
	'Idblgrave': ['I', ['dblgrave']],
	'Idieresis': ['I', ['dieresis']],
	'Idieresisacute': ['I', ['dieresis', 'acute']],
	'Idotaccent': ['I', ['dotaccent']],
	'Igrave': ['I', ['grave']],
	'Imacron': ['I', ['macron']],
	'Iogonek': ['I', ['ogonek']],
	'Itilde': ['I', ['tilde']],
	'Jcircumflex': ['J', ['circumflex']],
	'Kacute': ['K', ['acute']],
	'Kcaron': ['K', ['caron']],
	'Kcedilla': ['K', ['cedilla']],
	'Kcommaaccent': ['K', ['commaaccent']],
	'Lacute': ['L', ['acute']],
	'Lcaron': ['L', ['commaaccent']],
	'Lcedilla': ['L', ['cedilla']],
	'Lcommaaccent': ['L', ['commaaccent']],
	'Ldot': ['L', ['dot']],
	'Ldotaccent': ['L', ['dotaccent']],
	'Ldotaccentmacron': ['L', ['dotaccent', 'n']],
	'Macute': ['M', ['acute']],
	'Mdotaccent': ['M', ['dotaccent']],
	'Nacute': ['N', ['acute']],
	'Ncaron': ['N', ['caron']],
	'Ncedilla': ['N', ['cedilla']],
	'Ncommaaccent': ['N', ['commaaccent']],
	'Ndotaccent': ['N', ['dotaccent']],
	'Ngrave': ['N', ['grave']],
	'Ntilde': ['N', ['tilde']],
	'Oacute': ['O', ['acute']],
	'Obreve': ['O', ['breve']],
	'Ocaron': ['O', ['caron']],
	'Ocircumflex': ['O', ['circumflex']],
	'Ocircumflexacute': ['O', ['circumflex', 'e']],
	'Ocircumflexdotaccent': ['O', ['circumflex', 't']],
	'Ocircumflexgrave': ['O', ['circumflex', 'e']],
	'Ocircumflextilde': ['O', ['circumflex', 'e']],
	'Odblgrave': ['O', ['dblgrave']],
	'Odieresis': ['O', ['dieresis']],
	'Odieresismacron': ['O', ['dieresis', 'n']],
	'Ograve': ['O', ['grave']],
	'Ohungarumlaut': ['O', ['hungarumlaut']],
	'Omacron': ['O', ['macron']],
	'Omacronacute': ['O', ['macron', 'e']],
	'Omacrongrave': ['O', ['macron', 'e']],
	'Oogonek': ['O', ['ogonek']],
	'Oogonekmacron': ['O', ['ogonek', 'n']],
	'Oslashacute': ['Oslash', ['acute']],
	'Otilde': ['O', ['tilde']],
	'Otildeacute': ['O', ['tilde', 'e']],
	'Otildedieresis': ['O', ['tilde', 's']],
	'Otildemacron': ['O', ['tilde', 'n']],
	'Pacute': ['P', ['acute']],
	'Pdotaccent': ['P', ['dotaccent']],
	'Racute': ['R', ['acute']],
	'Rcaron': ['R', ['caron']],
	'Rcedilla': ['R', ['cedilla']],
	'Rcommaaccent': ['R', ['commaaccent']],
	'Rdblgrave': ['R', ['dblgrave']],
	'Rdotaccent': ['R', ['dotaccent']],
	'Rdotaccentmacron': ['R', ['dotaccent', 'n']],
	'Sacute': ['S', ['acute']],
	'Sacutedotaccent': ['S', ['acute', 't']],
	'Scaron': ['S', ['caron']],
	'Scarondotaccent': ['S', ['caron', 't']],
	'Scedilla': ['S', ['cedilla']],
	'Scircumflex': ['S', ['circumflex']],
	'Scommaaccent': ['S', ['commaaccent']],
	'Sdotaccent': ['S', ['dotaccent']],
	'Tcaron': ['T', ['caron']],
	'Tcedilla': ['T', ['cedilla']],
	'Tcommaaccent': ['T', ['commaaccent']],
	'Tdotaccent': ['T', ['dotaccent']],
	'Uacute': ['U', ['acute']],
	'Ubreve': ['U', ['breve']],
	'Ucaron': ['U', ['caron']],
	'Ucircumflex': ['U', ['circumflex']],
	'Udblgrave': ['U', ['dblgrave']],
	'Udieresis': ['U', ['dieresis']],
	'Udieresisacute': ['U', ['dieresis', 'e']],
	'Udieresiscaron': ['U', ['dieresis', 'n']],
	'Udieresisgrave': ['U', ['dieresis', 'e']],
	'Udieresismacron': ['U', ['dieresis', 'n']],
	'Ugrave': ['U', ['grave']],
	'Uhungarumlaut': ['U', ['hungarumlaut']],
	'Umacron': ['U', ['macron']],
	'Umacrondieresis': ['U', ['macron', 's']],
	'Uogonek': ['U', ['ogonek']],
	'Uring': ['U', ['ring']],
	'Utilde': ['U', ['tilde']],
	'Utildeacute': ['U', ['tilde', 'e']],
	'Vtilde': ['V', ['tilde']],
	'Wacute': ['W', ['acute']],
	'Wcircumflex': ['W', ['circumflex']],
	'Wdieresis': ['W', ['dieresis']],
	'Wdotaccent': ['W', ['dotaccent']],
	'Wgrave': ['W', ['grave']],
	'Xdieresis': ['X', ['dieresis']],
	'Xdotaccent': ['X', ['dotaccent']],
	'Yacute': ['Y', ['acute']],
	'Ycircumflex': ['Y', ['circumflex']],
	'Ydieresis': ['Y', ['dieresis']],
	'Ydotaccent': ['Y', ['dotaccent']],
	'Ygrave': ['Y', ['grave']],
	'Ytilde': ['Y', ['tilde']],
	'Zacute': ['Z', ['acute']],
	'Zcaron': ['Z', ['caron']],
	'Zcircumflex': ['Z', ['circumflex']],
	'Zdotaccent': ['Z', ['dotaccent']],
	
	'aacute': ['a', ['acute']],
	'abreve': ['a', ['breve']],
	'abreveacute': ['a', ['breve', 'e']],
	'abrevedotaccent': ['a', ['breve', 't']],
	'abrevegrave': ['a', ['breve', 'e']],
	'abrevetilde': ['a', ['breve', 'e']],
	'acaron': ['a', ['caron']],
	'acircumflex': ['a', ['circumflex']],
	'acircumflexacute': ['a', ['circumflex', 'e']],
	'acircumflexdotaccent': ['a', ['circumflex', 't']],
	'acircumflexgrave': ['a', ['circumflex', 'e']],
	'acircumflextilde': ['a', ['circumflex', 'e']],
	'adblgrave': ['a', ['dblgrave']],
	'adieresis': ['a', ['dieresis']],
	'adieresismacron': ['a', ['dieresis', 'n']],
	'adotaccent': ['a', ['dotaccent']],
	'adotaccentmacron': ['a', ['dotaccent', 'n']],
	'aeacute': ['ae', ['acute']],
	'aemacron': ['ae', ['macron']],
	'agrave': ['a', ['grave']],
	'amacron': ['a', ['macron']],
	'aogonek': ['a', ['ogonek']],
	'aring': ['a', ['ring']],
	'aringacute': ['a', ['ring', 'e']],
	'atilde': ['a', ['tilde']],
	'bdotaccent': ['b', ['dotaccent']],
	'cacute': ['c', ['acute']],
	'ccaron': ['c', ['caron']],
	'ccedilla': ['c', ['cedilla']],
	'ccedillaacute': ['c', ['cedilla', 'e']],
	'ccircumflex': ['c', ['circumflex']],
	'cdotaccent': ['c', ['dotaccent']],
	'dcaron': ['d', ['commaaccent']],
	'dcedilla': ['d', ['cedilla']],
	'ddotaccent': ['d', ['dotaccent']],
	'dmacron': ['d', ['macron']],
	'eacute': ['e', ['acute']],
	'ebreve': ['e', ['breve']],
	'ecaron': ['e', ['caron']],
	'ecedilla': ['e', ['cedilla']],
	'ecedillabreve': ['e', ['cedilla', 'e']],
	'ecircumflex': ['e', ['circumflex']],
	'ecircumflexacute': ['e', ['circumflex', 'e']],
	'ecircumflexdotaccent': ['e', ['circumflex', 't']],
	'ecircumflexgrave': ['e', ['circumflex', 'e']],
	'ecircumflextilde': ['e', ['circumflex', 'e']],
	'edblgrave': ['e', ['dblgrave']],
	'edieresis': ['e', ['dieresis']],
	'edotaccent': ['e', ['dotaccent']],
	'egrave': ['e', ['grave']],
	'emacron': ['e', ['macron']],
	'emacronacute': ['e', ['macron', 'e']],
	'emacrongrave': ['e', ['macron', 'e']],
	'eogonek': ['e', ['ogonek']],
	'etilde': ['e', ['tilde']],
	'fdotaccent': ['f', ['dotaccent']],
	'gacute': ['g', ['acute']],
	'gbreve': ['g', ['breve']],
	'gcaron': ['g', ['caron']],
	'gcedilla': ['g', ['cedilla']],
	'gcircumflex': ['g', ['circumflex']],
	'gcommaaccent': ['g', ['commaaccent']],
	'gdotaccent': ['g', ['dotaccent']],
	'gmacron': ['g', ['macron']],
	'hcaron': ['h', ['caron']],
	'hcedilla': ['h', ['cedilla']],
	'hcircumflex': ['h', ['circumflex']],
	'hdieresis': ['h', ['dieresis']],
	'hdotaccent': ['h', ['dotaccent']],
	'iacute': ['dotlessi', ['acute']],
	'ibreve': ['dotlessi', ['breve']],
	'icaron': ['dotlessi', ['caron']],
	'icircumflex': ['dotlessi', ['circumflex']],
	'idblgrave': ['dotlessi', ['dblgrave']],
	'idieresis': ['dotlessi', ['dieresis']],
	'idieresisacute': ['dotlessi', ['dieresis', 'e']],
	'igrave': ['dotlessi', ['grave']],
	'imacron': ['dotlessi', ['macron']],
	'iogonek': ['i', ['ogonek']],
	'itilde': ['dotlessi', ['tilde']],
	'jcaron': ['dotlessj', ['caron']],
	'jcircumflex': ['dotlessj', ['circumflex']],
	'jacute': ['dotlessj', ['acute']],
	'kacute': ['k', ['acute']],
	'kcaron': ['k', ['caron']],
	'kcedilla': ['k', ['cedilla']],
	'kcommaaccent': ['k', ['commaaccent']],
	'lacute': ['l', ['acute']],
	'lcaron': ['l', ['commaaccent']],
	'lcedilla': ['l', ['cedilla']],
	'lcommaaccent': ['l', ['commaaccent']],
	'ldot': ['l', ['dot']],
	'ldotaccent': ['l', ['dotaccent']],
	'ldotaccentmacron': ['l', ['dotaccent', 'n']],
	'macute': ['m', ['acute']],
	'mdotaccent': ['m', ['dotaccent']],
	'nacute': ['n', ['acute']],
	'ncaron': ['n', ['caron']],
	'ncedilla': ['n', ['cedilla']],
	'ncommaaccent': ['n', ['commaaccent']],
	'ndotaccent': ['n', ['dotaccent']],
	'ngrave': ['n', ['grave']],
	'ntilde': ['n', ['tilde']],
	'oacute': ['o', ['acute']],
	'obreve': ['o', ['breve']],
	'ocaron': ['o', ['caron']],
	'ocircumflex': ['o', ['circumflex']],
	'ocircumflexacute': ['o', ['circumflex', 'e']],
	'ocircumflexdotaccent': ['o', ['circumflex', 't']],
	'ocircumflexgrave': ['o', ['circumflex', 'e']],
	'ocircumflextilde': ['o', ['circumflex', 'e']],
	'odblgrave': ['o', ['dblgrave']],
	'odieresis': ['o', ['dieresis']],
	'odieresismacron': ['o', ['dieresis', 'n']],
	'ograve': ['o', ['grave']],
	'ohungarumlaut': ['o', ['hungarumlaut']],
	'omacron': ['o', ['macron']],
	'omacronacute': ['o', ['macron', 'e']],
	'omacrongrave': ['o', ['macron', 'e']],
	'oogonek': ['o', ['ogonek']],
	'oogonekmacron': ['o', ['ogonek', 'n']],
	'oslashacute': ['oslash', ['acute']],
	'otilde': ['o', ['tilde']],
	'otildeacute': ['o', ['tilde', 'e']],
	'otildedieresis': ['o', ['tilde', 's']],
	'otildemacron': ['o', ['tilde', 'n']],
	'pacute': ['p', ['acute']],
	'pdotaccent': ['p', ['dotaccent']],
	'racute': ['r', ['acute']],
	'rcaron': ['r', ['caron']],
	'rcedilla': ['r', ['cedilla']],
	'rcommaaccent': ['r', ['commaaccent']],
	'rdblgrave': ['r', ['dblgrave']],
	'rdotaccent': ['r', ['dotaccent']],
	'rdotaccentmacron': ['r', ['dotaccent', 'n']],
	'sacute': ['s', ['acute']],
	'sacutedotaccent': ['s', ['acute', 't']],
	'scaron': ['s', ['caron']],
	'scarondotaccent': ['s', ['caron', 't']],
	'scedilla': ['s', ['cedilla']],
	'scircumflex': ['s', ['circumflex']],
	'scommaaccent': ['s', ['commaaccent']],
	'sdotaccent': ['s', ['dotaccent']],
	'tcaron': ['t', ['commaaccent']],
	'tcedilla': ['t', ['cedilla']],
	'tcommaaccent': ['t', ['commaaccent']],
	'tdieresis': ['t', ['dieresis']],
	'tdotaccent': ['t', ['dotaccent']],
	'uacute': ['u', ['acute']],
	'ubreve': ['u', ['breve']],
	'ucaron': ['u', ['caron']],
	'ucircumflex': ['u', ['circumflex']],
	'udblgrave': ['u', ['dblgrave']],
	'udieresis': ['u', ['dieresis']],
	'udieresisacute': ['u', ['dieresis', 'e']],
	'udieresiscaron': ['u', ['dieresis', 'n']],
	'udieresisgrave': ['u', ['dieresis', 'e']],
	'udieresismacron': ['u', ['dieresis', 'n']],
	'ugrave': ['u', ['grave']],
	'uhungarumlaut': ['u', ['hungarumlaut']],
	'umacron': ['u', ['macron']],
	'umacrondieresis': ['u', ['macron', 's']],
	'uogonek': ['u', ['ogonek']],
	'uring': ['u', ['ring']],
	'utilde': ['u', ['tilde']],
	'utildeacute': ['u', ['tilde', 'e']],
	'vtilde': ['v', ['tilde']],
	'wacute': ['w', ['acute']],
	'wcircumflex': ['w', ['circumflex']],
	'wdieresis': ['w', ['dieresis']],
	'wdotaccent': ['w', ['dotaccent']],
	'wgrave': ['w', ['grave']],
	'wring': ['w', ['ring']],
	'xdieresis': ['x', ['dieresis']],
	'xdotaccent': ['x', ['dotaccent']],
	'yacute': ['y', ['acute']],
	'ycircumflex': ['y', ['circumflex']],
	'ydieresis': ['y', ['dieresis']],
	'ydotaccent': ['y', ['dotaccent']],
	'ygrave': ['y', ['grave']],
	'yring': ['y', ['ring']],
	'ytilde': ['y', ['tilde']],
	'zacute': ['z', ['acute']],
	'zcaron': ['z', ['caron']],
	'zcircumflex': ['z', ['circumflex']],
	'zdotaccent': ['z', ['dotaccent']]
}
font = CurrentFont()


# CLI messages
messages = {
	'start': 'Starting diacritics generation script',
	'taskpicker': 'Select what to generate',
	'notask': 'No option selected, exiting',
	'end': 'Generation script finished'
}


# top level tasks available
tasks = [
	'Generate all possible diacritics',
	'Generate empty diacritics', 
	'Generate selected diacritics',
	'Regenerate existing diacritics',
	''] #empty task will be returned when nothing is selected

# list for retrieving which glyphs are selected in the Font window
selected = []

# helper functions for the heavy lifting
def findCommonAnchor(glyph, accent):
	glyphAnchors = []
	accentAnchors = []

	if font.has_key(glyph):
		for anchor in font[glyph].anchors:
			glyphAnchors.append(re.sub('^_', '', anchor.name, 1))

	if font.has_key(accent):
		for anchor in font[accent].anchors:
			accentAnchors.append(re.sub('^_', '', anchor.name, 1))

	if (len(glyphAnchors) > 0 and len(accentAnchors) > 0):
		common = list(set(glyphAnchors) & set(accentAnchors))
		# TODO can there ever be a case where more than one anchor
		# is present both in a base glpyh and an accent?
		if len(common) > 0:
			return common[0]
		else:
			return False
	else:
		return False

def createGlyphBackup(glyph):
	font.insertGlyph(font[glyph].copy(), glyph + ".bak")
	return True

def deleteGlyphBackup(glyph):
	font.removeGlyph(glyph + ".bak")
	return True

# retrieve all selected glyphs
def getSelected(font, glyph, gindex):
	selected.append(glyph.name)

def getAllGlyphs(font):
	return map(lambda g: g.name, font.glyphs)

def generateDiacritics(createNew, overwrite, glyphList=False):
	for glyph in diacritics:
		accents = []
		components = True
		oldUnicode = 0
		
		fontGlyphs = getAllGlyphs(font) # all glyphs in font as list of strings

		if glyphList is False:
			glyphList = getAllGlyphs(font)


		# should the list of update glyphs ever be the same
		# as the list of glyphs to update we are done
		# TODO this is also the case if update + failed is the
		# same but that's a more tricky case
		if len(updated) is len(glyphList):
			break;

		# skip this loop if the diacritic sign is not in the list
		# of to do glyphs at all
		if not glyph in glyphList:
			continue;

		# save for convenience and performance
		glyphExists = glyph in fontGlyphs

		# skip this loop if we aren't overwriting but the glyph exists
		if not overwrite and glyphExists:
			continue;

		# for overwriting store some stuff
		if overwrite and glyphExists:
			font[glyph].mark = 0
			oldUnicode = font[glyph].unicode

		# start by figuring out if all required component glyphs
		# exists
		for accent in diacritics[glyph][1]:
			commonAnchor = findCommonAnchor(diacritics[glyph][0], accent)
			if commonAnchor:
				accents.append((accent, commonAnchor))
			else:
				print "No common anchor for glyphs " + glyph + " and " + accent
				components = False
				break;

		if components:
			# if components available and we overwrite, back up
			if overwrite and glyph in glyphList:
				createGlyphBackup(glyph)
				font.removeGlyph(glyph)

			font.compileGlyph(glyph, diacritics[glyph][0], accents)

			font[glyph].autoUnicodes()
			if not font[glyph].unicode:
				if oldUnicode:
					font[glyph].unicode = oldUnicode
				else:
					missingUnicode.append(glyph)

			deleteGlyphBackup(glyph)

			if glyphExists:
				font[glyph].mark = 150
				updated.append(glyph)
			else:
				font[glyph].mark = 50
				created.append(glyph)
		else:
			if glyph in font:
				existingButUntouched.append(glyph)
			else:
				failed.append(glyph)

	font.update()

# script run start	
task = OneList(tasks, 'Select what to generate', 'Generate')
selectedTask = tasks.index(task)


print ""
print messages['start']

created = []
updated = []
existingButUntouched = []
failed = []
missingUnicode = []

#def generateDiacritics(createNew, overwrite, glyphs):
if selectedTask is 0:
	# this task generates all diacritics possible from available
	# base and accent combinations, as found in variable "diacritics"
	print tasks[0]
	generateDiacritics(True, True)

elif selectedTask is 1:
	# this task generates all diacritics possible which are not yet
	# existing glyphs in the font
	print tasks[1]
	generateDiacritics(True, False)

elif selectedTask is 2:
	# this tasks (re-)generates all selected diacritic glyphs
	print tasks[2]
	fl.ForSelected(getSelected)
	generateDiacritics(False, True, selected)

elif selectedTask is 3:
	# this tasks regenerates (overwrites) those diacritic glyphs 
	# that are already in the font
	print tasks[3]
	generateDiacritics(False, True)

else:
	print messages['notask']
if len(created) > 0:
	print ""
	print "The following glyphs were newly created:"
	print created
if len(updated) > 0:
	print ""
	print "The following glyphs were updated:"
	print updated
if len(existingButUntouched) > 0:
	print ""
	print "The following glyphs were found in the font, but could not be generated. The old glyphs were left in the font as they were."
	print existingButUntouched
	print "Check that these glyphs have similar named anchors in all components and all components exist"
if len(failed) > 0:
	print ""
	print "The following glyphs could not be generated:"
	print failed
	print "Check that these glyphs have similar named anchors in all components and all components exist"

if len(missingUnicode) > 0:
	print "---"
	print "Failed to autogenerate unicodes for " + str(len(missingUnicode)) + " glyphs"
	print "Please update manually where glyphs are highlighted in red with yellow label"

print "---"
print "New glyphs........." + str(len(created))
print "Updated glyphs....." + str(len(updated))
print "Unaffected glyphs.." + str(len(existingButUntouched)) + " (these existed in the font but could not be regenerated due to missing components)"
print "Failed glyphs......" + str(len(failed)) + " (not generated due to missing components)"
print "---"
print "Scroll above for more detailed information."
if len(existingButUntouched) > 0 or len(failed) > 0:
	print "Unaffected of failed glyphs might be OK depending on your font scope"

print messages['end']
# script run end