import numpy as np
import os
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import time
import sep
from regularizepsf.fitter import CoordinatePatchCollection, CoordinateIdentifier
from regularizepsf.corrector import calculate_covering
from regularizepsf.psf import simple_psf
from regularizepsf.corrector import ArrayCorrector

def main():
    patch_size, psf_size = 256, 32
    out_dir = "../data/DASH/"
    fn = "../data/DASH/DASH_2014-07-22T22:37:51.040_LF_expTime_10_numInBurst_8_ccdTemp_-20.0046.fits"

    with fits.open(fn) as hdul:
        header = hdul[0].header
        data = hdul[0].data.astype(float)

    bkg = sep.Background(data)
    bkg_image = bkg.back()
    bkg_rms = bkg.rms()

    data_sub = data - bkg
    objects = sep.extract(data_sub, 3, err=bkg.globalrms)
    d = data_sub

    coordinates = [CoordinateIdentifier(0, int(x) - psf_size // 2, int(y) - psf_size // 2) for y, x in
                   zip(objects['x'], objects['y'])]
    patch_collection = CoordinatePatchCollection.extract([d], coordinates, psf_size)

    corners = calculate_covering(d.shape, patch_size)
    averaged = patch_collection.average(corners, patch_size, psf_size, mode='median')

    @simple_psf
    def dash_target(x, y, x0=patch_size / 2, y0=patch_size / 2, sigma_x=3.25 / 2.355, sigma_y=3.25 / 2.355):
        return np.exp(-(np.square(x - x0) / (2 * np.square(sigma_x)) + np.square(y - y0) / (2 * np.square(sigma_y))))

    pad_amount = (patch_size - psf_size) // 2

    evaluation_dictionary = dict()
    for identifier, patch in averaged.items():
        corrected_patch = patch.copy()
        corrected_patch[np.isnan(corrected_patch)] = 0
        low, high = np.median(corrected_patch), np.nanpercentile(corrected_patch, 99.999) - 0.1
        corrected_patch = (corrected_patch - low) / (high - low)
        corrected_patch[corrected_patch < 0.05] = 0
        corrected_patch[corrected_patch > 0.95] = 1
        evaluation_dictionary[(identifier.x, identifier.y)] = np.pad(corrected_patch,
                                                                     ((pad_amount, pad_amount),
                                                                      (pad_amount, pad_amount)),
                                                                     mode='constant')

    target_evaluation = dash_target(*np.meshgrid(np.arange(patch_size), np.arange(patch_size)))
    array_corrector = ArrayCorrector(evaluation_dictionary, target_evaluation)

    print(f"Starting with {len(evaluation_dictionary)}")
    start = time.time()
    corrected = array_corrector.correct_image(d, alpha=2.0, epsilon=0.3)
    end = time.time()
    print(end - start)
    print("Finished!")

    np.save(os.path.join(out_dir, "dash_uncorrected.npy"), d)
    np.save(os.path.join(out_dir, "dash_corrected.npy"), corrected)


if __name__ == "__main__":
    main()
