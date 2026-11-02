#!/usr/bin/env python3
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# defaults
dict_limit = {
  # [S,W,N,E]
  'LAKE_OKEE':[26.65,-81.13,27.25,-80.53],
  'FLKEYS':[24,-83,26,-80],
  'YUCATAN':[15,-90,22,-82],
  'PANAMA':[7.5,-84,15,-75],
}
dict_pixdeg = {
  '1KM':110,
  'QKM':440,
}
dict_minscl = {
  'CHL':4.0,
  'CYANO':0.0,
  'FAD':0.0,
}
dict_maxscl = {
  'CHL':200.0,
  'CYANO':40.0,
  'FAD':1.0,
}
dict_logscl = {
  'CHL':True,
  'CYANO':False,
  'FAD':False,
}
dict_highscl = {
  'CHL':235,
  'CYANO':235,
  'FAD':235,
}
# read digital numbers
filename = 'J20251741528.QKM.LAKE_OKEE.PASS.L3D.CHL.png'
filename = 'J20221941524.QKM.FLKEYS.PASS.L3D.CYANO.png'
im = Image.open(filename)
arr = np.array(im)
assert len(arr.shape)==2, 'This is RGB not indexed PNG -- digital numbers'
## extract from filename
ROI = filename.split('.')[2]
RES = filename.split('.')[1]
PROD = filename.split('.')[5]
## init scl parameters
limit = dict_limit[ROI]
pixdeg = dict_pixdeg[RES]
minscl = dict_minscl[PROD]
maxscl = dict_maxscl[PROD]
logscl = dict_logscl[PROD]
highscl = dict_highscl[PROD]
# try to read scl parameters
metadata = im.info
try:
    minscl = float(metadata['minscl'])
except KeyError:
    print('Use the default minscl')
try:
    maxscl = float(metadata['maxscl'])
except KeyError:
    print('Use the default maxscl')
try:
    logscl = bool(metadata['logscl'])
except KeyError:
    print('Use the default logscl')
try:
    highscl = int(metadata['highscl'])
except KeyError:
    print('Use the default highscl')
print('minscl - %f, maxscl - %f, logscl - %s, highscl - %i'%(minscl,maxscl,logscl,highscl))
# digital number to actual values
if logscl:
    val = np.exp(np.log(minscl)+(np.log(maxscl)-np.log(minscl))/(highscl-0)*arr)
else:
    val = minscl+(maxscl-minscl)/(highscl-0)*arr
val[arr>highscl] = np.nan	# any > highscl is for nondata
# generate logitude and latitude
dims = arr.shape
lons = limit[1]+np.arange(dims[1])/pixdeg
lons = np.repeat(lons[np.newaxis,:],dims[0],axis=0)
lats = limit[2]-np.arange(dims[0])/pixdeg
lats = np.repeat(lats[:,np.newaxis],dims[1],axis=1)
# quickly visualize a numpy array
if logscl:
    plt.imshow(val, norm=LogNorm(), cmap='rainbow')
else:
    plt.imshow(val, cmap='rainbow')
plt.colorbar()
plt.show()
