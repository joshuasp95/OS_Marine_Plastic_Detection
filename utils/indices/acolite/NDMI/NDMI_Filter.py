# Script para filtrar según el valor del NDMI los tif generados por NDMI.py
# Mirar estudios para filtrar por los valores de NDMI que tenga el plastico o dejar fuera (e.j 0.1 < NDMI)

# Import libraries
import glob
import os
import re
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version


# Define a function to calculate NDMI values
def ndmi(swir, nir):
    try:
        return ((nir-swir)/(nir + swir))
    except Exception as e:
        print("Error: " + str(e))


def filter_ndmi_values(path):
    print("Filtering NDMI values...")

    # Set input directory
    in_dir = path

    # Regex para capturar las bandas y sus extensiones
    pattern = re.compile(r'.*[\\\/].*(833|1610|1614)\.tif$')

    # Obtenemos listas conteniendo cada banda que se recorrera en bucle posteriormente
    swir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    swir_files = [band for band in swir_files if pattern.match(
        band) and ('1614' in band or '1610' in band)]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and '833' in band]

    for i in range(len(swir_files)):

        # Open each band using gdal
        swir_link = gdal.Open(swir_files[i])
        nir_link = gdal.Open(nir_files[i])

        # read in each band as array and convert to float for calculations
        swir = swir_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the ndmi() function on swir, NIR bands
        ndmi2 = ndmi(swir, nir)

        # Nombre de salida
        outfile_name = swir_files[i].split('_L')[0] + '_NDMI_Filtered.tif'

        # Matriz booleana
        ndmi_mask = (ndmi2 >= -0.4) & (ndmi2 <= 0.4)

        # Convertir matriz a mascara
        ndmi_treshold = ndmi_mask.astype(int)

        x_pixels = ndmi2.shape[0]  # number of pixels in x
        y_pixels = ndmi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, # of bands, and datatype
        ndmi_data = driver.Create(outfile_name, x_pixels,
                                  y_pixels, 1, gdal.GDT_Byte)

        # Set NDMI array as the 1 output raster band
        ndmi_data.GetRasterBand(1).WriteArray(ndmi_treshold)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = swir_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = swir_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        ndmi_data.SetGeoTransform(geotrans)
        ndmi_data.SetProjection(proj)
        ndmi_data.FlushCache()
        ndmi_data = None


if __name__ == '__main__':

    path = input(
        "Introduce la ruta donde se van a buscar las imagenes para filtrar según un rango determinado los valores de NDMI: ")

    filter_ndmi_values(path)
