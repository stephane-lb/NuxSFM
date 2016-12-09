#!/usr/bin/python
#! -*- encoding: utf-8 -*-

#### Modify general settings before running the script!

# Dense reconstruction from opemMVG suite results
#
# Easy use of pmvs/cmvs for openMVG-v0.8 "Paracheirodon simulans" 
#
# v0, 05/20/2015, by Pierre-Yves Paranthoen < nuxsfm at you know gmail dot com >
#
# Script is heavily inpired by @vins31 & Pierre Moulon openMVG-0.8 python scripts to keep their logic and use.
# It has to be run AFTER SfM_GlobalPipeline.py or SfM_SequentialPipeline.py
#
# usage : python mvg2pmvs.py input_dir output_dir
#
# input_dir is the directory of openMVG saved project. (the dirs where matches, reconstruction_sequential are located)
# output_dir is the directory where cmvs/pmvs will save their results. The subdirectory $output_dir/PMVS/models will contain the final dense reconstruction file (option-xxxx.ply)


# uncomment next line if running python2, else python3 is assumed (default) and have to be commented in. Also assumed an existing symlink to default interpreter (eg /usr/bin/python to /usr/bin/python3). Or user env. var.
#import commands
import os
import subprocess
import sys
import re

# General settings to be changed to suit your needs
# 
## Indicate the openMVG and CMVS/PMVS binaries directory.
OPENMVG_SFM_BIN = "/usr/local/bin"
CMVS_SFM_BIN = "/usr/local/bin"
#
# OpenMVG reconstruction type. "reconstruction_sequential" or "reconstruction_global". Sequential is default.
reconstruction_type = "reconstruction_sequential"
#
## Number of available CPU cores you'd like to use
maxCPU=8
#
## Number of max image series you'd like to use for CMVS
maxImages=10
#
## CMVS settings
# Exploit camera parameters Visdatas (0 or 1)
useVisData=1
#
# Image resolution: full resolution is 0, halved resolution is 1 (4 times less pixels), 2 is 4 times smaller (or 16 times less pixels)
level=1
#
# Density of reconstructions.
csize=2
#
# A patch reconstruction is accepted as a success and kept, if its associcated photometric consistency measure is above this threshold. 
# Normalized cross correlation is used as a photometric consistency measure, whose value ranges from -1 (bad) to 1 (good).
threshold=0.7
#
# Sample wsize x wsize pixel colors from each image to compute photometric consistency score.
# For example, when wsize=7, 7x7=49 pixel colors are sampled in each image.
# Increasing the value leads to more stable reconstructions, but the program runs slower.
wsize=7
#
# Each 3D point must be visible in at least minImageNum images for being reconstructed. 
# 3 is suggested in general. The software works fairly well with minImageNum=2, but you may get false 3D points where there are only weak texture information. 
# On the other hand, if your images do not have good textures, you may want to increase this value to 4 or 5.
minImageNum=3

# Run openMVG2PMVS/cmvs/pmvs pipeline
# given argument test
if len(sys.argv) < 3:
    print ("Usage %s input_dir output_dir" % sys.argv[0])
    sys.exit(1)
        
# openMVG reconstruction dir.
input_dir = sys.argv[1]
# cmvs/pmvs output dir
output_dir = sys.argv[2]

# Reconstruction type dir
reconstruction_dir = os.path.join(input_dir, reconstruction_type)
print ("You gave:", "input_dir=", reconstruction_dir, "output_dir=", output_dir)

# todo: add a test here to check presence of input_dir or openMVG results

# STEP 1
# openMVG2PMVS run: exports openMVG datas to cmvs/pmvs format.
print ("1. running openMVG2PMVS")
popenMVG2PMVS = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2PMVS"), "-c", str(maxCPU), "-v", str(useVisData), "-i", reconstruction_dir+"/sfm_data.json", "-o", output_dir] )
popenMVG2PMVS.wait()

# STEP 2
# CMVS run: decomposes the input images into a set of image clusters of managable size.
print ("2. running Clustering Views for Multi-view Stereo")
pClustering = subprocess.Popen( [os.path.join(CMVS_SFM_BIN, "cmvs"), output_dir+"/PMVS/", str(maxImages), str(maxCPU) ] )
pClustering.wait()

# STEP 3
# PMVS2 genOption run: generate clustered images option files for pmvs.
print ("3. Generating Clustered Images option files")
pOpt = subprocess.Popen( [os.path.join(CMVS_SFM_BIN, "genOption"), output_dir+"/PMVS/", str(level), str(csize), str(threshold), str(wsize), str(minImageNum), str(maxCPU) ] )
pOpt.wait()

# STEP 4
# PMVS2 pmvs2 run: dense reconstruction
print ("4. running Dense reconstruction")
pDense = subprocess.Popen( [os.path.join(CMVS_SFM_BIN, "pmvs2"), output_dir+"/PMVS/"] )
pDense.wait()

# Find all option-xxx files and process them.
for files in os.listdir(output_dir+"/PMVS/"):
   if re.match('option', files):
          print (files)
          pDense = subprocess.Popen( [os.path.join(CMVS_SFM_BIN, "pmvs2"), output_dir+"/PMVS/", files] )
          pDense.wait()