# Script para calcular el Kernel Normalized Difference Vegetation Index (kNDVI) de todos las imagenes de Sentinel-2 sin correccion atmosferica (.jp2)
# o con correccion atmosferica .tif
# La formula del kNDVI = tanh(NDVI*NDVI)

# Import libraries
import glob
import numpy as np
import re
import os
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version


# Define a function to calculate kNDVI values
def kndvi(red, nir):
    try:
        ndvi = ((nir - red)/(nir + red))
        ndvi_2 = ndvi * ndvi
        kndvi_val = np.tanh(ndvi_2)
        return kndvi_val

    except Exception as e:
        print("Error: " + str(e))


def calculate_kNDVI(path):
    print("Running kNDVI index...")

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

        # Call the ndvi() function on red, NIR bands
        kndvi2 = kndvi(red, nir)

        # Create output filename based on input name
        outfile_name = red_files[i].split('_B')[0] + '_kNDVI.tif'

        x_pixels = kndvi2.shape[0]  # number of pixels in x
        y_pixels = kndvi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, # of bands, and datatype
        kndvi_data = driver.Create(outfile_name, x_pixels,
                                   y_pixels, 1, gdal.GDT_Float32)

        # Set kNDVI array as the 1 output raster band
        kndvi_data.GetRasterBand(1).WriteArray(kndvi2)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = red_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = red_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        kndvi_data.SetGeoTransform(geotrans)
        kndvi_data.SetProjection(proj)
        kndvi_data.FlushCache()
        kndvi_data = None


if __name__ == "__main__":
    path = input(
        "Introduce la ruta donde se van a buscar los archivos de Acolite para calcular el kNDVI: ")

    calculate_kNDVI(path)
