#!/home/cenciso/miniconda3/envs/pangeo/bin/python
# -*- coding:utf-8 -*-
#---------------------------------------------------------------------------
# Project: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS
# File: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS/runPostWW3grib2.py
# @Author: Carlos Enciso Ojeda
# @Email: carlos.enciso.o@gmail.com
# @Created Date: Wednesday, April 7th 2021, 10:59:50 pm
# -----
# @Last Modified: Thursday, April 8th 2021 2:57:16 am
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
ilat=int(input('Ingrese Latitud (WGS84 coords): '))
ilon=int(input('Ingrese Longitud (WGS84 coords): '))
nameit=outdiri+f'WW3_posthindcast_{ilat}S_{ilon}N.csv'
postww3 = postWW3grb2(lat=ilat,lon=ilon,dirigrib=dirigrib,path_subset=path_subset)
#-------------------------------------#
# Take into account your period process 
#-------------------------------------#
printing('Obteniendo Parametros')
Subsetgrib2=input('Quiere realizar el subset (dependiendo de la cantidad puede tomar tiempo)? (Si: 1 | No: 0): ')
if Subsetgrib2:
    until2009=input('Quiere realizar el subset de archivos comprendidos entre 1979-2009? (Si: 1 | No: 0): ')
    post2009=input('Quiere realizar el subset de archivos del 2010? (Si: 1 | No: 0): ')
    if until2009:
        postww3.subsetgrib(htype='multi_reanal')
    if post2009:
        postww3.subsetgrib(htype='multi_1')
#-------------------------------------#
# Save it as csv
#-------------------------------------#
postww3.grb2tocsv(nameitcsv=nameit)
# Enjoy it!
printing('All processess has finish successfully!')

