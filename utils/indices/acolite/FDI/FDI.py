# Script para calcular el Floating Debris Index (FDI) de todos las imagenes de Sentinel-2 con correccion atmosferica (rhos)
# .tif de Acolite
# La formula del FDI = (nir - (re2 + (swir - re2) * ((833-665)/(1614-665) * 10)))

# Import libraries
import glob
import os
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version
import re


# Define a function to calculate FDI values
def fdi(re2, nir, swir):
    cte = (833-665)/(1614-665)
    try:
        return (nir - (re2 + (swir - re2) * (cte * 10)))
    except Exception as e:
        print("Error: " + str(e))


def calculate_fdi(path):
    print("Running FDI index...")

    # Set input directory
    in_dir = path

    # Regex para capturar las bandas y sus extensiones
    pattern = re.compile(r'.*[\\\/].*(665|739|740|833|1610|1614)\.tif$')

    # Obtenemos listas conteniendo cada banda que se recorrera en bucle posteriormente
    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(
        band) and '665' in band]

    re2_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    re2_files = [band for band in re2_files if pattern.match(
        band) and ('740' in band or '739' in band)]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and '833' in band]

    swir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    swir_files = [band for band in swir_files if pattern.match(
        band) and ('1614' in band or '1610' in band)]

    print(red_files)
    print(re2_files)
    print(nir_files)
    print(swir_files)

    for i in range(len(red_files)):

        # Open each band using gdal
        red_link = gdal.Open(red_files[i])
        re2_link = gdal.Open(re2_files[i])
        nir_link = gdal.Open(nir_files[i])
        swir_link = gdal.Open(swir_files[i])

        # read in each band as array and convert to float for calculations
        red = red_link.ReadAsArray().astype(float)
        re2 = re2_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)
        swir = swir_link.ReadAsArray().astype(float)

        # Call the fdi() function on red, Red Edge 2, NIR and SWIR bands
        fdi2 = fdi(re2, nir, swir)

        # Create output filename based on input name
        outfile_name = red_files[i].split('_L')[0] + '_FDI.tif'
        print('***, outfile name: ', outfile_name)

        x_pixels = fdi2.shape[0]  # number of pixels in x
        y_pixels = fdi2.shape[1]  # number of pixels in y

        try:
            # Set up output GeoTIFF
            driver = gdal.GetDriverByName('GTiff')

            # Create driver using output filename, x and y pixels, # of bands, and datatype
            fdi_data = driver.Create(outfile_name, x_pixels,
                                     y_pixels, 1, gdal.GDT_Float32)

            # Set FDI array as the 1 output raster band
            fdi_data.GetRasterBand(1).WriteArray(fdi2)

            # Setting up the coordinate reference system of the output GeoTIFF
            geotrans = red_link.GetGeoTransform()  # Grab input GeoTranform information
            proj = red_link.GetProjection()  # Grab projection information from input file

            # now set GeoTransform parameters and projection on the output file
            fdi_data.SetGeoTransform(geotrans)
            fdi_data.SetProjection(proj)
            fdi_data.FlushCache()
            fdi_data = None

        except Exception as e:
            print("Error creating output file: " + str(e))


if __name__ == '__main__':

    path = input(
        "Introduce la ruta donde se van a buscar los .tif de acolite (rhos) para calcular el FDI: ")

    calculate_fdi(path)
