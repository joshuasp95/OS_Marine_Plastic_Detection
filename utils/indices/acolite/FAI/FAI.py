# Script para calcular el Floating Algae Index (FAI) de todos las imagenes de Sentinel-2 con correccion atmosferica (rhos)
# .tif de Acolite
# La formula del FAI = (nir - (red + (swir - red) * ((833-665)/(1614-665))))

# Import libraries
import glob
import os
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version
import re


# Define a function to calculate FAI values
def fai(red, nir, swir):
    cte = (833-665)/(1614-665)
    try:
        return (nir - (red + (swir - red) * cte))
    except Exception as e:
        print("Error: " + str(e))


def calculate_fai(path):
    print("Running FAI index...")

    # Set input directory
    in_dir = path

    # Regex para capturar las bandas y sus extensiones
    pattern = re.compile(r'.*[\\\/].*(665|833|1610|1614)\.tif$')

    # Obtenemos listas conteniendo cada banda que se recorrera en bucle posteriormente
    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(
        band) and '665' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and '833' in band]

    swir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    swir_files = [band for band in swir_files if pattern.match(
        band) and ('1614' in band or '1610' in band)]

    print(red_files)
    print(nir_files)
    print(swir_files)

    for i in range(len(red_files)):

        # Open each band using gdal
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])
        swir_link = gdal.Open(swir_files[i])

        # read in each band as array and convert to float for calculations
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)
        swir = swir_link.ReadAsArray().astype(float)

        # Call the fai() function on red, NIR and SWIR bands
        fai2 = fai(red, nir, swir)

        # Create output filename based on input name
        outfile_name = red_files[i].split('_L')[0] + '_FAI.tif'

        x_pixels = fai2.shape[0]  # number of pixels in x
        y_pixels = fai2.shape[1]  # number of pixels in y

        try:
            # Set up output GeoTIFF
            driver = gdal.GetDriverByName('GTiff')

            # Create driver using output filename, x and y pixels, # of bands, and datatype
            fai_data = driver.Create(outfile_name, x_pixels,
                                     y_pixels, 1, gdal.GDT_Float32)

            # Set FAI array as the 1 output raster band
            fai_data.GetRasterBand(1).WriteArray(fai2)

            # Setting up the coordinate reference system of the output GeoTIFF
            geotrans = red_link.GetGeoTransform()  # Grab input GeoTranform information
            proj = red_link.GetProjection()  # Grab projection information from input file

            # now set GeoTransform parameters and projection on the output file
            fai_data.SetGeoTransform(geotrans)
            fai_data.SetProjection(proj)
            fai_data.FlushCache()
            fai_data = None

        except Exception as e:
            print("Error creating output file: " + str(e))


if __name__ == '__main__':

    path = input(
        "Introduce la ruta donde se van a buscar los .tif de acolite (rhos) para calcular el FAI: ")

    calculate_fai(path)
