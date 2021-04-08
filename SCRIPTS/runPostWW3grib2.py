#!/home/cenciso/miniconda3/envs/pangeo/bin/python
# -*- coding:utf-8 -*-
#---------------------------------------------------------------------------
# Project: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS
# File: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS/runPostWW3grib2.py
# @Author: Carlos Enciso Ojeda
# @Email: carlos.enciso.o@gmail.com
# @Created Date: Wednesday, April 7th 2021, 10:59:50 pm
# -----
# @Last Modified: Thursday, April 8th 2021 1:24:58 am
# Modified By: Carlos Enciso Ojeda at <carlos.enciso.o@gmail.com>
# -----
# Copyright (c) 2021 EyM GeoInsight Company
# @License: MIT
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
#---------------------------------------------------------------------------
#-------------------------------------#
# Import modules 
#-------------------------------------#
from ClassCodeWW3 import postWW3grb2, printing
import os
#-------------------------------------#
# Main code 
#-------------------------------------#
#---- Using my class ----#
"""
    dirigrib: Directory where the grib2 files were Download
    path_subset: Directory where you want to save the subset processing files
    outdiri: Directory where you want to save the final processed file (csv format)
"""
dirigrib='../DATASET/GRIB2/'
path_subset='../DATASET/SUBSET/'
outdiri='../OUTPUT/'
os.makedirs(dirigrib, exist_ok=True)
os.makedirs(path_subset, exist_ok=True)
os.makedirs(outdiri, exist_ok=True)
ilat=-14
ilon=-77
nameit=outdiri+f'WW3_posthindcast_{ilat}S_{ilon}N.csv'
Subsetgrib2=False
until2005=True
post2005=True
postww3 = postWW3grb2(lat=ilat,lon=ilon,dirigrib=dirigrib,path_subset=path_subset)
#-------------------------------------#
# Take into account your period process 
#-------------------------------------#
if Subsetgrib2:
    if until2005:
        postww3.subsetgrib(htype='multi_reanal')
    if post2005:
        postww3.subsetgrib(htype='multi_1')
#-------------------------------------#
# Save it as csv
#-------------------------------------#
postww3.grb2tocsv(nameitcsv=nameit)
# Enjoy it!
printing('All processess has finish successfully!')

