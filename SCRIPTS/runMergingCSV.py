#!/home/cenciso/miniconda3/envs/pangeo/bin/python
# -*- coding:utf-8 -*-
#---------------------------------------------------------------------------
# Project: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS
# File: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS/runMergingCSV.py
# @Author: Carlos Enciso Ojeda
# @Email: carlos.enciso.o@gmail.com
# @Created Date: Thursday, April 8th 2021, 1:03:21 am
# -----
# @Last Modified: Thursday, April 8th 2021 1:25:34 am
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
from ClassCodeWW3 import merging_all, myheader, printing
#-------------------------------------#
# Main code 
#-------------------------------------#
outdiri='../OUTPUT/'
os.makedirs(outdiri, exist_ok=True)
nameit='WW3_Allmerged_dataset.csv'
merging_all(outdiri=outdiri,nameit=nameit)
#---- Writting my header ----#
mysign='../HEADER/mysign'
fili=outdiri+nameit
myheader(fili=fili,mysign=mysign)
# Enjoy it!
printing('All processess has finish successfully!')