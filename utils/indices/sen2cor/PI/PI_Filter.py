"""
# Script to filter the generated TIFF files by Plastic Index (PI) value from PI.py
"""

# Import libraries
import glob
import os
import re
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version


# Define a function to calculate plastic index using band arrays for red, NIR bands
def pi(red, nir):
    return (nir/(nir + red))


def filter_pi_values(path):
    print("Filtering PI values...")

    # Set input directory
    in_dir = path

    # Regex to capture bands and their extensions
    pattern = re.compile(r'.*_(B\d{2})_\d+m\.tif$|.*_(B\d{2})\.jp2$')

    # Get lists containing each band that will be looped through later
    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(
        band) and 'B04' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and 'B08' in band]

    print('red_files', red_files)
    print('nir_files', nir_files)

    for i in range(len(red_files)):

        # Open each band using gdal
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])

        # read in each band as array and convert to float for calculations
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the pi() function on red, NIR bands
        pi2 = pi(red, nir)

        # Output name
        outfile_name = red_files[i].split('_B')[0] + '_PI_Filtered.tif'

        # Boolean matrix
        pi_mask = (pi2 >= 0.424) & (pi2 <= 0.477)

        # Convert matrix to mask
        pi_treshold = pi_mask.astype(int)

        x_pixels = pi2.shape[0]  # number of pixels in x
        y_pixels = pi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, number of bands, and datatype
        pi_data = driver.Create(outfile_name, x_pixels,
                                y_pixels, 1, gdal.GDT_Byte)

        # Set PI array as the 1 output raster band
        pi_data.GetRasterBand(1).WriteArray(pi_treshold)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = red_link.GetGeoTransform()  # Grab input GeoTransform information
        proj = red_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        pi_data.SetGeoTransform(geotrans)
        pi_data.SetProjection(proj)
        pi_data.FlushCache()
        pi_data = None


if __name__ == '__main__':

    path = input(
        "Enter the path where the images will be searched to filter the PI values within a specific range: ")

    filter_pi_values(path)
