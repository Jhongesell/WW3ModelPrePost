#!/home/cenciso/miniconda3/envs/pangeo/bin/python
# -*- coding:utf-8 -*-
#---------------------------------------------------------------------------
# Project: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS
# File: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS/runDownloadGribWW3.py
# @Author: Carlos Enciso Ojeda
# @Email: carlos.enciso.o@gmail.com
# @Created Date: Wednesday, April 7th 2021, 9:14:57 pm
# -----
# @Last Modified: Thursday, April 8th 2021 1:24:40 am
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
from ClassCodeWW3 import DownloadWW3, downloadASCII, printing
import os
#-------------------------------------#
# Main code 
#-------------------------------------#
#---- Important Inquiry ----#
downloadgrib, downloadascii = True,False
#---- Taking options ----#
if downloadgrib:
    dirigrib='../DATASET/GRIB2/'
    os.makedirs(dirigrib, exist_ok=True)
    DownloadWW3('2004-01','2004-03',dirigrib=dirigrib) 
if downloadascii:
    #---- Using my class ----#
    diri_ascii='../OUTPUT/'
    os.makedirs(diri_ascii, exist_ok=True)
    ascii_name='WW3ascii'
    ilat=-14
    ilon=-77
    iDate='2021-01-01'
    eDate='2021-02-01'
    downloadASCII(iDate=iDate,eDate=eDate,diri_ascii=diri_ascii,ascii_name=ascii_name,
                  downloads=True,lat=ilat,lon=ilon)
# Enjoy it!
printing('All processess has finish successfully!')