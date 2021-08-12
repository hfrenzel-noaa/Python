#!/usr/bin/env python
#
# rename_file_by_date.py: Simple utility script that renames or copies
# one or more files by appending the date (and optionally time)
# of its creation to the original name.
#
# H. Frenzel, CICOES, University of Washington // NOAA-PMEL
#
# Latest version: August 12, 2021
#
# First version:  March 3, 2020

import argparse
import os
import shutil

from datetime import datetime


def parse_input_args():
    '''Parse the command line arguments and return them as an object.'''
    parser = argparse.ArgumentParser()

    # required argument:
    parser.add_argument('filename_in', nargs='+',
                        help='name of the input file')
    # options:
    parser.add_argument('-c', '--copy', action='store_true',
                        dest='create_copy', default = False,
                        help='copy file instead of renaming it')
    parser.add_argument('-t', '--test', action='store_true',
                        dest='test_only', default=False,
                        help='show commands without executing them')
    parser.add_argument('-T', '--time', action='store_true',
                        dest='add_time', default=False,
                        help='add time of file creation to new file name')
    parser.add_argument('-v', '--verbose', action='store_true',
                        dest='verbose', default=False,
                        help='show commands')
    args = parser.parse_args()
    return args


def process_file(filename, args):
    '''Rename or copy the file with the given name by adding date
    and optionally time to its name.'''
    if not os.path.isfile(filename):
        print('{0:s} is not a file!'.format(filename))
    else:
        mtime = os.path.getmtime(filename)
        if args.add_time:
            date = datetime.fromtimestamp(mtime).strftime('%b_%d_%Y_%H:%M:%S')
        else: # use date only
            date = datetime.fromtimestamp(mtime).strftime('%b_%d_%Y')
        new_file = '{0:s}_{1:s}'.format(filename, date)    
        if args.create_copy:
            if args.test_only or args.verbose:
                print('cp {0:s} {1:s}'.format(filename, new_file))
            if not args.test_only:    
                shutil.copy2(filename, new_file)
        else:
            if args.test_only or args.verbose:
                print('mv {0:s} {1:s}'.format(filename, new_file))
            if not args.test_only:    
                shutil.move(filename, new_file)


if __name__ == '__main__':
    args = parse_input_args()
    for file in args.filename_in:
        process_file(file, args)
