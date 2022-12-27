#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Digvijay Singh (digvijay.in1 at gmail.com)
import sys
from glob import glob
import glob, os
import starfile
import pandas as pd
import getopt
import argparse

# THE MAIN SCRIPT STARTS from here
parser=argparse.ArgumentParser(description='''Will batch read all Relion 3.0 style star files into the input directory (input with -d with \ at end) using Alister Burt's starfile into panda dataframes and combine them all to a combined star file.Example: combine_starFiles.py -c combo.star -d /data/stars/''', epilog="""For questions, contact at digvijay.in1 at gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-c', '--combined_star', help='Name of the output starfile combining all other star files', required=True)
requiredNamed.add_argument('-d', '--star_directory', help='Directory containing star files you want combined into one', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 'c:d:',
                               ['combined_star', 'star_directory'])
for opt, arg in opts:
 if opt in ('-c', '--combined_star'):
  combined_starfile = arg
 if opt in ('-d', '--star_directory'):
  star_directory = arg

data_frame = pd.DataFrame(index=range(1, 7))
for star_file in glob.glob(star_directory + "*.star"):
 temp = starfile.read(star_file)
 data_frame = pd.concat([data_frame, temp], axis=0)
starfile.write(data_frame, combined_starfile,overwrite=True)