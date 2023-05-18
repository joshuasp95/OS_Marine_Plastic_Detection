# Script to calculate the Enhanced Vegetation Index (EVI) of all Sentinel-2 images without atmospheric correction (.jp2)
# or with atmospheric correction (.tif)
# The formula for EVI is 2.5*(nir - red)/(nir + 6*red - 7.5*blue + 1)

# Import libraries
import glob
import re
import os
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check the version


# Define a function to calculate EVI values
def evi(blue, red, nir):
    try:
        return 2.5 * (nir - red) / (nir + 6*red - 7.5*blue + 1)
    except Exception as e:
        print("Error: " + str(e))


def calculate_EVI(path):
    print("Running EVI index...")

    # Set the input directory
    in_dir = path

    # Regex to capture the bands and their extensions
    pattern = re.compile(r'.*_(B\d{2})_\d+m\.tif$|.*_(B\d{2})\.jp2$')

    # Get lists containing each band that will be iterated over later
    blue_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    blue_files = [band for band in blue_files if pattern.match(
        band) and 'B02' in band]

    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(
        band) and 'B04' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and 'B08' in band]

    print('blue_files', blue_files)
    print(len(blue_files))
    print('red_files', red_files)
    print(len(red_files))
    print('nir_files', nir_files)
    print(len(nir_files))

    for i in range(len(red_files)):
        # Open each band using GDAL
        blue_link = gdal.Open(blue_files[i])
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])

        # Read each band as an array and convert it to float for calculations
        blue = blue_link.ReadAsArray().astype(float)
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the evi() function on blue, red, and NIR bands
        evi2 = evi(blue, red, nir)

        # Create an output filename based on the input name
        outfile_name = red_files[i].split('_B')[0] + '_EVI.tif'

        x_pixels = evi2.shape[0]  # number of pixels in x
        y_pixels = evi2.shape[1]  # number of pixels in y

        # Set up the output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create a driver using the output filename, x and y pixels, number of bands, and datatype
        evi_data = driver.Create(
            outfile_name, x_pixels, y_pixels, 1, gdal.GDT_Float32)

        # Set the EVI array as the 1 output raster band
        evi_data.GetRasterBand(1).WriteArray(evi2)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = blue_link.GetGeoTransform()  # Grab input GeoTransform information
        proj = blue_link.GetProjection()  # Grab projection information from the input file

        # Set the GeoTransform parameters and projection on the output file
        evi_data.SetGeoTransform(geotrans)
        evi_data.SetProjection(proj)
        evi_data.FlushCache()
        evi_data = None


if __name__ == "__main__":
    path = input(
        "Enter the path where Acolite files are located for calculating EVI: ")

    calculate_EVI(path)
