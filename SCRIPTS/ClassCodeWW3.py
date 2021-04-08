#!/home/cenciso/miniconda3/envs/pangeo/bin/python
# -*- coding:utf-8 -*-
#---------------------------------------------------------------------------
# Project: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS
# File: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS/downloadWW3.py
# @Author: Carlos Enciso Ojeda
# @Email: carlos.enciso.o@gmail.com
# @Created Date: Wednesday, April 7th 2021, 9:06:37 pm
# -----
# @Last Modified: Thursday, April 8th 2021 3:29:06 am
# Modified By: Carlos Enciso Ojeda at <carlos.enciso.o@gmail.com>
# -----
# Copyright (c) 2021 EyM GeoInsight Company
# @License: MIT
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
#---------------------------------------------------------------------------
import numpy as np
import pandas as pd
import xarray as xr
from datetime import datetime, timedelta
import os
#-------------------------------------#
# Adding decorator printing
#-------------------------------------#
def _decorator(func):
    def wrap(*args, **kwargs):
        print('#'+'-'*(len(*args)+2))
        func(*args)
        print('#'+'-'*(len(*args)+2))
    return wrap
@_decorator
def printing(msg):
    print('# '+msg)
#-------------------------------------#
# Downloader Func
#-------------------------------------#
def DownloadWW3(iDate,eDate,dirigrib=None):
  """
    Introduce initial and end dates to download dataset
    iDate: Initial Date in string format (YYYY-MM)
    eDate: End Date in string format(YYYY-MM)
  """
  #---- Range time ----#
  drg = pd.date_range(iDate,eDate,freq='1MS')
  #---- Setting parameters ----#
  main_url = ['https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase2/',
              'ftp://polar.ncep.noaa.gov/pub/history/waves/multi_1/']
  vars = ['dp','hs','tp']
  cname = ['multi_reanal.glo_30m_ext','multi_1.glo_30m']
  #---- Split daterange ----#
  for dts in drg:
    if dts < datetime(2010,1,1):
      urls=['{}{}/gribs/{}.{}.{}.grb2'.format(main_url[0],dts.strftime('%Y%m'),
                                            cname[0],v,dts.strftime('%Y%m')) for v in vars]
    elif dts >= datetime(2010,1,1) and dts <= datetime(2019,6,1):
      urls=['{}{}/gribs/{}.{}.{}.grb2'.format(main_url[1],dts.strftime('%Y%m'),
                                            cname[1],v,dts.strftime('%Y%m')) for v in vars]
    else:
      pass
    #---- Download----#
    try:
      print('Downloading...')
      _ = [os.system(f'wget -c -P {dirigrib} {x}') for x in urls]
    except:
      pass

if __name__ == '__main__':
    pass

