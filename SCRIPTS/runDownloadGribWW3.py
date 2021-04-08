#!/home/cenciso/miniconda3/envs/pangeo/bin/python
# -*- coding:utf-8 -*-
#---------------------------------------------------------------------------
# Project: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS
# File: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS/runDownloadGribWW3.py
# @Author: Carlos Enciso Ojeda
# @Email: carlos.enciso.o@gmail.com
# @Created Date: Wednesday, April 7th 2021, 9:14:57 pm
# -----
# @Last Modified: Thursday, April 8th 2021 3:43:51 am
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
printing('Obteniendo Parametros')
#---- Taking options ----#
if int(input('Quiere descargar datos del periodo hindcast 1979-2010? (Si: 1 | No: 0): ')):
    dirigrib='../DATASET/GRIB2/'
    os.makedirs(dirigrib, exist_ok=True)
    iDate=input('Ingrese Fecha Inicial de Descarga (YYYY-mm format): ')
    eDate=input('Ingrese Fecha Inicial de Descarga (YYYY-mm format): ')
    DownloadWW3(iDate,eDate,dirigrib=dirigrib)
printing('Obteniendo Parametros') 
if int(input('Quiere descargar datos del periodo post-hindcast 2011-2021? (Si: 1 | No: 0): ')):
    #---- Using my class ----#
    printing('Obteniendo Parametros')
    diri_ascii='../OUTPUT/'
    os.makedirs(diri_ascii, exist_ok=True)
    ascii_name='WW3ascii'
    ilat=int(input('Ingrese Latitud (WGS84 coords): '))
    ilon=int(input('Ingrese Longitud (WGS84 coords): '))
    iDate=input('Ingrese Fecha Inicial de Descarga (YYYY-mm-01 format): ')
    eDate=input('Ingrese Fecha Inicial de Descarga (YYYY-mm-dd format): ')
    downloadASCII(iDate=iDate,eDate=eDate,diri_ascii=diri_ascii,ascii_name=ascii_name,
                  downloads=True,lat=ilat,lon=ilon)
# Enjoy it!
printing('All processess has finish successfully!')