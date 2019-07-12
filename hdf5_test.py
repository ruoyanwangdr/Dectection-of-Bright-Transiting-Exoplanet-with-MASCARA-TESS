#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 15:20:55 2018

@author: rywang
Cited from talens
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

filename = 'red0_vmag_2018Q1LSE.hdf5'#'/data5/mascara/LaSilla/20171202LSN/lightcurves/fast_20171202LSN.hdf5'

#Open the file in read only mode, always use a with statement.
with h5py.File(filename,'r') as f:
    # Print all groups and dataset present in the root of the file.
    print (f.keys())
    # Print the names and values for all attributes of the 'header' group.
    print (f['header'].attrs.items())
    # Print all groups and datasets that are part of the 'station' group.
    print (f['station'].keys())
    # Read the values from the lstseq dataset in the data group as an array.
    lstseq = f['station/lstseq'].value
    #When reading multiple datasets from the same group this alternate syntax
    #may be useful.
    grp = f['station']
    
    lstseq = grp['lstseq'].value
    jd = grp['jd'].value
    moonalt = grp['moonalt'].value
    moonx = grp['moonx'].value
    moony = grp['moony'].value
    
    #Read the ascc numbers of the stars.
    ascc = f['stars/ascc'].value
    
    #Read the lightcurve of a star.
    grp = f['lightcurves']
    lc = grp[ascc[1500]].value
    
#Plot the moon's path across the detector.
plt.subplot(111, aspect='equal')
    
#Remove out-of-bounds values.
mask = (moonx !=9999) | (moony !=9999)
plt.plot(moonx[mask], moony[mask])
plt.xlim(0,4008)
plt.ylim(0,2672)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
    
#Plot the flux of the star.
plt.title('ASCC {}'.format(ascc[1500]))
    
#Look up the jd of the observation using the lstseq
idx = np.searchsorted(lstseq, lc['lstseq'])
plt.plot(jd[idx], lc['flux0'], 'k.')
plt.xlabel('Julian date [days]')
plt.ylabel('Flux [counts]')
plt.show
   
