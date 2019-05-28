import numpy as np

# Compute a moving mean along the x-axis.
def moving_mean(x, y, yerr=None, window=3.):

    # Set the weights.
    if yerr is None:
        weights = np.ones_like(y)
    else:
        weights = 1/yerr**2

    # Sums for computing the mean.
    sum1 = np.append(0, np.cumsum(weights*y))
    sum2 = np.append(0, np.cumsum(weights))

    # Indices at the start and end of the window.
    i = np.searchsorted(x, x - window/2.)
    j = np.searchsorted(x, x + window/2.)

    # Compute the mean.
    mean = (sum1[j] - sum1[i])/(sum2[j] - sum2[i])

    return mean

# Fit a curve for local linear
def linfit(lstidx, x, y, sky, mag, emag):

    sort = np.argsort(lstidx)
    invsort = np.argsort(sort)

    lstidx = lstidx[sort]
    x = x[sort]
    y = y[sort]
    sky = sky[sort]
    mag = mag[sort]
    emag = emag[sort]

    _, idx = np.unique(lstidx, return_inverse=True)

    nobs = np.bincount(idx)
    strides = np.append(0, np.cumsum(nobs))

    xbar = np.bincount(idx, x)/np.bincount(idx)
    ybar = np.bincount(idx, y)/np.bincount(idx)

    mat = np.column_stack([np.ones(len(lstidx)), x-xbar[idx], y-ybar[idx], sky])

    pars = np.zeros((len(nobs), 4))
    pars[:,0] = np.bincount(idx, mag/emag**2)/np.bincount(idx, 1/emag**2)

    for i in range(len(nobs)):

        if nobs[i] < 5:
             continue

        i1 = strides[i]
        i2 = strides[i+1]

        pars[i] = np.linalg.lstsq(mat[i1:i2]/emag[i1:i2,None], mag[i1:i2]/emag[i1:i2], rcond=None)[0]

    fit = np.sum(pars[idx]*mat, axis=1)

    fit1 = pars[idx,0]
    fit2 = fit - pars[idx,0]

    return fit1[invsort], fit2[invsort], (nobs > 4)[idx][invsort]

def local_lin(jd, lstseq, x, y, sky, mag, emag, window=5., maxiter=50, dtol=1e-3):

    lstidx = (lstseq % 270)
    fit0 = np.zeros(len(jd))
    fit1 = np.zeros(len(jd))

    fit = np.zeros_like(mag)
    for niter in range(maxiter):
        fit1, fit2, mask = linfit(lstidx, x, y, sky, mag - fit0, emag)
        fit0 = moving_mean(jd, mag - fit1 - fit2, emag, window)

        if niter > 0:

            if np.all(np.abs(fit - fit0 - fit1 - fit2) < dtol):
                break

        fit = fit0 + fit1 + fit2

    return fit#, fit0, fit1, fit2, mask
