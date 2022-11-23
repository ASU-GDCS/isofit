import pandas as pd
import numpy as np
from scipy.interpolate import UnivariateSpline


noisetab = pd.read_csv("data/avirisng_noise.txt",skiprows=1,header=None,sep='\s+',names=['wl','a','b','c','rmse'])

##Get current GAO wavelengths
#Copy isofit-formatted wavelengths from March 2022 to data
wltab = pd.read_csv("data/gao_wv_fwhm_march22.txt",sep='\s+',header=None,names=['band0','wl','fwhm'])
wltab["wl"] = wltab["wl"]*1000
wltab["fwhm"] = wltab["fwhm"]*1000

noisetab2 = pd.DataFrame({"wl":np.round(wltab["wl"],0)})


def interpolate_vals(var):
    # us = UnivariateSpline(noisetab["wl"], noisetab[var], s=None, ext='const')
    us = UnivariateSpline(noisetab["wl"], noisetab[var], s=0, ext='extrapolate')
    tmp = us(noisetab2["wl"])
    us = UnivariateSpline(noisetab["wl"], noisetab[var], s=0.0001, ext='const')
    tmp[:15] = us(noisetab2["wl"].to_numpy()[:15])
    tmp[-10:] = us(noisetab2["wl"].to_numpy()[-10:])
    noisetab2[var] = tmp


for var in ["a", "b", "c", "rmse"]:
    interpolate_vals(var)


#  v = "b"
#  ax.cla()
#  ax.plot(noisetab["wl"],noisetab[v],c='red')
#  ax.plot(noisetab2["wl"],noisetab2[v],c='darkred')

# Write out
with open("data/gao_2013_noise.txt", 'w') as outref:
    #  # Copy the header
    #  outref.write("#       wvl                a                b                c                d\n")
    #  for id, row in noisetab2.iterrows():
    #      outref.write("{wl:11.7f} {a:16.12f} {b:16.12f} {c:16.12f} {rmse:16.12f}\n".format(**row.to_dict()))
    # Must be single spaces between columns
    outref.write("#wvl a b c rmse\n")
    for id, row in noisetab2.iterrows():
        outref.write("{wl:0.7f} {a:0.12f} {b:0.12f} {c:0.12f} {rmse:0.12f}\n".format(**row.to_dict()))
