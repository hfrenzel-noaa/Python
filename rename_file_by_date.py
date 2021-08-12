#!/usr/bin/env python
#
# rename_file_by_date.py
#
# H. Frenzel, School of Oceanography, University of Washington
#
# First version: March 3, 2020

from __future__ import print_function

from sys import argv
import os
from optparse import OptionParser
import systools
from datetime import datetime
from systools import print_execute_command

parser = OptionParser()
parser.add_option("-c", "--copy", action="store_true",
                  dest="create_copy", default=False,
                  help="copy file instead of renaming it")
parser.add_option("-t", "--test", action="store_false",
                  dest="run_cmd", default=True,
                  help="show commands without executing them")

# note that in "args" the first element is 0, not 1 as in original argv!
(options, args) = parser.parse_args()

op = 'mv'
if options.create_copy:
    op = 'cp -p'
    
if len(args) < 1:
    print("\nError: rename_file_by_date.py [-t] file(s)\n\n")
    os.system(argv[0] + ' -h')
    exit(1)

files = args
for file in files:
    if not os.path.isfile(file):
        print(file + ' is not a file!')
        continue # keep going, try the other files
    else:
        mtime = os.path.getmtime(file)
        date = datetime.fromtimestamp(mtime).strftime('%b_%d_%Y')
        file_new = file + '.' + date
        cmd = '{0:s} {1:s} {2:s}'.format(op, file, file_new)
        print_execute_command(cmd, options.run_cmd)

