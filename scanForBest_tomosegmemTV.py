#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Digvijay Singh (digvijay.in1 at gmail.com)
import copy
import shutil
from shutil import copyfile
import sys
import os
import re
import subprocess
import math
import getopt
import numpy as np
import argparse

def stringFile_maker(tomo_name,tomoSeg_param,sum_slices,scale_nm):
 string_file = open(tomo_name+"_string.txt","w")
 string_file.write("ridgeoredgelike: %f \n" %(float(tomoSeg_param[0])))
 string_file.write("scale_space: %f \n" %(float(tomoSeg_param[1])))
 string_file.write("surfaceness_threshold: %f \n" %(float(tomoSeg_param[2])))
 string_file.write("saliency_threshold: %f \n" %(float(tomoSeg_param[3])))
 string_file.write("OverallThreshold: %f \n" %(float(tomoSeg_param[4])))
 string_file.write("Scale Bar: %d \n" %(scale_nm))
 string_file.close()

def slicer_images(tomo_name,tomoSeg_param,sum_slices,scale_nm,annotate_images,index):
 stringFile_maker(tomo_name,tomoSeg_param,sum_slices,scale_nm)
 proc = subprocess.Popen("header -size "+ tomo_name+"_Salient_Threshold.rec", shell=True, stdout =subprocess.PIPE)
 mid_section=int(int(proc.communicate()[0].split("    ")[3])/2)
 os.system("mrc2tif -z "+str(int(mid_section-sum_slices/2))+","+str(int(mid_section+sum_slices/2))+" -s "+tomo_name+"_Salient_Threshold.rec "+tomo_name+"_Segmented_Slice_"+str(index)+".tiff")
 os.system("./slicer_images.py "+tomo_name+"_Segmented_Slice_"+str(index)+".tiff "+tomo_name+"_string.txt "+annotate_images)
 if not os.path.exists("SegmemTVSlicers"):
  os.makedirs("SegmemTVSlicers")
 shutil.move(tomo_name+"_Segmented_Slice_"+str(index)+".tif","./SegmemTVSlicers/"+tomo_name+"_Segmented_Slice_"+str(index)+".tif")

def calc_pixSize(tomo_name):
 proc = subprocess.Popen("header -pixel "+tomo_name+".rec", shell=True,stdout =subprocess.PIPE)
 pix_size=float([x for x in proc.communicate()[0].split("\n")[0].split(" ") if x != ''][0])
 return pix_size
  
def tomoSegmemTV(tomo_name,tomoSeg_param,pix_size):
 os.system("scale_space -s "+str(float(tomoSeg_param[1])/pix_size)+" "+tomo_name+".rec "+tomo_name+"_scaled_space.rec")
 if float(tomoSeg_param[0])==1.0:
  os.system("dtvoting "+tomo_name+"_scaled_space.rec "+tomo_name+"_tv.rec")
 else:
  os.system("dtvoting -e "+tomo_name+"_scaled_space.rec "+tomo_name+"_tv.rec")
 os.system("surfaceness -m "+str(float(tomoSeg_param[2]))+" "+tomo_name+"_tv.rec "+tomo_name+"_surface.rec")
 os.system("dtvoting -w  "+tomo_name+"_surface.rec "+tomo_name+"_tv2.rec")
 os.system("surfaceness -S -s "+str(float(tomoSeg_param[3]))+" -p "+str(float(tomoSeg_param[3]))+" "+tomo_name+"_tv2.rec "+tomo_name+"_Salient.rec")
 os.system("thresholding -l "+str(float(tomoSeg_param[4]))+" "+tomo_name+"_Salient.rec "+tomo_name+"_Salient_Threshold.rec")
 
# THE MAIN SCRIPT STARTS from here
sum_slices=1
annotate_images="yes"
scale_nm=100

parser=argparse.ArgumentParser(description='''Will take your tomogram and generate its tomosegmenTV segmented  slicer images across a range of input tomosegmemTV parameters. Choose the ones where the membrane segmentation is the best. Run as python scanForBest_tomosegmemTV.py -t tomo_name -a StartoftheRangeofTomosegmemTVParameters -d EndOftheRangeofTomosegmemTVParameters -n NumberofTomosegmemTVParametersbetweenTwoRanges. It needs the accompanying slicer_images.py script in the same folder ''', epilog="""For questions, contact at digvijay.in1 at gmail.com.""")

requiredNamed = parser.add_argument_group('Required arguments')
requiredNamed.add_argument('-t', '--tomo_name', help='Tomogram File (which should have .rec extension), but here pass the name without .rec extension', required=True)
requiredNamed.add_argument('-a', '--start', help='Start of TomoSegmenTV parameters you want to scan in this format: ridgeoredgelike#scale_space#surfaceness_threshold#saliency_filtering_threshold#OverallThreshold', required=True)
requiredNamed.add_argument('-b', '--end', help='End of TomoSegmenTV parameters you want to scan in this format: ridgeoredgelike#scale_space#surfaceness_threshold#saliency_filtering_threshold#OverallThreshold', required=True)
requiredNamed.add_argument('-n', '--n_steps', help='Number of steps between the start and end parameters', required=True)
args=parser.parse_args()


opts, args = getopt.gnu_getopt(sys.argv[1:], 't:a:b:n:',['tomo_name=', 'start=','end=','n_steps='])
for opt, arg in opts:
 if opt in ('-t', '--tomo_name'):
  tomo_name=arg
 elif opt in ('-a', '--start'):
  start=arg
 elif opt in ('-b', '--end'):
  end=arg
 elif opt in ('-n', '--n_steps'):
  n_steps=int(arg)

if os.path.isfile(tomo_name+".rec"):
 pix_size=calc_pixSize(tomo_name)
 start= [float(i) for i in start.split('#')]
 end= [float(i) for i in end.split('#')]
 ridgeoredgelike_range=np.linspace(start[0],end[0],n_steps)
 scaleSpace_range=np.linspace(start[1],end[1],n_steps)
 surfacenessThreshold_range=np.linspace(start[2],end[2],n_steps)
 saliency_range=np.linspace(start[3],end[3],n_steps)
 overallThreshold_range=np.linspace(start[4],end[4],n_steps)
 for i in range(n_steps):
  params=str(ridgeoredgelike_range[i])+"#"+str(scaleSpace_range[i])+"#"+str(surfacenessThreshold_range[i])+"#"+str(saliency_range[i])+"#"+str(overallThreshold_range[i])
  try:
   print(params.split('#'))
   tomoSegmemTV(tomo_name,params.split('#'),pix_size)
   slicer_images(tomo_name,params.split('#'),sum_slices,scale_nm,annotate_images,i)
  except Exception:
   pass
 os.system("newstack ./SegmemTVSlicers/*.tif Stack.mrc")
 os.system("mrc2tif -s Stack.mrc SegmentedStacks.tiff")
 if os.path.isfile("Stack.mrc"):
  os.remove("Stack.mrc")
 if os.path.exists("SegmemTVSlicers"):
  shutil.rmtree("SegmemTVSlicers")
