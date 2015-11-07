#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# v1 : MVE2 support, october 2015

#### Modify general settings before running the script!

# Multi-View Environment and Floating Scale Surface Reconstruction (MVE/FSSR) script for openMVG
#
# v0:initiation, 05/20/2015, by Pierre-Yves Paranthoen < nuxsfm at you know gmail dot com >
#
# Script is heavily inpired by @vins31 & Pierre Moulon openMVG-0.8 python scripts to keep the logic and use.
# It has to be run AFTER SfM_GlobalPipeline.py or SfM_SequentialPipeline.py
#
# usage : python mvg2mve.py input_dir output_dir e.g. python mvg2mve.py /home/dataset/images /home/dataset/mve
#
# input_dir is the directory of openMVG saved project. (the dirs where matches, reconstruction_sequential are located)
# output_dir is the directory where MVE will save its results. 
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
OPENMVG_SFM_BIN = "/usr/local/bin"
CMVS_SFM_BIN = "/usr/local/bin"
#
# OpenMVG reconstruction type. "reconstruction_sequential" or "reconstruction_global". Sequential is default.
reconstruction_type = "reconstruction_sequential"
#
## MVE settings
#
# Scale reconsruction. 2 is default
Scale=2
# 
# Huge point cloud settings.
# -d argument specifies the depth map to use, -i specifies the color image to color the point cloud, -n -c -s instructs the application to also generate normals, confidences and scale values for every sample
hugePCsettings="-ddepth-L2 -iundist-L2 -n -c -s"

# Run openMVG2MVE2 and MVE2 pipeline

# given argument test
if len(sys.argv) < 3:
    print ("Usage %s input_dir output_dir" % sys.argv[0])
    sys.exit(1)

# openMVG reconstruction dir.
input_dir = sys.argv[1]
# mve output dir
output_dir = sys.argv[2]

# Create the ouput_dir folder if ir does not exist
#if not os.path.exists(output_dir):
#  os.mkdir(output_dir)

# Print out final arguments given
reconstruction_dir = os.path.join(input_dir, reconstruction_type)
print ("You gave:", "input_dir=", reconstruction_dir, "output_dir=", output_dir)


## Run MVE pipeline

# STEP 1
# MVE scene creation
print ("1. makescene: Multi View Scene creation")
popenMVG2PMVS = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "makescene"), reconstruction_dir, output_dir ] )
popenMVG2PMVS.wait()

# STEP 2
# Depth map reconstruction
print ("2. dmrecon: Depth map reconstruction")
pClustering = subprocess.Popen( [os.path.join(CMVS_SFM_BIN, "dmrecon"), Scale, output_dir ] )
pClustering.wait()

# STEP 3
# Huge point cloud creation
print ("3. scene2pset: Huge point cloud creation")
pOpt = subprocess.Popen( [os.path.join(CMVS_SFM_BIN, "scene2pset"), hugePCsettings, output_dir+"OUTPUT.ply" ] )
pOpt.wait()

# STEP 4
# Floating Scale Surface Reconstruction
print ("4. fssrecon: Floating Scale Surface Reconstruction")
pDense = subprocess.Popen( [os.path.join(CMVS_SFM_BIN, "fssrecon"), output_dir+"OUTPUT.ply", output_dir+"OUTPUT_fssr.ply"] )
pDense.wait()

# STEP 5
# Mesh cleaning
print ("5. meshclean: Mesh cleaning")
pDense = subprocess.Popen( [os.path.join(CMVS_SFM_BIN, "fssrecon"), output_dir+"OUTPUT_fssr.ply", output_dir+"final_mesh.ply"] )
pDense.wait()

