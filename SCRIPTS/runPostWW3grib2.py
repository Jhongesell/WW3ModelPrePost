#!/home/cenciso/miniconda3/envs/pangeo/bin/python
# -*- coding:utf-8 -*-
#---------------------------------------------------------------------------
# Project: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS
# File: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS/runPostWW3grib2.py
# @Author: Carlos Enciso Ojeda
# @Email: carlos.enciso.o@gmail.com
# @Created Date: Wednesday, April 7th 2021, 10:59:50 pm
# -----
# @Last Modified: Wednesday, April 14th 2021 4:38:30 pm
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
dirigrib='../DATASETS/GRIB2/'
path_subset='../DATASETS/netCDF/'
ilat=int(input('Ingrese Latitud (WGS84 coords): '))
ilon=int(input('Ingrese Longitud (WGS84 coords): '))
nameit=f'Dataset_postGrib2_lat_{ilat}_lon_{ilon}.csv'
postww3 = postWW3grb2(lat=ilat,lon=ilon,poshindsubsets=True,
                      dirigrib=dirigrib,path_subset=path_subset)
postww3.poshindcastgrb2(nameitcsv=nameit)
# Enjoy it!
printing('All processess has finish successfully!')