#-------------------------------------#
# Downloader ASCII class
#-------------------------------------#
class WW3downloaderascii:
  #---- Parameters ----#
  vars=['Thgt','Tper','Tdir']
  pre_url='https://pae-paha.pacioos.hawaii.edu/thredds/dodsC/ww3_global/'
  def __init__(self,iDate=None,eDate=None,lat=None,lon=None,
               diriout=None,nameout=None,**kwargs):
    self.iDate = iDate; self.eDate=eDate
    nidays=datetime.strptime(iDate,'%Y-%m-%d')-datetime(2010,11,7)
    nedays=datetime.strptime(eDate,'%Y-%m-%d')-datetime(2010,11,7)
    ih=nidays.days*24+21; eh=nedays.days*24+42
    ilat=np.arange(-77.5,77.5,.5).tolist().index(lat)
    ilon=np.arange(0,359.5,.5).tolist().index(lon+180)
    url=[f'WaveWatch_III_Global_Wave_Model_best.ncd.ascii?lon%5B{ilon}%5D,',
         f'lat%5B{ilat}%5D,z%5B0:1:0%5D,time%5B{ih}:1:{eh}%5D,',
         f'Thgt%5B{ih}:1:{eh}%5D%5B0:1:0%5D%5B{ilat}%5D%5B{ilon}%5D,',
         f'Tper%5B{ih}:1:{eh}%5D%5B0:1:0%5D%5B{ilat}%5D%5B{ilon}%5D,',
         f'Tdir%5B{ih}:1:{eh}%5D%5B0:1:0%5D%5B{ilat}%5D%5B{ilon}%5D']
    self.lat=lat; self.lon=lon
    self.url=''.join(map(str, url))
    self.main_url=self.pre_url+self.url
    self.diriout=diriout
    self.nameout=nameout
    self.copyright = 'Carlos Enciso Ojeda'
    self.license = 'MIT@License'
  @property
  def downloadww3(self):
    print(self.main_url)
    try:
      os.system(f'wget -c -P {self.diriout} {self.main_url}')
    except:
      print('Something went wrong. Check it!')
      #---- Rename it ----#
    fili=[os.path.join(self.diriout,x) for x in os.listdir(self.diriout) \
          if self.url[:4] in x]
    os.rename(fili[0],self.diriout+self.nameout)
  def ascii2csv(self):
    #---- Converto CSV ----#
    with open(self.diriout+self.nameout,'r+') as f:
      file_lines=f.readlines()
      Lines=list(file_lines)
      #---- Looking for position ----#
      pos_vars = {k:[n for n,x in enumerate(Lines) if f'{k}.' in x][:2] for k in self.vars}
      contents = {k:Lines[v[0]:v[1]] for k,v in pos_vars.items()}
      contents = {k:list(map(float,list(filter(None,[x.strip('\n').split(',')[-1].strip() \
                                                     for x in v if k not in x])))) \
                                                     for k,v in contents.items()}
      self.df = pd.DataFrame.from_dict(contents)
      self.df['date'] = pd.date_range(self.iDate,self.eDate,freq='1H')
      self.df.set_index('date',inplace=True)
#----------------------
# Class PostProcess
#----------------------
class postWW3grb2:
  vars=['dp','hs','tp']
  def __init__(self,lat=None,lon=None,
               dirigrib=None,path_subset=None,):
    self.dirigrib=dirigrib
    self.path_subset=path_subset
    self.lat=lat; self.lon=lon 
  #---- Preprocesing vars & time----#
  def replacedtime(self,ds):
    ds = ds.drop(['time'])
    ds = ds.compute()
    ds['step'] = ds['valid_time']
    ds = ds.sel(step=~ds.get_index("step").duplicated())
    ds = ds.drop(['valid_time','surface'])
    return ds
  def subsetgrib(self,htype='multi_1'):
    self.dicfili={k:sorted([os.path.join(self.dirigrib,x) for x in os.listdir(self.dirigrib) \
      if k in x and htype in x and x.endswith('.grb2')]) for k in self.vars}
    dsdict={k:[xr.open_dataset(x,engine='cfgrib',decode_cf=False).sel(latitude=self.lat, 
                                                                      longitude=self.lon, 
                                                                      method='nearest', drop=True) \
              for x in v if k in x] for k,v in self.dicfili.items()}
    printing('Subseting to NetCDF!')
    for k in self.vars:
        for n,(i,l) in enumerate(zip(self.dicfili[k],dsdict[k])):
          pathi = self.path_subset+i.split('/')[-1][:-4]+'nc'
          print(f'Var: {k} | File: {n} | Saved File: {pathi}' )
          l.squeeze().to_netcdf(path=pathi) 
          
  def grb2tocsv(self,nameitcsv=None):
    self.nameitcsv=nameitcsv
    fili_subsets = {k:sorted([os.path.join(self.path_subset,x) for x in os.listdir(self.path_subset) \
                              if k in x and x.endswith('.nc')]) for k in self.vars}
    #---- Reading files using 10000 chunks using dask ----#
    dsmf_subsets = {k:xr.open_mfdataset(v,combine='nested',concat_dim='step',parallel=True,
                                        chunks={'step':10000}) for k,v in fili_subsets.items()}
    #---- Concating all variables and compute chunks ----#
    self.dsSubsetposhind = xr.merge([self.replacedtime(v) for v in dsmf_subsets.values()])
    #---- Saveing csv ----#
    self.dfSubsetposhind = self.dsSubsetposhind.to_dataframe()
    self.dfSubsetposhind.reset_index(inplace=True)
    self.dfSubsetposhind = self.dfSubsetposhind.rename(columns={'step':'date'})
    self.dfSubsetposhind.set_index('date',inplace=True)
    self.dfSubsetposhind.to_csv(self.nameitcsv)
