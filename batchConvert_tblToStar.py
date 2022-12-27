#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Digvijay Singh (digvijay.in1 at gmail.com)
import sys
from glob import glob
import glob, os
import getopt
import argparse

parser=argparse.ArgumentParser(description='''Will batch convert all Dynamo tbls in the input directory (input in -t with / at end) using Alister Burt's dynamo2m function, so dynamo2warp2 should be in your path''', epilog="""For questions, contact at digvijay.in1 at gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-t', '--tbl_directory', help='Directory containing tbl files you want converted into .star', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 't:', ['tbl_directory'])
for opt, arg in opts:
 if opt in ('-t', '--tbl_directory'):
  tbl_directory = arg

for tbl_name in glob.glob(tbl_directory + "*.tbl"):
 tomo_name = tbl_name[0:-4] + ".mrc"
 print(tomo_name)
 tbl_id = open(tbl_name, "r")
 lines = tbl_id.readlines()
 for x in lines:
  tomo_ID = x.split(' ')[19]
 tbl_id.close()

 with open('temp_map.txt', 'w') as tempfile_id:
  tempfile_id.write(tomo_ID + ' ' + tomo_name)
 tempfile_id.close()
 #os.system("/home/dsingh/.local/bin/dynamo2warp -i " + tbl_name +"  -tm temp_map.txt -o " + tbl_name[0:-4] + ".star")
 os.system("dynamo2warp -i " + tbl_name +" -tm temp_map.txt -o " + tbl_name[0:-4] + ".star")
os.remove('temp_map.txt')
