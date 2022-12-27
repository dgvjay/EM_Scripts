# Introduction
A collection of scripts that I use to help process my cryo-electron tomography data.  I am starting this repository with only a handful of scripts; I will continue to add more. Most of these are wrapper scripts that rely on other programs and scripts

# How to use
The description for the usage of each script can be found in its commented header or with the -h flag when running them (if Python script). An incomplete list of description for each script is the following:

## average_neighboringSlices.py
This script will take a tomogram as input and generate a new one where every slice is an average of the n (also input) slices. This may be useful to generate tomograms for visualization software like Amira, where the option to average neighboring slices is not present. 

## massNormalize_mdoc.py
This script will nornalize (i.e. offset by PreTilt Zero angle) tilt angles in all mdocs in the input folder (input with -d with a slash at end) and generate a new folder called Adjusted containing new mdocs with normalized tilt angles. which can then be directly used in WARP & other software. 
Using the adjusted mdocs in WARP & other software will generate a nearly ‘Flattened’ tomo which makes it easier to visualize tomos and pick particles and define filaments or membrane geometries.

## visualize_mDoc.py
This script will parse all the mdoc files present in the input directory (input with -d with \ at end) and generate plots summarizing various attributes of the mdoc files. This visualization can be used to see if the tilt-series was acquired properly with proper exposure and tilt-angle distribution (in negative & positive sides).

## scanForBest_tomosegmemTV.py
TomoSegmemTV is an excellent program for membrane segmentation in tomograms. It uses a lot of parameters and it can take a long time to optimize the right set of parameters most suitable for your tomograms. So this script will automate this optimization, it will take your tomogram and generate its tomosegmenTV segmented slicer images across a range of input tomosegmemTV parameters. Choose the ones where the membrane segmentation is the best. Run as python scanForBest_tomosegmemTV.py -t tomo_name -a StartoftheRangeofTomosegmemTVParameters -d EndOftheRangeofTomosegmemTVParameters -n NumberofTomosegmemTVParametersbetweenTwoRanges. It needs the accompanying slicer_images.py script in the same folder. I have not tested this script in a long time, so you may have to do some debugging if it does not work straight away. But the script is quite simple, so you should be able to debug easily. 

## batchAreTomo_reconstruction.py
This script will batch AreTomo reconstruct tilt-series present inside each of the sub-directory in the WARP generated IMOD directory (input in -t with / at end). After batch reconstruction, the reconstruction parameters can be read by WARP like IMOD, because .xf files are generated. AreTomo parameters of reconstruction can be changed by changing parameters in the are_string below

## batchConvert_json_to_tbls.py
I really like EMAN2's e2spt_boxer for particle picking. This program ill batch read all EMAN2's json file (they should have boxes_3d in them) in the input directory (-d with \ end) and read the coordinates from it and convert it into Dynamo's .tbl. This dynamo style .tbl can be converted into .star using Alister Burt's dynamo2m. A wrapper for batch converting tbls to starfile is also present in this repository. Please batchConvert_tbls_to_stars.py

## batchConvert_stars_to_tbls.py
This script will batch convert all Relion3.0 star file in the input directory (input in -d with / at end) using Alister Burt's dynamo2m function, so warp2dynamo should be in your path

## batchConvert_tbls_to_stars.py
This script will batch convert all Dynamo tbls in the input directory (input in -t with / at end) using Alister Burt's dynamo2m function, so dynamo2warp2 should be in your path

## batchReconstruction_Relion4.py
This script will batch reconstruct tomograms in Relion4 project based on the input of the tomograms.star file, input of the prefix of tomograms in your project and input of the range of tomograms to reconstructio. Pass only -h flag with no input for help

## combine_starfiles.py
This script will batch read all Relion 3.0 style star files into the input directory (input with -d with \ at end) using Alister Burt's starfile into panda dataframes and combine them all to a combined star file

## localRes_EMAN.py
This script will calculate local resolution between two half maps using the input box size using EMAN2's e2fsc_real_local.py

# License & terms of use
All the materials are free to use: you can redistribute it and/or modify it under the terms of the GNU General Public License. The licenses/terms of use for other programs that these scripts uses can be found in their original sources. 
