#!/usr/bin/env python 
from __future__ import print_function
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import read_diag
import numpy as np

fig = plt.figure(figsize=(16,8))

m = Basemap(lon_0=180)
m.drawmapboundary(fill_color='#A6CAE0',linewidth=0)
m.fillcontinents(color='grey',alpha=0.7,lake_color='grey',zorder=10)
m.drawcoastlines(linewidth=0.1,color="white")


dtg = '2017091712'

instrument = 'seviri'
platformlist = ['m08','m10']

for platform in platformlist:

  obsfile = 'diag_'+ instrument + '_' + platform + '_ges.'+ dtg

  # open diag 
  diag_rad = read_diag.diag_rad(obsfile,endian='big')
  print(platform,' total number of obs = ',diag_rad.nobs)

  # activate reading in data
  diag_rad.read_obs()

  # print o-f stats for one channel
  nobsall = diag_rad.channel.sum()

  idx = np.logical_and(diag_rad.used == 1, diag_rad.oberr < 1.e9)
  nobs = idx.sum()

  print(' total ',nobs,' obs out of ',nobsall)


  x,y = m(diag_rad.lon[idx],diag_rad.lat[idx])

  if platform == 'n15':
    color='r'
    platformname='NOAA-15'
  elif platform == 'm08':
    color='g'
    platformname='METEOSAT-8'
  elif platform == 'm10':
    color='r'
    platformname='METEOSAT-10'
  elif platform == 'metop-b':
    color='b'
    platformname='METOP-B'
  elif platform == 'aqua':
    color='b'
    platformname='AQUA'
  else:
    color='k'
  
  m.scatter(x,y,4,color=color,marker='o',edgecolors='none',zorder=20,label=platformname+' - '+str(nobs))

plt.legend(ncol=7,loc=8,bbox_to_anchor=(0.5,-0.1),markerscale=2)
plt.title(' %s   %s  Assimilated '% (dtg,'SEVIRI'),fontsize=25)
plt.savefig(instrument+'_'+str(dtg)+'.png',dpi=100)
plt.show()


