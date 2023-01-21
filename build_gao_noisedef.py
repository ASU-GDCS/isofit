import pandas as pd
import numpy as np
import argparse
import os, sys
from scipy.interpolate import UnivariateSpline


if "ISOFIT_BASE" in os.environ["ISOFIT_BASE"]:
    ##Use the active isofit directory if defined
    isofit_repo = os.path.dirname(os.environ["ISOFIT_BASE"])
    AVNGNOISE=os.path.join(isofit_repo,"data/avirisng_noise.txt")
else:
    ##Use path of this file
    mydir = os.path.dirname(__file__)
    AVNGNOISE=os.path.join(mydir,"data/avirisng_noise.txt")


def main():
    parser = argparse.ArgumentParser(
               description="Interpolate AVNG noise to GAO3 wavelengths/fwhm")
    parser.add_argument("--verbose","-v",action="store_true",
                        help="Verbose output")
    parser.add_argument("-e", "--angnoise", default=AVNGNOISE,
                        help="Avisis-ng noise definition table")
    parser.add_argument("input",
                        help="3-column table of band number, wl, and fwhm")
    ## Example of input: data/gao_wv_fwhm_march22.txt
    parser.add_argument("output",
                        help="Output noise def file for isofit")
    args = parser.parse_args()

    input_noise = pd.read_csv(args.angnoise,skiprows=1,header=None,
                               sep='\s+',names=['wl','a','b','c','rmse'])

    ##Get current GAO wavelengths
    wltab = pd.read_csv(args.input,sep='\s+',header=None,
                        names=['band0','wl','fwhm'])
    wltab["wl"] = wltab["wl"]*1000
    wltab["fwhm"] = wltab["fwhm"]*1000

    output_noise = pd.DataFrame({"wl":np.round(wltab["wl"],0)})

    def interpolate_vals(var):
        # us = UnivariateSpline(input_noise["wl"], input_noise[var], s=None, ext='const')
        us = UnivariateSpline(input_noise["wl"], input_noise[var], s=0, ext='extrapolate')
        tmp = us(output_noise["wl"])
        us = UnivariateSpline(input_noise["wl"], input_noise[var], s=0.0001, ext='const')
        tmp[:15] = us(output_noise["wl"].to_numpy()[:15])
        tmp[-10:] = us(output_noise["wl"].to_numpy()[-10:])
        output_noise[var] = tmp

    for var in ["a", "b", "c", "rmse"]:
        interpolate_vals(var)

    # Write out
    rowmap = "{wl:0.7f} {a:0.12f} {b:0.12f} {c:0.12f} {rmse:0.12f}\n" 
    with open(args.output, 'w') as outref:
        ##Write header
        outref.write("#wvl a b c rmse\n")
        for id, row in output_noise.iterrows():
            outref.write(rowmap.format(**row.to_dict()))

    print("Done - output at {}".format(args.output))


if __name__ == "__main__":
    main()
