# Script para filtrar según el valor del NDWI los tif generados por NDWI.py
# Mirar estudios para filtrar por los valores de NDWI que tenga el plastico o dejar fuera (e.j 0.3 < NDWI)

# Import libraries
import glob
import os
import re
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version


# Define a function to calculate NDWI values
def ndwi(green, nir):
    try:
        return ((green - nir)/(nir + green))
    except Exception as e:
        print("Error: " + str(e))


def filter_ndwi_values(path):
    print("Filtering NDWI values...")

    # Set input directory
    in_dir = path

    # Regex para capturar las bandas y sus extensiones
    pattern = re.compile(r'.*[\\\/].*(559|560|833)\.tif$')

    # Obtenemos listas conteniendo cada banda que se recorrera en bucle posteriormente
    green_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    green_files = [band for band in green_files if pattern.match(
        band) and ('559' in band or '560' in band)]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and '833' in band]

    for i in range(len(green_files)):

        # Open each band using gdal
        green_link = gdal.Open(green_files[i])
        nir_link = gdal.Open(nir_files[i])

        # read in each band as array and convert to float for calculations
        green = green_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the ndwi() function on green, NIR bands
        ndwi2 = ndwi(green, nir)

        # Nombre de salida
        outfile_name = green_files[i].split('_L')[0] + '_NDWI_Filtered.tif'

        # Matriz booleana
        ndwi_mask = (ndwi2 >= -0.4) & (ndwi2 <= 0.4)

        # Convertir matriz a mascara
        ndwi_treshold = ndwi_mask.astype(int)

        x_pixels = ndwi2.shape[0]  # number of pixels in x
        y_pixels = ndwi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, # of bands, and datatype
        ndwi_data = driver.Create(outfile_name, x_pixels,
                                  y_pixels, 1, gdal.GDT_Byte)

        # Set NDWI array as the 1 output raster band
        ndwi_data.GetRasterBand(1).WriteArray(ndwi_treshold)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = green_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = green_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        ndwi_data.SetGeoTransform(geotrans)
        ndwi_data.SetProjection(proj)
        ndwi_data.FlushCache()
        ndwi_data = None


if __name__ == '__main__':

    path = input(
        "Introduce la ruta donde se van a buscar las imagenes para filtrar según un rango determinado los valores de NDWI: ")

    filter_ndwi_values(path)
