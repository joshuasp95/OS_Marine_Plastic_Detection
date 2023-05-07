# Import libraries
import glob
import os
import re
from osgeo import gdal  


# Define a function to calculate NDVI values
def ndvi(red, nir):
    try:
        return ((nir - red)/(nir + red))
    except Exception as e:
        print("Error: " + str(e))


def filter_ndvi_values(path):
    print("Filtering NDVI values...")

    # Set input directory
    in_dir = path

    pattern = re.compile(r'.*[\\\/].*(665|833)\.tif$')

    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(
        band) and '665' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and '833' in band]

    for i in range(len(red_files)):

        # Open each band using gdal
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])

        # read in each band as array and convert to float for calculations
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the ndvi() function on red, NIR bands
        ndvi2 = ndvi(red, nir)

        # Output name
        outfile_name = red_files[i].split('_L')[0] + '_NDVI_Filtered.tif'

        # Boolean mask
        ndvi_mask = (ndvi2 >= -0.2) & (ndvi2 <= 0.25)

        # Convertir matriz a mascara
        ndvi_treshold = ndvi_mask.astype(int)

        x_pixels = ndvi2.shape[0]  # number of pixels in x
        y_pixels = ndvi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, # of bands, and datatype
        ndvi_data = driver.Create(outfile_name, x_pixels,
                                  y_pixels, 1, gdal.GDT_Byte)

        # Set NDVI array as the 1 output raster band
        ndvi_data.GetRasterBand(1).WriteArray(ndvi_treshold)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = red_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = red_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        ndvi_data.SetGeoTransform(geotrans)
        ndvi_data.SetProjection(proj)
        ndvi_data.FlushCache()
        ndvi_data = None


if __name__ == '__main__':

    path = input(
        "Enter the path where the images will be searched to filter according to a specific NDVI value range: ")

    filter_ndvi_values(path)

