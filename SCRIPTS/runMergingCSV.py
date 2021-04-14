#!/home/cenciso/miniconda3/envs/pangeo/bin/python
# -*- coding:utf-8 -*-
#---------------------------------------------------------------------------
# Project: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS
# File: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS/runMergingCSV.py
# @Author: Carlos Enciso Ojeda
# @Email: carlos.enciso.o@gmail.com
# @Created Date: Thursday, April 8th 2021, 1:03:21 am
# -----
# @Last Modified: Wednesday, April 14th 2021 4:42:46 pm
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
import os
#-------------------------------------#
# Main code 
#-------------------------------------#
#---- Merging all CSV ----#
outdiri='../OUTPUT/'
nameit='WW3_Allmerged_dataset.csv'
merging_all(outdiri=outdiri,nameit=nameit)
#---- Writting my header ----#
myheader(outdiri=outdiri,nameit=nameit)
# Enjoy it!
printing('All processess has finish successfully!')