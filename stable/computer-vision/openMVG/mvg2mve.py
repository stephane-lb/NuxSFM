#!/usr/bin/python
#! -*- encoding: utf-8 -*-

#### Modify general settings before running the script!

# Multi-View Environment and Floating Scale Surface Reconstruction (MVE/FSSR) script for openMVG
#
# v0:initiation, 05/20/2015, by Pierre-Yves Paranthoën < py.paranthoen at you know gmail dot com >
#
# Script is heavily inpired by @vins31 & Pierre Moulon openMVG-0.8 python scripts to keep their logic and use.
# It has to be run AFTER SfM_GlobalPipeline.py or SfM_SequentialPipeline.py
#
# usage : python mvg2mve.py input_dir output_dir e.g. python mvg2mve.py /home/dataset /home/dataset
#
# input_dir is the directory of openMVG saved project. (the dirs where matches, reconstruction_sequential are located)
# output_dir is the directory where MVE will save its results. It creates automaticaly a MVE subdir into the output_dir.
# If output_dir is not present script will create it.


# uncomment next line if running python3, else python2 is assumed (default) and have to be commented in. Also assumed an existing symlink to default interpreter (eg /usr/bin/python to /usr/bin/python3). Or user env. var.
#import commands
import os
import subprocess
import sys
import re

# General settings to be changed to suit your needs
# 
## Indicate the openMVG, mve and fssr binaries directory.
BINS = "/usr/local/bin"
#
# OpenMVG reconstruction type. "reconstruction_sequential" or "reconstruction_global". Sequential is default.
reconstruction_type = "reconstruction_sequential"
#
## MVE settings
#
# Scale reconsruction. 2 is default
scale="-s2"
# 
# Huge point cloud settings.
# -d argument specifies the depth map to use, -i specifies the color image to color the point cloud, -n -c -s instructs the application to also generate normals, confidences and scale values for every sample
# hugePCsettings="-ddepth-L2 -iundist-L2 -n -c -s"
hugePCsettings="-F1"
# Mesh cleaning
threshold=10


# Given argument test
if len(sys.argv) < 3:
    print ("Usage %s input_dir output_dir" % sys.argv[0])
    sys.exit(1)

# openMVG reconstruction dir.
input_dir = sys.argv[1]
# mve output dir
output_dir = sys.argv[2]

# Create the ouput_dir folder if ir does not exist
if not os.path.exists(output_dir):
  os.mkdir(output_dir)

# Final arguments given
reconstruction_dir = os.path.join(input_dir, reconstruction_type)
print ("You gave:", "input_dir=", reconstruction_dir, "output_dir=", output_dir)


## Run MVE pipeline

# STEP 1
print ("1. openMVG2MVE2: Convert the openMVG SfM scene to the MVE format")
#popenMVG2MVE = subprocess.Popen( [os.path.join(BINS, "openMVG_main_openMVG2MVE2"), "-i", reconstruction_dir+"/sfm_data.json", "-o", output_dir] )
#popenMVG2MVE.wait()

# STEP 2
print ("2. dmrecon: Depth map reconstruction")
#pDmrecon = subprocess.Popen( [os.path.join(BINS, "dmrecon"), scale, output_dir+"/MVE" ] )
#pDmrecon.wait()

# STEP 3
print ("3. scene2pset: Huge point cloud creation")
#pScene2pset = subprocess.Popen( [os.path.join(BINS, "scene2pset"), hugePCsettings, output_dir+"/MVE", output_dir+"/MVE/pset-L2.ply" ] )
#pScene2pset.wait()

# STEP 5
print ("4. fssrecon: Floating Scale Surface Reconstruction")
pFssrecon = subprocess.Popen( [os.path.join(BINS, "fssrecon"), output_dir+"/MVE/pset-L2.ply", output_dir+"/MVE/surface-L2.ply"] )
pFssrecon.wait()

# STEP 5
print ("5. meshclean: Mesh cleaning")
pMeshclean = subprocess.Popen( [os.path.join(BINS, "meshclean"), threshold, output_dir+"/MVE/surface-L2.ply", output_dir+"/MVE/surface-L2-clean.ply"] )
pMeshclean.wait()

