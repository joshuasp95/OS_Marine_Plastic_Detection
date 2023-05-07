# Script para filtrar según el valor del FAI los tif generados por FAI.py
# Mirar estudios para filtrar por los valores de FAI que tenga el plastico o dejar fuera
# (e.j FAI > 0.02 & FAI < 0.06)

# Import libraries
import glob
import os
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version
import re


# Para las imagenes originales es necesario resamplear los archivos SWIR para que tengan la misma
# resolucion que las demas bandas
def resampler(file, folderpath):

    path = file

    ds = gdal.Open(path)

    # resample
    dsRes = gdal.Warp(os.path.join(folderpath + '_resampled.tif'), ds, xRes=10, yRes=10,
                      resampleAlg="near")

    array = ds.GetRasterBand(1).ReadAsArray()
    print('array', array)

    print(dsRes.GetGeoTransform())
    print(dsRes.GetProjection())

    ds = dsRes = None

    return os.path.join(folderpath + '_resampled.tif')


def resamplear_20_to_10(files):
    files_res = []
    for file in files:
        if file.endswith('.jp2'):
            file_name = file.split('.jp2')[0]
            files_res.append(resampler(file, file_name))
        else:
            return files
    return files_res


# Define a function to calculate FAI values
def fai(red, nir, swir):
    cte = (833-665)/(1614-665)
    try:
        return (nir - (red + (swir - red) * cte))
    except Exception as e:
        print("Error: " + str(e))


def filter_fai_values(path):
    print("Filtering FAI values...")

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

    swir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    swir_files = [band for band in swir_files if pattern.match(
        band) and 'B11' in band]

    print(red_files)
    print(nir_files)
    print(swir_files)

    swir_files = resamplear_20_to_10(swir_files)

    for i in range(len(red_files)):

        # Open each band using gdal
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])
        swir_link = gdal.Open(swir_files[i])

        # read in each band as array and convert to float for calculations
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)
        swir = swir_link.ReadAsArray().astype(float)

        # Call the fdi() function on red, NIR and SWIR bands
        fai2 = fai(red, nir, swir)

        # Create output filename based on input name
        outfile_name = red_files[i].split('_B')[0] + '_FAI_Filtered.tif'

        # Matriz booleana
        fai_mask = (fai2 >= -0.0038) & (fai2 <= 0.0123)

        # Convertir matriz a mascara
        fai_treshold = fai_mask.astype(int)

        x_pixels = fai2.shape[0]  # number of pixels in x
        y_pixels = fai2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using output filename, x and y pixels, # of bands, and datatype
        fai_data = driver.Create(outfile_name, x_pixels,
                                 y_pixels, 1, gdal.GDT_Float32)

        # Set FDI array as the 1 output raster band
        fai_data.GetRasterBand(1).WriteArray(fai_treshold)

        # Setting up the coordinate reference system of the output GeoTIFF
        geotrans = red_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = red_link.GetProjection()  # Grab projection information from input file

        # now set GeoTransform parameters and projection on the output file
        fai_data.SetGeoTransform(geotrans)
        fai_data.SetProjection(proj)
        fai_data.FlushCache()
        fai_data = None


if __name__ == '__main__':

    path = input(
        "Introduce la ruta donde se van a buscar las imagenes para filtrar según un rango determinado los valores de FAI: ")

    filter_fai_values(path)
