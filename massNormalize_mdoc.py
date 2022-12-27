#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Digvijay Singh (digvijay.in1 at gmail.com)
# Run it in the directory containing .mdocs, it will create a new sub-directory called Adjusted_mdoc with adjusted mdoc files with the same name.
import re,sys
import glob, os
import getopt
import argparse


def adjust_mdoc(mdoc_file):
 exposure_times = []
 counts_per_electron = []
 mean_intensities = []
 tilt_angles = []

 with open(mdoc_file, "r") as f:
  for line in f:
   match1 = re.search('ExposureTime = ?(\d*.\d*)', line)
   match2 = re.search('CountsPerElectron = ?(\d*.\d*)', line)
   match3 = re.search('MinMaxMean = ?(\d*.\d*)\s(\d*.\d*)\s(\d*.\d*)', line)
   match4 = re.search('TiltAngle = ?(-?\d*.\d*)', line)
   if match1:
    exposure_times.append(float(match1.group(1)))
   if match2:
    counts_per_electron.append(float(match2.group(1)))
   if match3:
    mean_intensities.append(float(match3.group(3)))
   if match4:
    tilt_angles.append(float(match4.group(1)))
 f.close()

 dose_camera = [
     aa / (bb * cc) for aa, bb, cc in zip(mean_intensities,
                                          counts_per_electron, exposure_times)
 ]
 pretilt_angle = tilt_angles[dose_camera.index(max(dose_camera))]

 input_file = open(mdoc_file, "r")
 if not os.path.exists('./Adjusted_mdoc'):
  os.makedirs('./Adjusted_mdoc')
 output_file = open('./Adjusted_mdoc/' + os.path.basename(mdoc_file), "w")

 for line in input_file:
  match2 = re.search('TiltAngle = ?(-?\d*.\d*)', line)
  match3 = re.search('bidir = ?(-?\d*.\d*)', line)
  if match2:
   new_tilt_angle = float(match2.group(1)) - pretilt_angle
   line = re.sub('TiltAngle = ?(-?\d*.\d*)',
                 'TiltAngle = ' + str(new_tilt_angle), line)
  if match3:
   new_bidirec_angle = float(match3.group(1)) - pretilt_angle
   line = re.sub('bidir = ?(-?\d*.\d*)', 'bidir = ' + str(new_bidirec_angle),
                 line)
  output_file.write(line)
 output_file.close()



# THE MAIN SCRIPT STARTS from here
parser=argparse.ArgumentParser(description='''Will nornalize (i.e. offset by PreTilt Zero angle) tilt angles in all mdocs in the input folder (input with -d with a slash at end) and generate a new folder called Adjusted containing new mdocs with normalized tilt angles. which can then be directly used in WARP & other software''', epilog="""For questions, contact at digvijay.in1 at gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-d', '--mdoc_directory', help='Directory containing all mdocs whose tilt angles you want normalize', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 'd:',
                               ['mdoc_directory'])
for opt, arg in opts:
 if opt in ('-d', '--tomo_name'):
  mdoc_directory=arg
 
for mdoc_file in glob.glob(mdoc_directory+"*.mdoc"):
 print("Normalized:"+mdoc_file)
 adjust_mdoc(mdoc_file)
