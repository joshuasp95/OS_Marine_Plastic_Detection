# Script para filtrar según el valor del NDVI los tif generados por NDVI.py
# Mirar estudios para filtrar por los valores de NDVI que tenga el plastico o dejar fuera (e.j 0.4 < NDVI)

# Import libraries
import glob
import os
import re
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version


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
        ndvi2 = ndvi(red, nir)

        # Nombre de salida
        outfile_name = red_files[i].split('_B')[0] + '_NDVI_Filtered.tif'

        # Matriz booleana
        ndvi_mask = (ndvi2 >= -0.153) & (ndvi2 <= -0.046)

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
        "Introduce la ruta donde se van a buscar las imagenes para filtrar según un rango determinado los valores de NDVI: ")

    filter_ndvi_values(path)
