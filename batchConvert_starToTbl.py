#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Digvijay Singh (digvijay.in1@gmail.com)
import sys
from glob import glob
import glob, os
import getopt
import argparse


# THE MAIN SCRIPT STARTS from here
parser=argparse.ArgumentParser(description='''Will batch convert all Relion3.0 star file in the input directory (input in -d with / at end) using Alister Burt's dynamo2m function, so warp2dynamo should be in your path''', epilog="""For questions, contact at digvijay.in1@gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-b', '--box_size', help='Box size in .tbl files', required=True)
requiredNamed.add_argument('-d', '--star_directory', help='Directory containing star files you want converted into .tbl', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 'b:d:',
                               ['box_size', 'star_directory'])
for opt, arg in opts:
 if opt in ('-b', '--box_size'):
  box_size = arg
 if opt in ('-d', '--star_directory'):
  star_directory = arg

for star_file in glob.glob(star_directory + "*.star"):
 #relevant_name = star_file[0:-18]
 relevant_name = star_file
 try:
  #os.system("/home/dsingh/.local/bin/warp2dynamo -i " + star_file + " -o " +
   #         relevant_name + ".tbl -bs " + box_size)
  os.system("warp2dynamo -i " + star_file + " -o " +relevant_name + ".tbl -bs " + box_size)
 except:
  pass
