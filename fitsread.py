from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table
from astropy.io import fits
#from astropy.stats import BoxLeastSquares

### Written by Keegan Thomson-Paressant

# Read in your TESS lightcurve as a fits file, taking the values for time and flux (you can also take their respective errors if you like).
#f=fits.open("tess2018206045859-s0001-0000000267263253-111-s_llc.fits")
f=fits.open("toi135.fits")
time=f[1].data['TIME']
flux=f[1].data['SAP_FLUX']

# I defined a range of values to replace with NaNs wherever I see weird points in the data.
# Certainly not optimised, but works as a brute force approach in the short term.
flagvals=[1340,1346,2298,3006,5119,5403,6977,6983,6986,6987,6998,7013,7234,8233,8760,9034,11809,13661,13671,13849,13937,15424,15763,15764,17335,17352,17401,17414,17415,17433,18975,19002,19006,19076,19240,19725]
#[15887:17320]

# Replace any values below a generous flux value with NaNs, as well as any of the flagged points defined earlier.
for i in range(len(flux)):
    if flux[i] < 29800:
        flux[i] = np.nan
        i+=1
    else:
        i+=1

for j in flagvals:
    flux[j] = np.nan
    j+=1

for k in range(15887,17321):
    flux[k] = np.nan
    k+=1

# Temporarily replace the NaNs with zeroes in another array in order to calculate the mean (as NaN prevents it from working).
vals=[]
for a in range(len(flux)):
    if (np.isnan(flux[a])):
        vals.append(0)
    else:
        vals.append(flux[a])
mean=np.mean(vals)
normflux=flux/mean

# Plot of time versus the mean-reduced flux
plt.plot(time,normflux)
plt.show()

# Define a polynomial fit, specifying to define it only where time and flux are finite (i.e. not NaNs), and divide it from the data.
idx=np.isfinite(time) & np.isfinite(normflux)
coefs = np.polynomial.polynomial.polyfit(time[idx],normflux[idx],1)
ffit=np.polynomial.polynomial.polyval(time,coefs)
corrected=normflux/ffit

#idx = np.isfinite(time) & np.isfinite(flux)
#fit = np.polyfit(time[idx],flux[idx],1)
#fit_fn = np.poly1d(fit)
#corrected = flux - fit_fn(time) #+ 30221.9122551963

#t=np.ascontiguousarray(time, dtype=np.float64)
#f=np.ascontiguousarray(corrected, dtype=np.float64)

#durations = np.linspace(0.05, 0.2, 10)
#model = BLS(t,f, dy=0.01)
#periodogram = model.autopower(0.2)


# Plot BJD versus normalised and corrected flux
plt.plot(time,corrected,linewidth=1)
plt.xlim(1325.0,1353.3)
plt.xlabel('Barycentric Julian Date')
plt.ylabel('Normalised Flux')
plt.show()

# Convert BJD to JD. The tau value given here is a scaling factor, which will be mostly correct for you, but should probably be checked.
tau=1.3228e-8
for a in range(len(time)):
    time[a] = (time[a]+2457000)-a*tau

# Plot the final JD versus normalised and corrected flux
plt.plot(time,corrected,linewidth=1)
#plt.xlim(1325.0,1353.3)
plt.xlabel('Julian Date')
plt.ylabel('Normalised Flux')
plt.show()

# Export your corrected data as a new fits file, ready for phase folding.
data=Table([time,corrected],names=['Time_JD','Flux'])
data.write('/data5/thomson/Folder/TOI135.fits',format='fits', overwrite=True)
