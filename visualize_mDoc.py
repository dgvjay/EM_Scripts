# By Digvijay Singh (digvijay.in1 at gmail.com)
import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import numpy as np
import re
import getopt
import argparse
import sys


# THE MAIN SCRIPT STARTS from here
parser=argparse.ArgumentParser(description='''Will parse all the mdoc file present in the input directory (input with -d with \ at end) and generate plots summarizing various attributes of the mdoc files''', epilog="""For questions, contact at digvijay.in1 at gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-d', '--mdoc_directory', help='Directory containing all mdocs whose you want parsed/visually summarized', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 'd:',
                               ['mdoc_directory'])
for opt, arg in opts:
 if opt in ('-d', '--mdoc_directory'):
  mdoc_directory=arg
 
for mdoc_file in glob.glob(mdoc_directory+"*.mdoc"):
 exposure_times = []
 tilt_angles=[]
 countsPer_electron=[]
 mean_intensities=[]
 max_intensities=[]
 with open(mdoc_file, "r") as f:
  for line in f:
   match1=re.search('ExposureTime = ?(\d*.\d*)',line)
   match2=re.search('TiltAngle = ?(-?\d*.\d*)',line)
   match3=re.search('CountsPerElectron = ?(\d*.\d*)',line)
   match4=re.search('MinMaxMean = ?(\d*.\d*)\s(\d*.\d*)\s(\d*.\d*)',line)
   if match1:
    exposure_times.append(float(match1.group(1)))
   if match2:
    tilt_angles.append(float(match2.group(1)))
   if match3:
    countsPer_electron.append(float(match3.group(1)))
   if match4:
    mean_intensities.append(float(match4.group(3)))
    max_intensities.append(float(match4.group(2)))
 f.close()
 Increment=abs(tilt_angles[0]-tilt_angles[1])
 dose_rates=[aa/(bb*cc) for aa,bb,cc in zip(mean_intensities, countsPer_electron,exposure_times)]
 doseRate_atPreTiltZero=max(dose_rates)
 preTilt_zero= tilt_angles[dose_rates.index(max(dose_rates))]
 maxbyMean_intensities= [aa/bb for aa,bb in zip(max_intensities,mean_intensities)]
 fplot = plt.figure(figsize=(6.25,7))
 ax1=fplot.add_subplot(311)
 ax2=fplot.add_subplot(312)
 ax3=fplot.add_subplot(313)
 fig = plt.figure()
 ax1.plot(tilt_angles, dose_rates, 'o', color='black',label='Through sample(e-/pix/s)',markersize=3)
 ax1.legend(loc='best', fancybox=True, numpoints=1,prop={'size': 5})
 ax1.set_xlabel("Tilt (Degrees)",fontsize=7)
 ax1.set_ylabel("Doserate on Camera(e-/pix/s)",fontsize=7)
 ax1.tick_params(labelsize=8)
 ax2.plot(tilt_angles, exposure_times, 'o', color='black',label='Exposure Time(s)',markersize=3)
 ax2.set_xlabel("Tilt (Degrees)",fontsize=7)
 ax2.set_ylabel("Exposure Time(s)",fontsize=7)
 ax2.legend(loc='best', fancybox=True, numpoints=1,prop={'size': 5})
 ax2.tick_params(labelsize=8)
 ax3.plot(tilt_angles, maxbyMean_intensities, 'o', color='yellow',label='MaxbyMean Intensity',markersize=3)
 ax3.set_xlabel("Tilt (Degrees)",fontsize=7)
 ax3.set_ylabel("MaxbyMean Intensity",fontsize=7)
 ax3.legend(loc='best', fancybox=True, numpoints=1,prop={'size': 5})
 ax3.tick_params(labelsize=8)
 fplot.suptitle("Dose Rates, exposures times etc. vs.tilt angle")
 fplot.subplots_adjust(bottom=0.1, left=0.125,right=0.975, top=0.94,wspace = 0.3,hspace = 0.15)
 fplot.savefig(mdoc_file + '_AttributesVsTiltAngle.png',dpi=300)
