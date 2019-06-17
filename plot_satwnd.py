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


dtg = '2018072618'
platform = 'conv'
obsfile = 'diag_'+platform+'_ges.'+dtg

# read header 
diag_conv = read_diag.diag_conv(obsfile,endian='big')
print('total number of obs = ',diag_conv.nobs)

# read data 
diag_conv.read_obs()



#instrumentlist = ['  v','  u','  t','  q','gps']
instrumentlist = ['  v']
for instrument in instrumentlist:

  if instrument == '  v':
    obsname = 'V-Wind'
  elif instrument == '  u':
    obsname = 'U-Wind'
  elif instrument == '  t':
    obsname = 'Temperature'
  elif instrument == '  q':
    obsname = 'Specific Humidity'
  elif instrument == 'gps':
    obsname = 'GPS Radio Occultation'

  reptypelist =[173,174,55,56,57,70,257,259,270]
  for reptype in reptypelist:
    indx = np.logical_or(np.logical_or(np.logical_or(diag_conv.code == 242, diag_conv.code == 243),diag_conv.code == 245),diag_conv.code == 246)
    indx = np.logical_or(np.logical_or(np.logical_or(indx, diag_conv.code == 250),diag_conv.code == 252),diag_conv.code == 253)
    indx = np.logical_and(np.logical_and(np.logical_and(diag_conv.obtype == instrument, diag_conv.used == 1), diag_conv.subcode == reptype),indx)
    nobs = indx.sum()
    print('total number of obs',reptype,' = ',nobs)

    if reptype == 173: 
      color='b'
      platformname='HIMAWARI-8('+str(reptype)+')'
    elif reptype == 55: 
      color='darkorange'
      platformname='METEOSAT-8('+str(reptype)+')'
    elif reptype == 56: 
      color='orange'
      platformname='METEOSAT-9('+str(reptype)+')'
    elif reptype == 57: 
      color='r'
      platformname='METEOSAT-10('+str(reptype)+')'
    elif reptype == 70: 
      color='darkred'
      platformname='METEOSAT-11('+str(reptype)+')'
    elif reptype == 257: 
      color='c'
      platformname='GOES-13('+str(reptype)+')'
    elif reptype == 259: 
      color='g'
      platformname='GOES-15('+str(reptype)+')'
    elif reptype == 270: 
      color='olive'
      platformname='GOES-16('+str(reptype)+')'
    elif reptype == 784: 
      color='c'
      platformname='AQUA('+str(reptype)+')'
    else: 
      color='k'
      print(diag_conv.code)
      platformname='UNKNOWN('+str(reptype)+')'

    if nobs != 0:
      x,y = m(diag_conv.lon[indx],diag_conv.lat[indx])
      m.scatter(x,y,4,color=color,marker='o',edgecolors='none',zorder=20,label=platformname+' - '+str(nobs))

  plt.legend(ncol=7,loc=8,bbox_to_anchor=(0.5,-0.1),markerscale=2)
  plt.title(' %s   %s  Assimilated '% (dtg,'AMV'),fontsize=25)
  plt.savefig('AMV'+'_'+str(dtg)+'.png',dpi=100)
  plt.show()


