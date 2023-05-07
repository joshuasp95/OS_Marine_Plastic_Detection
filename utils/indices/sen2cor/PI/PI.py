# Script para calcular el Plastic Index (PI) de todos las imagenes de Sentinel-2 sin correccion atmosferica (.jp2)
# o con correccion atmosferica .tif
# La formula del PI = NIR/(NIR+RED)

# Import libraries
import glob
import os
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version
import re


# Define a function to calculate plastic index using band arrays for red, NIR bands
def pi(red, nir):
    try:
        return (nir/(nir + red))
    except Exception as e:
        print("Error: " + str(e))


def calculate_PI(path):
    print("Running PI index...")

    # Set input directory
    in_dir = path

    # Regex para capturar las bandas y sus extensiones
    pattern = re.compile(r'.*_(B\d{2})_\d+m\.tif$|.*_(B\d{2})\.jp2$')

    # Obtenemos listas conteniendo cada banda que se recorrera en bucle posteriormente
    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(
        band) and 'B04' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and 'B08' in band]

    print(red_files)
    print(nir_files)


    for i in range(len(red_files)):

        # Open each band using gdal
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])

        # read in each band as array and convert to float for calculations
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the pi() function on red, NIR bands
        pi2 = pi(red, nir)

        # Create output filename based on input name
        outfile_name = red_files[i].split('_B')[0] + '_PI.tif'

        x_pixels = pi2.shape[0]  # number of pixels in x
        y_pixels = pi2.shape[1]  # number of pixels in y

        try:
            # Set up output GeoTIFF
            driver = gdal.GetDriverByName('GTiff')

            # Create driver using output filename, x and y pixels, # of bands, and datatype
            pi_data = driver.Create(outfile_name, x_pixels,
                                    y_pixels, 1, gdal.GDT_Float32)

            # Set PI array as the 1 output raster band
            pi_data.GetRasterBand(1).WriteArray(pi2)

            # Setting up the coordinate reference system of the output GeoTIFF
            geotrans = red_link.GetGeoTransform()  # Grab input GeoTranform information
            proj = red_link.GetProjection()  # Grab projection information from input file

            # now set GeoTransform parameters and projection on the output file
            pi_data.SetGeoTransform(geotrans)
            pi_data.SetProjection(proj)
            pi_data.FlushCache()
            pi_data = None

        except Exception as e:
            print("Error creating output file: " + str(e))


if __name__ == '__main__':

    path = input(
        "Introduce la ruta donde se van a buscar los .jp2 o .tif de Sentinel2 para calcular el PI: ")

    calculate_PI(path)
