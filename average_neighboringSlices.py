#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Digvijay Singh (digvijay.in1 at gmail.com)
import sys
import os
import subprocess
import getopt
import argparse


 
def make_stack(tomo_name,slices_sum):
 proc = subprocess.Popen("header -size "+tomo_name, shell=True, stdout =subprocess.PIPE)
 size_string=proc.communicate()[0]
 #size_string.decode("utf-8")
 size_string=str(size_string,'utf-8')
 max_z=int(int(size_string.split("    ")[3]))
 max_z=max_z-slices_sum
 counter=0
 for i in range(1,slices_sum):
  counter=counter+1
  os.system("mrc2tif -z "+str(counter)+","+str(max_z+counter)+" -s "+tomo_name+ " ./Tiffs_"+str(counter)+".tiff")
 os.system("clip average ./Tiffs_*.tiff "+tomo_name[0:-4]+"_Averaged.mrc")
 os.system("clip contrast "+tomo_name[0:-4]+"_Averaged.mrc "+tomo_name[0:-4]+"_Averaged.mrc")
 counter=0
 for i in range(1,slices_sum):
  counter=counter+1
  os.remove("./Tiffs_"+str(counter)+".tiff")
 if os.path.isfile(tomo_name[0:-4]+"_Averaged.mrc~"):
  os.remove(tomo_name[0:-4]+"_Averaged.mrc~")
 
# THE MAIN SCRIPT STARTS from here
parser=argparse.ArgumentParser(description='''Will take a tomogram as input and generate a new one where every slice is an average of the n (also input) slices. Pass only -h flag with no input for help''', epilog="""For questions, contact at digvijay.in1 at gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-t', '--tomo_name', help='Path to tomogram file', required=True)
requiredNamed.add_argument('-s', '--slices_sum', help='number of neighoring slices to average', required=True)
args=parser.parse_args()

opts, args = getopt.gnu_getopt(sys.argv[1:], 't:s:',
                               ['tomo_name','slices_sum'])
for opt, arg in opts:
 if opt in ('-t', '--tomo_name'):
  tomo_name=arg
 if opt in ('-s', '--slices_sum'):
  slices_sum=int(round((int(arg)/2)*2)) # Number of Slices to sum. It must be made the nearest even, if it not an even number.
make_stack(tomo_name,slices_sum)
