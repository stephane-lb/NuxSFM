#!/usr/bin/python
#! -*- encoding: utf-8 -*-

#### Modify general settings before running the script!

# Low poly reconstruction with textured mesh from opemMVG suite results
#
# Easy use of openMVS for openMVG>=v0.8 
#
# v0, 11/09/2015, by Pierre-Yves ParanthoŽn < nuxsfm at you know gmail dot com >
#
# Script is heavily inpired by @vins31 & Pierre Moulon openMVG-0.8 python scripts to keep their logic and use.
# It has to be run AFTER SfM_GlobalPipeline.py or SfM_SequentialPipeline.py
#
# usage : python mvg2mvs.py input_dir output_dir. e.g: mvg2mvs.py /home/dataset /home/dataset/OUT/MVS
#
# input_dir is the directory of openMVG saved project. (reconstruction_[sequential][global]/sfm_data.json is located)
# output_dir is the directory where openMVS will save its work.


# uncomment next line if running python2, else python3 is assumed (default) and have to be commented in. Also assumed an existing symlink to default interpreter (eg /usr/bin/python to /usr/bin/python3). Or user env. var.
#import commands
import os
import subprocess
import sys
import re

# General settings to be changed to suit your needs
# 
## Indicate the openMVG and CMVS/PMVS binaries directory.
OPENMVG_BINS = "/usr/local/bin"
OPENMVS_BINS = "/usr/local/bin"
#
# OpenMVG reconstruction type. "reconstruction_sequential" or "reconstruction_global". Sequential is default. To be changed if GlobalPipeline was used.
reconstruction_type = "reconstruction_sequential"
#

# Run openMVG to openMVS pipeline
# given argument test
if len(sys.argv) < 3:
    print ("Usage %s input_dir output_dir" % sys.argv[0])
    sys.exit(1)
        
# openMVG reconstruction dir.
input_dir = sys.argv[1]
# openMVS output dir
output_dir = sys.argv[2]

# Reconstruction type dir
reconstruction_dir = os.path.join(input_dir, reconstruction_type)
print ("You gave:", "input_dir=", reconstruction_dir, "output_dir=", output_dir)

# Create the ouput_dir folder if it does not exist
if not os.path.exists(output_dir):
  os.mkdir(output_dir)

# todo: add a test here to check presence of input_dir or openMVG results

# STEP 1
# Import Scene from OpenMVG
print ("1. running openMVG2PMVS")
popenMVG2MVS = subprocess.Popen( [os.path.join(OPENMVG_BINS, "InterfaceOpenMVG"), "-i", reconstruction_dir+"/sfm_data.json", "-o", output_dir+"/scene.mvs"] )
popenMVG2MVS.wait()

# STEP 2
# Rough Mesh Reconstruction from non densifyied point cloud.
print ("3. Rough Mesh Reconstruction from non densifyied point cloud.")
popenMVG2MVS = subprocess.Popen( [os.path.join(OPENMVG_BINS, "ReconstructMesh"), output_dir+"/scene.mvs"] )
popenMVG2MVS.wait()

# STEP 3
# Mesh Refinement (optional)
print ("4. RefineMesh from non dense scene")
popenMVG2MVS = subprocess.Popen( [os.path.join(OPENMVG_BINS, "RefineMesh"), output_dir+"/scene_mesh.mvs"] )
popenMVG2MVS.wait()

# STEP 4 
# Mesh Texturing
print ("5. Mesh Texturing")
popenMVG2MVS = subprocess.Popen( [os.path.join(OPENMVG_BINS, "TextureMesh"), output_dir+"/scene_mesh.mvs"] )
popenMVG2MVS.wait()

