#!/home/cenciso/miniconda3/envs/pangeo/bin/python
# -*- coding:utf-8 -*-
#---------------------------------------------------------------------------
# Project: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS
# File: /home/cenciso/Documents/CONSULTING/WW/SCRIPTS/downloadWW3.py
# @Author: Carlos Enciso Ojeda
# @Email: carlos.enciso.o@gmail.com
# @Created Date: Wednesday, April 7th 2021, 9:06:37 pm
# -----
# @Last Modified: Wednesday, April 14th 2021 4:37:37 pm
# Modified By: Carlos Enciso Ojeda at <carlos.enciso.o@gmail.com>
# -----
# Copyright (c) 2021 EyM GeoInsight Company
# @License: MIT
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
#---------------------------------------------------------------------------
import xarray as xr
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from dask.diagnostics import ProgressBar
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
#---- Downloaders ----#
class WW3downloaderascii:
  #---- Parameters ----#
  vars=['Thgt','Tper','Tdir']
  pre_url='https://pae-paha.pacioos.hawaii.edu/thredds/dodsC/ww3_global/'
  def __init__(self,iDate=None,eDate=None,lat=None,lon=None,
               diriout=None,nameout=None,**kwargs):
    self.iDate = iDate; self.eDate=eDate
    nidays=datetime.strptime(iDate,'%Y-%m-%d')-datetime(2010,11,7)
    nedays=datetime.strptime(eDate,'%Y-%m-%d')+timedelta(1)-datetime(2010,11,7)
    ih=nidays.days*24+21; eh=nedays.days*24+21+23
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
      self.df['date'] = pd.date_range(self.iDate,periods=len(self.df),freq='1H')
      self.df.set_index('date',inplace=True)
      self.df=self.df.rename(columns={'Tdir':'dirpw','Tper':'perpw','Thgt':'swh'})
#----------------------
# Funcs using my class
#----------------------
def downloadASCII(iDate=None,eDate=None,diri_ascii=None,ascii_name=None,
                  downloads=None,lat=None,lon=None):
  os.makedirs(diri_ascii, exist_ok=True)
  os.makedirs('../OUTPUT/', exist_ok=True)
  nmnths = np.diff(np.array([datetime.strptime(x,'%Y-%m-%d') \
                             for x in [iDate,eDate]]))[0]
  nmnths = nmnths.days/30
  nameit = f'../OUTPUT/Dataset_lat_{lat}_lon_{lon}_{iDate}_to_{eDate}.csv'
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
  try:
      dfs.to_csv(nameit)
      print(f'Saveing... {nameit}')
  except:
      pass
#---- Grib Funcs ----#
def DownloadWW3(iDate,eDate,dirigrib=None):
  """
    Introduce initial and end dates to download dataset
    iDate: Initial Date in string format (YYYY-MM)
    eDate: End Date in string format(YYYY-MM)
  """
  os.makedirs(dirigrib, exist_ok=True)
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
      print(urls)
      _ = [os.system(f'wget -c -P {dirigrib} {x}') for x in urls]
    except:
      pass
class postWW3grb2:
  vars=['dp','hs','tp']
  def __init__(self,lat=None,lon=None, poshindsubsets=False,
               dirigrib=None,path_subset=None,):
    self.dirigrib=dirigrib
    self.path_subset=path_subset
    os.makedirs(self.path_subset, exist_ok=True)
    self.lat=lat; self.lon=lon+180 
    self.poshindsubsets=poshindsubsets
  #---- Preprocesing vars & time----#
  def replacedtime(self,ds):
    ds = ds.drop(['time'])
    ds = ds.compute()
    ds['step'] = ds['valid_time']
    ds = ds.sel(step=~ds.get_index("step").duplicated())
    ds = ds.drop(['valid_time','surface'])
    return ds
  def poshindcastgrb2(self,htype='multi_',nameitnc='concated_',nameitcsv=None,nchunks=1000):
    self.nameitnc=f'{nameitnc}_lat_{self.lat}_lon_{self.lon}.nc'
    self.nameitcsv=f'../OUTPUT/{nameitcsv}'
    if self.poshindsubsets:
      self.dicfili={k:sorted([os.path.join(self.dirigrib,x) for x in os.listdir(self.dirigrib) \
                              if k in x and htype in x and x.endswith('.grb2')]) for k in self.vars}
      dsdict={k:xr.open_mfdataset(v,combine='by_coords',concat_dim='time',preprocess=prepross,parallel=True,
                                  chunks={'step':10000},engine='cfgrib') for k,v in self.dicfili.items()}
      dsmf=xr.merge([v for v in dsdict.values()])
      dsmf_rechunk = dsmf.chunk({'time':nchunks})
      #---- Writing chunks ----#
      print(f'Saving File: {self.path_subset+self.nameitnc}' )
      delayed_obj = dsmf_rechunk.to_netcdf(self.path_subset+self.nameitnc, compute=False)
      with ProgressBar():
        results = delayed_obj.compute()
    fili_subsets = [os.path.join(self.path_subset,x) for x in os.listdir(self.path_subset) if x.endswith('.nc') and self.nameitnc in x]
    ds = xr.open_mfdataset(fili_subsets)
    ds = ds.rename({'time':'date'})
    df = ds.to_dataframe()
    df = df.drop(columns=['latitude','longitude'])
    df = df[~df.index.duplicated()]
    df.sort_index(inplace=True)
    df.to_csv(self.nameitcsv)
#---- Merging all Dataset ----#
def merging_all(outdiri='../OUTPUT/',nameit=None):
  fili_csv = [os.path.join(outdiri,x) for x in os.listdir(outdiri) if x.endswith('.csv') and 'Dataset' in x]
  dfcat = pd.concat([pd.read_csv(x) for x in fili_csv])
  dfcat.sort_values('date',inplace=True)
  dfcat['date']=pd.to_datetime(dfcat['date'],infer_datetime_format=True)
  dfcat.set_index('date',inplace=True)
  dfcat = dfcat.resample('3H').mean()
  dfcat = dfcat.round(3)
  dfcat.to_csv(outdiri+nameit)
  return dfcat
def myheader(outdiri='../OUTPUT/',nameit=None):
  Lines = ['#'+'-'*80,
           '# -*- coding:utf-8 -*-',
           '# %Project       : Pisco Project WW3',
           '# %Author       : Carlos Enciso Ojeda',
           '# %Email        : carlos.enciso.o@gmail.com',
           '# %Created Date : Tuesday, April 03th 2021, 12:22:40 am',
           '# %Copyright (c): 2021 EyM GeoInsight',
           '# %License      : MIT',
           '#------------#','# Parameters:','#------------#',
           '# .swh.   = significant height of combined wind waves and swell (m)',
           '# .perpw. = primary wave mean period (s)',
           '# .dirpw. = primary wave direction',
           '# (degrees true, i.e. 0 deg => coming from North; 90 deg => coming from East)',
           '#--------------------------------------------------------------------------------']
  nlns=len(Lines)
  with open(outdiri+nameit,'r+') as f:
    lines=f.readlines()
    nls=len(lines)
    f.seek(0)
    for n,l in enumerate(Lines):
      f.write(l+'\n')
    for line in lines:
      f.write(line)
    f.close()
#--------------- Dont touch this ---------------#
def prepross(ds,lat=-14,lon=-77):
    ds['step']=ds['time']+ds['step']
    ds=ds.drop(['time','valid_time','surface'])
    ds=ds.rename({'step':'time'})
    ds=ds.sel(latitude=lat,longitude=lon+180)
    return ds
#-----------------------------------------------# 
# ---- Pass it ----#
if __name__ == '__main__':
    pass