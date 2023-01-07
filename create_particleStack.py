#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Digvijay Singh (digvijay.in1@gmail.com)
import sys, os
import starfile
import pandas as pd
import getopt
import argparse
import subprocess

parser=argparse.ArgumentParser(description='''Will read all image files from the Relion3.1 star file and create a single stack containing all image files, that can be read using programs like EMAN2's powerful e2display.py program and others''', epilog="""For questions, contact at digvijay.in1@gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-s', '--star_file', help='Relion3.1 star file whose image files you want combined into a single stack of images', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 's:',['star_file'])
for opt, arg in opts:
 if opt in ('-s', '--star_file'):
  star_file = arg


all_data=starfile.read(star_file)
all_data=all_data['particles'] #Relion3.1 have data_optics & data_particles groups, selecting the particles group. If using Relion3.0 star file, you can simply omit this step.
image_files=all_data['rlnImageName']
image_files=image_files.values.tolist()

for item in image_files:
 eman_command="module load eman2/2.91; e2proc3d.py "+item+" "+star_file[0:-4]+"hdf --append"
 subprocess.call(['/bin/csh', '-c', eman_command])