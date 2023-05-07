# Script para filtrar según el valor del kNDVI los tif generados por kNDVI.py
# Mirar estudios para filtrar por los valores de kNDVI que tenga el plastico o dejar fuera
# (e.j kNDVI > -0.2 & 0.2 < kNDVI )

# Import libraries
import glob
import os
import re
import numpy as np
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version


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

    # Regex para capturar las bandas y sus extensiones
    pattern = re.compile(r'.*_(B\d{2})_\d+m\.tif$|.*_(B\d{2})\.jp2$')

    # Obtenemos listas conteniendo cada banda que se recorrera en bucle posteriormente
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

        # read in each band as array and convert to float for calculations
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the ndvi() function on red, NIR bands
        kndvi2 = kndvi(red, nir)

        # Nombre de salida
        outfile_name = red_files[i].split('_B')[0] + '_kNDVI_Filtered.tif'

        # Matriz booleana
        kndvi_mask = (kndvi2 >= 0.005) & (kndvi2 <= 0.032)

        # Convertir matriz a mascara
        kndvi_treshold = kndvi_mask.astype(int)

        x_pixels = kndvi2.shape[0]  # number of pixels in x
        y_pixels = kndvi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, # of bands, and datatype
        kndvi_data = driver.Create(outfile_name, x_pixels,
                                y_pixels, 1, gdal.GDT_Byte)

        # Set kNDVI array as the 1 output raster band
        kndvi_data.GetRasterBand(1).WriteArray(kndvi_treshold)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = red_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = red_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        kndvi_data.SetGeoTransform(geotrans)
        kndvi_data.SetProjection(proj)
        kndvi_data.FlushCache()
        kndvi_data = None


if __name__ == '__main__':

    path = input(
        "Introduce la ruta donde se van a buscar las imagenes para filtrar según un rango determinado los valores de kNDVI: ")

    filter_kndvi_values(path)
