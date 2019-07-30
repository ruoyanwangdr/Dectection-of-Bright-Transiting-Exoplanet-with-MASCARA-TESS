import os
import matplotlib.pyplot as plt
import numpy as np
import math as m
from astropy.io import fits

### Written by Keegan Thomson-Paressant ###

# Read in MASCARA and TESS fits files that you've created
# Comment out whatever lines you don't need (e.g. if you're only using TESS)
mascara = fits.open('/data5/thomson/ASCC_2430860.fits')
tess = fits.open('/data5/thomson/Folder/TOI135.fits')

mtime=mascara[1].data['Time_JD']
mflux=mascara[1].data['Norm_Flux']

ttime=tess[1].data['Time_JD']
tflux=tess[1].data['Flux']

# Define period and epoch, given in PDF summary of TESS, or calculated with MASCARA
period=4.126904
epoch=1325.783759+2457000

# Loop over orbital period to define phase between -1 and 1, ideally having transit at 0
# if you've done everything correctly.
mphase=((mtime-epoch)%period)
tphase=((ttime-epoch)%period)
mphase = np.array([mphase[i]/period if mphase[i] < period/2. else (mphase[i]-period)/period for i in range(len(mphase))])
tphase = np.array([tphase[i]/period if tphase[i] < period/2. else (tphase[i]-period)/period for i in range(len(tphase))])

# Plot of time vs flux for both instruments
plt.figure()
plt.scatter(mtime,mflux,s=1.5)
plt.scatter(ttime,tflux,s=1.5)
#plt.show()

# Plot of phase vs flux for both instruments, transit should be immediately apparent.
plt.figure()
plt.scatter(mphase,mflux,s=1.5)
plt.scatter(tphase,tflux,s=1.5)
plt.show()
