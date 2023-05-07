# Script para filtrar según el valor del Plastic Index (PI) los tif generados por PI.py
# Según el estudio realizado en Chipre los valores deberian ser 0.39 a 0.42

# Import libraries
import glob
import os
import re
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version


# Define a function to calculate plastic index using band arrays for red, NIR bands
def pi(red, nir):
    return (nir/(nir + red))


def filter_pi_values(path):
    print("Filtering PI values...")

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

    print('red_files', red_files)
    print('nir_files', nir_files)

    for i in range(len(red_files)):

        # Open each band using gdal
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])

        # read in each band as array and convert to float for calculations
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the ndvi() function on red, NIR bands
        pi2 = pi(red, nir)

        # Nombre de salida
        outfile_name = red_files[i].split('_B')[0] + '_PI_Filtered.tif'

        # Matriz booleana
        pi_mask = (pi2 >= 0.424) & (pi2 <= 0.477)

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
        "Introduce la ruta donde se van a buscar las imagenes para filtrar según un rango determinado los valores de PI: ")

    filter_pi_values(path)
