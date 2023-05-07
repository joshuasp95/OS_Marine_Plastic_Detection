# @author: Cole Krehbiel, thanks and big support
# @modified by: Joshua Sainz Palacios
# NDVI = nir-red / nir+red

# Import libraries
import glob
import re
import os
from osgeo import gdal 


# Define a function to calculate NDVI using band arrays for red, NIR bands
def ndvi(red, nir):
    try:
        return ((nir - red)/(nir + red))
    except Exception as e:
        print("Error: " + str(e))


def calculate_NDVI(path):
    print("Running NDVI index...")

    # Set input directory
    in_dir = path

    pattern = re.compile(r'.*[\\\/].*(665|833)\.tif$')

    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(
        band) and '665' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and '833' in band]

    print(red_files)
    print(nir_files)

    for i in range(len(red_files)):

        # Open each band using gdal
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])

        # read in each band as array and convert to float for calculations
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the ndvi() function on red, NIR bands
        ndvi2 = ndvi(red, nir)

        # Create output filename based on input name
        outfile_name = red_files[i].split('_L')[0] + '_NDVI.tif'

        x_pixels = ndvi2.shape[0]  # number of pixels in x
        y_pixels = ndvi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, # of bands, and datatype
        ndvi_data = driver.Create(outfile_name, x_pixels,
                                  y_pixels, 1, gdal.GDT_Float32)

        # Set NDVI array as the 1 output raster band
        ndvi_data.GetRasterBand(1).WriteArray(ndvi2)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = red_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = red_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        ndvi_data.SetGeoTransform(geotrans)
        ndvi_data.SetProjection(proj)
        ndvi_data.FlushCache()
        ndvi_data = None


if __name__ == "__main__":
    path = input(
        "Enter the path where the Acolite files will be searched to calculate the NDVI: ")

    calculate_NDVI(path)
