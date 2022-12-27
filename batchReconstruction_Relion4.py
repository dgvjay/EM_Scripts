#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Digvijay Singh (digvijay.in1 at gmail.com)
import sys
import subprocess
import getopt
import argparse

# THE MAIN SCRIPT STARTS from here
parser=argparse.ArgumentParser(description='''Will batch reconstruct tomograms in Relion4 project based on the input of the tomograms.star file, input of the prefix of tomograms in your project and input of the range of tomograms to reconstructio. Pass only -h flag with no input for help. Example: batchReconstruction_Relion4 -t tomograms.star -p TS_ -r 1#15 -b 4 -j 12''', epilog="""For questions, contact at digvijay.in1 at gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-t', '--tomostar_name', help='Path to tomo star file', required=True)
requiredNamed.add_argument('-p', '--tomo_prefix', help='Prefix of tomogram names, like TD_ or TS_', required=True)
requiredNamed.add_argument('-r', '--tomo_range', help='Range of tomograms to reconstruction. E.g., from 2 to 6, should be input as 2#6', required=True)
requiredNamed.add_argument('-b', '--bin', help='Binning of tomograms', required=True)
requiredNamed.add_argument('-j', '--threads', help='Number of threads to use', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 't:p:r:b:j:',
                               ['tomostar_name','tomo_prefix','tomo_range','bin','threads'])
for opt, arg in opts:
 if opt in ('-t', '--tomostar_name'):
  tomostar_name=arg
 if opt in ('-p', '--tomo_prefix'):
  tomo_prefix=arg
 if opt in ('-r', '--tomo_range'):
  tomo_range=arg.split('#')
 if opt in ('-b', '--bin'):
  bin=arg
 if opt in ('-j', '--threads'):
  n_threads=arg

for x in range(int(tomo_range[0]),int(tomo_range[1])):
 Command="module unload relion ; module load relion/4.0-beta2;relion_tomo_reconstruct_tomogram --t "+tomostar_name+" --tn "+tomo_prefix+str(x)+" --noctf --o ./reconstructions/TD_"+str(x)+".mrc --bin "+bin+" --j "+n_threads
 print(Command)
 subprocess.call(['/bin/csh', '-c', Command])