#---------------------------------
# Funcs using my Downloader class
#---------------------------------
def downloadASCII(iDate=None,eDate=None,diri_ascii=None,ascii_name=None,
                  downloads=None,lat=None,lon=None):
  nmnths = np.diff(np.array([datetime.strptime(x,'%Y-%m-%d') \
                             for x in [iDate,eDate]]))[0]
  nmnths = nmnths.days/30
  nameit = f'{diri_ascii}{ascii_name}_lat_{lat}_lon_{lon}_{iDate}_to_{eDate}.csv'
  #---- For downloading  ----#
  if nmnths<=2:
    ww3 = WW3downloaderascii(iDate=iDate,eDate=eDate,lat=-14,
                             lon=-77,diriout=diri_ascii,nameout=ascii_name)
    if downloads==True:
      ww3.downloadww3
    ww3.ascii2csv()
    dfs=ww3.df
  else:
    idrg = pd.date_range(iDate,eDate,freq='1MS')
    edrg = pd.date_range(iDate,eDate,freq='1M')
    #---- Looping it 'cause it takes too much time if you want ----#
    #---- to retrieve data for more than one year ----#
    container=[]
    for i,e in zip(idrg,edrg):
      print(i.strftime('%Y-%m'))
      #---- Download ascii ----#
      ww3 = WW3downloaderascii(iDate=i.strftime('%Y-%m-%d'),
                               eDate=e.strftime('%Y-%m-%d'),
                               lat=lat,lon=lon,diriout=diri_ascii,
                               nameout=ascii_name)
      #---- May it takes its time depending the range time ----#
      if downloads==True:
        ww3.downloadww3
      ww3.ascii2csv()
      container.append(ww3.df)
    dfs=pd.concat(container)
    dfs=dfs.rename(columns={'Tdir':'dirpw','Tper':'perpw','Thgt':'swh'})
  try:
      dfs=dfs.resample('3H').mean()
      dfs.to_csv(nameit)
      print(f'Saving... {nameit}')
  except:
      pass
#---------------#
# Merging all 
#---------------#
def merging_all(outdiri=None,nameit=None):
  fili_csv = [os.path.join(outdiri,x) for x in os.listdir(outdiri) if x.endswith('.csv') \
              if 'Allmerged' not in x]
  dfcat = pd.concat([pd.read_csv(x) for x in fili_csv])
  dfcat.sort_values('date',inplace=True)
  dfcat['date']=pd.to_datetime(dfcat['date'],infer_datetime_format=True)
  dfcat.set_index('date',inplace=True)
  dfcat.to_csv(outdiri+nameit)
  return dfcat
def myheader(fili=None,mysign=None):
  with open(mysign,'r+') as f:
    file_lines=f.readlines()
    Lines=list(file_lines)
    nlns=len(Lines)
    f.close()
  with open(fili,'r+') as f:
    lines=f.readlines()
    nls=len(lines)
    f.seek(0)
    for n,l in enumerate(Lines):
      f.write(l) if n<nlns-1 else f.write(l+'\n')
    for line in lines:
      f.write(line)
    f.close()
# ---- Pass it ----#
if __name__ == '__main__':
    pass

