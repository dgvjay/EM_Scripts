

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Digvijay Singh (digvijay.in1@gmail.com)
import sys
from glob import glob
import glob, os
import getopt
import argparse
import shutil

parser=argparse.ArgumentParser(description='''This program will batch AreTomo reconstruct tilt-series present inside each of the sub-directory in the WARP generated IMOD directory (input in -t with / at end). After batch reconstruction, the reconstruction parameters can be read by WARP like IMOD, because .xf files are generated. AreTomo parameters of reconstruction can be changed by changing parameters in the are_string below''', epilog="""For questions, contact at digvijay.in1@gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-t', '--warpImod_directory', help='WARP generated IMOD Directory containing sub-directories representing each of the tilt-series. This program will batch AreTomo reconstruct tilt-series present inside each of the sub-directory', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 't:', ['warpImod_directory'])
for opt, arg in opts:
 if opt in ('-t', '--warpImod_directory'):
  warpImod_directory = arg
  warpImod_directory = os.path.abspath(warpImod_directory)
  
os.chdir(warpImod_directory)
for contents in os.listdir(warpImod_directory):
 pathx = os.path.join(warpImod_directory, contents)
 if os.path.isdir(pathx):
  os.chdir(pathx)
  are_string = "AreTomo_1.1.0_Cuda101 -VolZ 1500 -OutBin 8 -TiltCor -1 -Wbp 1 -AlignZ 800 -FlipVol 1 -InMrc " +contents+".st -OutMrc "+contents+"_recon.mrc -AngFile "+contents+".rawtlt -TiltAxis -95 -Gpu 0,1,2,3 -OutXf 1"
  os.system(are_string)
  try:
   shutil.copyfile(contents[0:-4]+".xf",contents+".xf")
  except Exception:
   pass
  os.chdir(warpImod_directory)
