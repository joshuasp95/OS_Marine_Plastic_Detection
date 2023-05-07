# Import libraries
import glob
import os
import re
from osgeo import gdal  


# Define a function to calculate plastic index using band arrays for red, NIR bands
def pi(red, nir):
    return (nir/(nir + red))


def filter_pi_values(path):
    print("Filtering PI values...")

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

        # Call the pi() function on red, NIR bands
        pi2 = pi(red, nir)

        outfile_name = red_files[i].split('_L')[0] + '_PI_Filtered.tif'

        # Boolean mask
        pi_mask = (pi2 >= 0.35) & (pi2 <= 0.45)

        # Convertir matriz a mascara
        pi_treshold = pi_mask.astype(int)

        x_pixels = pi2.shape[0]  # number of pixels in x
        y_pixels = pi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, # of bands, and datatype
        pi_data = driver.Create(outfile_name, x_pixels,
                                y_pixels, 1, gdal.GDT_Byte)

        # Set PI array as the 1 output raster band
        pi_data.GetRasterBand(1).WriteArray(pi_treshold)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = red_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = red_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        pi_data.SetGeoTransform(geotrans)
        pi_data.SetProjection(proj)
        pi_data.FlushCache()
        pi_data = None


if __name__ == '__main__':

    path = input(
        "Enter the path where the images will be searched to filter according to a specific PI value range: ")

    filter_pi_values(path)

