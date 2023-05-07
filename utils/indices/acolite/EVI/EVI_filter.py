# Script para filtrar según el valor del Enhanced Vegetation Index (EVI) los tif generados por EVI.py
# Mirar estudios para filtrar por los valores de EVI que tenga el plastico o dejar fuera
# (e.j EVI > -0.1 & EVI < 0.0)

# Import libraries
import glob
import os
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version
import re


# Define a function to calculate EVI values
def evi(blue, red, nir):
    try:
        return 2.5 * (nir - red) / (nir + 6*red - 7.5*blue + 1)
    except Exception as e:
        print("Error: " + str(e))


def filter_evi_values(path):
    print("Filtering EVI values...")

    # Set input directory
    in_dir = path

    # Regex para capturar las bandas y sus extensiones
    pattern = re.compile(r'.*[\\\/].*(492|665|833)\.tif$')

    # Obtenemos listas conteniendo cada banda que se recorrera en bucle posteriormente
    blue_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    blue_files = [band for band in blue_files if pattern.match(
        band) and '492' in band]

    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(
        band) and '665' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and '833' in band]

    print('blue_files', blue_files)
    print(len(blue_files))
    print('red_files', red_files)
    print(len(red_files))
    print('nir_files', nir_files)
    print(len(nir_files))

    for i in range(len(red_files)):
        
        # Open each band using gdal
        blue_link = gdal.Open(blue_files[i])
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])

        # read in each band as array and convert to float for calculations
        blue = blue_link.ReadAsArray().astype(float)
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)


        # Call the evi() function on blue, red, NIR  bands
        evi2 = evi(blue, red, nir)

        # Create output filename based on input name
        outfile_name = red_files[i].split('_L')[0] + '_EVI_Filtered.tif'

        # Matriz booleana
        evi_mask = (evi2 >= -0.0283) & (evi2 <= 0.0255)

        # Convertir matriz a mascara
        evi_treshold = evi_mask.astype(int)

        x_pixels = evi2.shape[0]  # number of pixels in x
        y_pixels = evi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, # of bands, and datatype
        evi_data = driver.Create(outfile_name, x_pixels,
                                 y_pixels, 1, gdal.GDT_Float32)

        # Set EVI array as the 1 output raster band
        evi_data.GetRasterBand(1).WriteArray(evi_treshold)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = red_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = red_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        evi_data.SetGeoTransform(geotrans)
        evi_data.SetProjection(proj)
        evi_data.FlushCache()
        evi_data = None


if __name__ == '__main__':

    path = input(
        "Introduce la ruta donde se van a buscar las imagenes para filtrar según un rango determinado los valores de EVI: ")

    filter_evi_values(path)
