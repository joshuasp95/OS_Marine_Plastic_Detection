# NDWI = (green - nir)/(green+nir)

# Import libraries
import glob
import re
import os
from osgeo import gdal


# Define a function to calculate NDWI values
def ndwi(green, nir):
    try:
        return ((green - nir)/(nir + green))
    except Exception as e:
        print("Error: " + str(e))


def calculate_NDWI(path):
    print("Running NDWI index...")

    # Set input directory
    in_dir = path

    pattern = re.compile(r'.*[\\\/].*(559|560|833)\.tif$')

    green_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    green_files = [band for band in green_files if pattern.match(
        band) and ('559' in band or '560' in band)]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and '833' in band]

    print(green_files)
    print(nir_files)

    for i in range(len(green_files)):

        # Open each band using gdal
        green_link = gdal.Open(green_files[i])
        nir_link = gdal.Open(nir_files[i])

        # read in each band as array and convert to float for calculations
        green = green_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the ndwi() function on green, NIR bands
        ndwi2 = ndwi(green, nir)

        # Create output filename based on input name
        outfile_name = green_files[i].split('_L')[0] + '_NDWI.tif'

        x_pixels = ndwi2.shape[0]  # number of pixels in x
        y_pixels = ndwi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, # of bands, and datatype
        ndwi_data = driver.Create(outfile_name, x_pixels,
                                  y_pixels, 1, gdal.GDT_Float32)

        # Set NDWI array as the 1 output raster band
        ndwi_data.GetRasterBand(1).WriteArray(ndwi2)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = green_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = green_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        ndwi_data.SetGeoTransform(geotrans)
        ndwi_data.SetProjection(proj)
        ndwi_data.FlushCache()
        ndwi_data = None


if __name__ == "__main__":
    path = input(
        "Enter the path where the Acolite files will be searched to calculate the NDWI: ")

    calculate_NDWI(path)
