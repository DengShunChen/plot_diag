#!/usr/bin/env python 
from __future__ import print_function
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import read_diag
import numpy as np
from matplotlib import gridspec as gspec

dtg = '2017091712'
platform = 'conv'
obsfile = 'diag_'+platform+'_ges.'+dtg

fig = plt.figure(figsize=(16,8),dpi=100)
plt.subplots_adjust(top=0.9,bottom=0.1,right=0.98,left=0.02)
gs = gspec.GridSpec(1,2)

ax = plt.subplot(gs[0])

plt.title("North Hemisphere - Polar")
m = Basemap(projection='npstere',boundinglat=55,lon_0=180,resolution='l')
m.drawmapboundary(fill_color='#A6CAE0',linewidth=0)
m.fillcontinents(color='grey',alpha=0.7,lake_color='grey',zorder=10)
m.drawcoastlines(linewidth=0.1,color="white")
m.drawparallels(np.asarray([80,60]), labels=[1,1,0,1])
m.drawmeridians(np.arange(-180,180,30), labels=[1,1,0,1])


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

  reptypelist =[3,4,206,207,209]
  for reptype in reptypelist:
    indx = np.logical_or(np.logical_or(diag_conv.code == 244, diag_conv.code == 257),diag_conv.code == 258) 
    indx = np.logical_and(indx,np.logical_and(np.logical_and(diag_conv.obtype == instrument, diag_conv.used == 1), diag_conv.subcode == reptype))
    nobs = indx.sum()
    print('total number of obs',reptype,' = ',nobs)
    
    if reptype == 3: 
      color='b'
      platformname='METOP-B('+str(reptype)+')'
    elif reptype == 4: 
      color='darkorange'
      platformname='METOP-A('+str(reptype)+')'
    elif reptype == 206: 
      color='g'
      platformname='NOAA-15('+str(reptype)+')'
    elif reptype == 207: 
      color='c'
      platformname='NOAA-16('+str(reptype)+')'
    elif reptype == 209: 
      color='violet'
      platformname='NOAA-18('+str(reptype)+')'
    else: 
      color='k'
      platformname='UNKNOWN('+str(reptype)+')'

    if nobs != 0:
      x,y = m(diag_conv.lon[indx],diag_conv.lat[indx])
      m.scatter(x,y,4,color=color,marker='o',edgecolors='none',zorder=20,label=platformname+' - '+str(nobs))

ax = plt.subplot(gs[1])
plt.title("Sourth Hemisphere - Polar")
m = Basemap(projection='spstere',boundinglat=-55,lon_0=180,resolution='l')
m.drawmapboundary(fill_color='#A6CAE0',linewidth=0)
m.fillcontinents(color='grey',alpha=0.7,lake_color='grey',zorder=10)
m.drawcoastlines(linewidth=0.1,color="white")
m.drawparallels(np.asarray([-80,-60]), labels=[1,1,0,1])
m.drawmeridians(np.arange(-180,180,30), labels=[1,1,0,1])

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

  reptypelist =[3,4,206,207,209,784]
  for reptype in reptypelist:
    indx = np.logical_or(np.logical_or(np.logical_or(diag_conv.code == 244, diag_conv.code == 257),diag_conv.code == 258),diag_conv.code == 259)
    indx = np.logical_and(indx,np.logical_and(np.logical_and(diag_conv.obtype == instrument, diag_conv.used == 1), diag_conv.subcode == reptype))
    nobs = indx.sum()
    print('total number of obs',reptype,' = ',nobs)

    if reptype == 3:
      color='b'
      platformname='METOP-B('+str(reptype)+')'
    elif reptype == 4:
      color='darkorange'
      platformname='METOP-A('+str(reptype)+')'
    elif reptype == 206:
      color='g'
      platformname='NOAA-15('+str(reptype)+')'
    elif reptype == 207:
      color='c'
      platformname='NOAA-16('+str(reptype)+')'
    elif reptype == 209:
      color='violet'
      platformname='NOAA-18('+str(reptype)+')'
    elif reptype == 784:
      color='darkred'
      platformname='AQUA('+str(reptype)+')'
    else:
      color='k'
      platformname='UNKNOWN('+str(reptype)+')'

    if nobs != 0:
      x,y = m(diag_conv.lon[indx],diag_conv.lat[indx])
      m.scatter(x,y,4,color=color,marker='o',edgecolors='none',zorder=20,label=platformname+' - '+str(nobs))

plt.legend(ncol=7,loc=8,bbox_to_anchor=(-0.1,-0.15),markerscale=2)
plt.suptitle(' %s   %s  Assimilated '% (dtg,'AMV'),fontsize='x-large',fontweight='bold')
plt.savefig('AMV'+'_'+str(dtg)+'_polar.png',dpi=100)
plt.show()


