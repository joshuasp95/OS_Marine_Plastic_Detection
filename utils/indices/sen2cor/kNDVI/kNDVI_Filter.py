# Script to filter tif files generated by kNDVI.py based on kNDVI values
# Refer to studies to filter out plastic based on kNDVI values (e.g., kNDVI > -0.2 & 0.2 < kNDVI)

# Import libraries
import glob
import os
import re
import numpy as np
from osgeo import gdal  

# Define a function to calculate kNDVI values


def kndvi(red, nir):
    try:
        ndvi = ((nir - red)/(nir + red))
        kndvi = np.tanh(ndvi * ndvi)
        return kndvi
    except Exception as e:
        print("Error: " + str(e))


def filter_kndvi_values(path):
    print("Filtering kNDVI values...")

    # Set input directory
    in_dir = path

    # Regex to capture the bands and their extensions
    pattern = re.compile(r'.*_(B\d{2})_\d+m\.tif$|.*_(B\d{2})\.jp2$')

    # Get lists containing each band that will be iterated over later
    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(
        band) and 'B04' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and 'B08' in band]

    for i in range(len(red_files)):

        # Open each band using gdal
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])

        # Read each band as an array and convert it to float for calculations
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the kndvi() function on red and NIR bands
        kndvi2 = kndvi(red, nir)

        # Output filename
        outfile_name = red_files[i].split('_B')[0] + '_kNDVI_Filtered.tif'

        # Boolean array
        kndvi_mask = (kndvi2 >= 0.005) & (kndvi2 <= 0.032)

        # Convert array to mask
        kndvi_threshold = kndvi_mask.astype(int)

        x_pixels = kndvi2.shape[0]  # number of pixels in x
        y_pixels = kndvi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create a driver using the output filename, x and y pixels, number of bands, and datatype
        kndvi_data = driver.Create(
            outfile_name, x_pixels, y_pixels, 1, gdal.GDT_Byte)

        # Set the kNDVI array as the 1 output raster band
        kndvi_data.GetRasterBand(1).WriteArray(kndvi_threshold)

        # Set up the coordinate reference system of the output GeoTIFF
        geotrans = red_link.GetGeoTransform()  # Grab input GeoTransform information
        proj = red_link.GetProjection()  # Grab projection information from the input file

        # Set GeoTransform parameters and projection on the output file
        kndvi_data.SetGeoTransform(geotrans)
        kndvi_data.SetProjection(proj)
        kndvi_data.FlushCache()
        kndvi_data = None


if __name__ == '__main__':
    path = input(
        "Enter the path where the images are located to filter based on a specified kNDVI range: ")

    filter_kndvi_values(path)
