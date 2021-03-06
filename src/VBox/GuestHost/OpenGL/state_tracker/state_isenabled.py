# Copyright (c) 2001, Stanford University
# All rights reserved.
#
# See the file LICENSE.txt for information on redistributing this software.

import sys, re, string
import apiutil


line_re = re.compile(r'^(\S+)\s+(GL_\S+)\s+(.*)\s*$')
extensions_line_re = re.compile(r'^(\S+)\s+(GL_\S+)\s(\S+)\s+(.*)\s*$')

params = {}
extended_params = {}

input = open( sys.argv[2]+"/state_isenabled.txt", 'r' )
for line in input.readlines():
	match = line_re.match( line )
	if match:
		type = match.group(1)
		pname = match.group(2)
		fields = string.split( match.group(3) )
		params[pname] = ( type, fields )

input = open( sys.argv[2]+"/state_extensions_isenabled.txt", 'r' )
for line in input.readlines():
	match = extensions_line_re.match( line )
	if match:
		type = match.group(1)
		pname = match.group(2)
		ifdef = match.group(3)
		fields = string.split( match.group(4) )
		extended_params[pname] = ( type, ifdef, fields )

apiutil.CopyrightC()

print """
/* DO NOT EDIT - THIS FILE GENERATED BY THE state_isenabled.py SCRIPT */
#include <stdio.h>
#include <math.h>

#include "state.h"
#include "state/cr_statetypes.h"

GLboolean STATE_APIENTRY crStateIsEnabled( GLenum pname )
{
	CRContext *g = GetCurrentContext();

	if (g->current.inBeginEnd)
	{
		crStateError(__LINE__, __FILE__, GL_INVALID_OPERATION, "glGet called in Begin/End");
		return 0;
	}

    switch ( pname ) {
"""

keys = params.keys()
keys.sort();

for pname in keys:
	print "\tcase %s:" % pname
	print "\t\treturn %s;" % params[pname][1][0]

keys = extended_params.keys();
keys.sort()

for pname in keys:
	(srctype,ifdef,fields) = extended_params[pname]
	ext = ifdef[3:]  # the extension name with the "GL_" prefix removed
	ext = ifdef
	print '#ifdef CR_%s' % ext
	print "\tcase %s:" % pname
	print "\t\treturn %s;" % extended_params[pname][2][0]
	print '#endif /* CR_%s */' % ext
print "\tdefault:"
print "\t\tcrStateError(__LINE__, __FILE__, GL_INVALID_ENUM, \"glIsEnabled: Unknown enum: %d\", pname);"
print "\t\treturn 0;"
print "\t}"
print "}"
