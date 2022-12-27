#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Digvijay Singh (digvijay.in1 at gmail.com)
import os
import sys
import getopt
import argparse
import subprocess
from EMAN2 import *
parser=argparse.ArgumentParser(description='''Will calculate local resolution between two half maps using the input box size using EMAN2's e2fsc_real_local.py''', epilog="""For questions, contact at digvijay.in1 at gmail.com.""")

#Optional arguments
#parser.add_argument('-o', '--output', help='Output file name', default='stdout')
requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-o', '--odd_map', help='Path to odd_map file', required=True)
requiredNamed.add_argument('-e', '--even_map', help='Path to even map file', required=True)
requiredNamed.add_argument('-l', '--local_size', help='local size for local resolution (in Angstroms)', required=True)
requiredNamed.add_argument('-m', '--mask', help='Mask', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 'o:e:l:m:',
                               ['odd_map','even_map','local_size','mask'])
for opt, arg in opts:
 if opt in ('-o', '--odd_map'):
  odd_map = arg
 if opt in ('-e', '--even_map'):
  even_map = arg
 if opt in ('-l', '--local_size'):
  local_size= int(arg)
 if opt in ('-m', '--mask'):
  mask= arg



 
EMANCommand="module load eman2/2.91;e2fsc_real_local.py "+even_map+" "+odd_map+" --output fscvol_"+str(local_size)+".hdf --localsizea "+str(local_size)+" --threads 20 --compressbits 12 -v 1 --outfilt LocFiltered_WithLocalArea_"+str(local_size)+".hdf"
subprocess.call(['/bin/csh', '-c', EMANCommand])


EMANCommand="module load eman2/2.91;e2proc3d.py fscvol_"+str(local_size)+".hdf fscvol_"+str(local_size)+".hdf --process=math.reciprocal"
subprocess.call(['/bin/csh', '-c', EMANCommand])



EMANCommand="module load eman2/2.91;e2proc3d.py LocFiltered_WithLocalArea_"+str(local_size)+".hdf LocFiltered_WithLocalArea_"+str(local_size)+"_Masked.hdf --multfile="+mask
subprocess.call(['/bin/csh', '-c', EMANCommand])


print('wrote: fscvol_'+str(local_size)+'.hdf')
print('wrote: LocFiltered_WithLocalArea_'+str(local_size)+'.hdf')
print('wrote: LocFiltered_WithLocalArea_'+str(local_size)+'_Masked.hdf')
