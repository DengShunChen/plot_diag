from __future__ import print_function
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import read_diag
import numpy as np
import ncepbufr

fig = plt.figure(figsize=(16,8))

m = Basemap(lon_0=180)
m.drawparallels(np.arange(-90,90,10),labels=[1,1,0,0])
m.drawmeridians(np.arange(0,360,20),labels=[0,0,0,1])
#m = Basemap(llcrnrlon=80.,llcrnrlat=-10.,urcrnrlon=190.,urcrnrlat=50., 
#            projection='lcc',lat_1=20.,lat_2=40.,lon_0=120.,
#            resolution='h',area_thresh=1000.)
#m.drawparallels(np.arange(0,70,10),labels=[1,1,0,0])
#m.drawmeridians(np.arange(80,190,10),labels=[0,0,0,1])

m.drawmapboundary(fill_color='#A6CAE0',linewidth=0)
m.fillcontinents(color='grey',alpha=0.7,lake_color='grey',zorder=10)
m.drawcoastlines(linewidth=0.1,color="white")


#----------------------------------------------------------------------------------------#
# NCEP BUFR
#----------------------------------------------------------------------------------------#
# filename
dtg ='17091712'
filename='gdas.satwnd.tm00.bufr_d.'+dtg

# string
hdrstr = 'SAID CLAT CLON YEAR MNTH DAYS HOUR MINU SWCM SAZA GCLONG SCCF SWQM'
obstr = 'HAMD PRLC WDIR WSPD'
qcstr = 'OGCE GNAP PCCF'

lons=[]
lats=[]

# read satellite wind file.
bufr = ncepbufr.open(filename)
bufr.print_table()
while bufr.advance() == 0:
  print(bufr.msg_counter, bufr.msg_type, bufr.msg_date)
  while bufr.load_subset() == 0:
      hdr = bufr.read_subset(hdrstr).squeeze()
      satid = int(hdr[0])
      if satid == 173 :
        yyyymmddhh ='%04i%02i%02i%02i%02i' % tuple(hdr[3:8])
        windtype = int(hdr[8])
        qm = hdr[12]
        obdata = bufr.read_subset(obstr).squeeze()
        lat = hdr[1]; lon = hdr[2]
        if windtype == 1 :
          print('satid, wind type, lat, lon, press, qcflg, time, speed, dir =',\
          satid,windtype,lat,lon,obdata[1],qm,yyyymmddhh,obdata[3],obdata[2])
          if lon < 0 :
              lon = lon + 360
          lats.append(lat)
          lons.append(lon)
  # only loop over first 4 subsets
# if bufr.msg_counter == 100: break
bufr.close()

print(lons,lats)
x,y = m(lons,lats)

nobs = len(lons)
platformname='All Observation'
m.scatter(x,y,4,color='b',marker='o',edgecolors='none',zorder=20,label=platformname+' - '+str(nobs))

#----------------------------------------------------------------------------------------#
# GSI diag
#----------------------------------------------------------------------------------------#
#dtg = '2017091712'
#platform = 'conv'
#obsfile = 'diag_'+platform+'_ges.'+dtg
#
## read header 
#diag_conv = read_diag.diag_conv(obsfile,endian='big')
#print('total number of obs = ',diag_conv.nobs)
#
## read data 
#diag_conv.read_obs()
#
#instrument = '  v'
#
## loop over all AMV satellite type
#reptype = 252
#
#indx = np.logical_and(diag_conv.obtype == instrument, diag_conv.used == 1)
#indx = np.logical_and(indx, diag_conv.code == reptype)
#nobs = indx.sum()
#
#color='r'
#platformname='Assimilated'
#
#x,y = m(diag_conv.lon[indx],diag_conv.lat[indx])
#m.scatter(x,y,4,color=color,marker='o',edgecolors='none',zorder=20,label=platformname+' - '+str(nobs))
#
#
#plt.legend(ncol=7,loc=8,bbox_to_anchor=(0.5,-0.1),markerscale=2)
#plt.title(' %s     %s AMV'% (dtg,'HIMAWARI-8'),fontsize=25)
#plt.savefig('H8_Tinning'+'_'+str(dtg)+'.png',dpi=100)
plt.show()


