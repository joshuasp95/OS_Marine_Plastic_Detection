# Script para calcular el Floating Debris Index (FDI) de todos las imagenes de Sentinel-2 sin correccion atmosferica (.jp2)
# o con correccion atmosferica .tif
# La formula del FDI = (nir - (re2 + (swir - re2) * ((833-665)/(1614-665) * 10)))

# Import libraries
import glob
import os
from osgeo import gdal  # If GDAL doesn't recognize jp2 format, check version
import re


# Para las imagenes originales es necesario resamplear los archivos a 20 m para que tengan la misma
# resolucion que las demas bandas(10m)
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


# Define a function to calculate FDI values
def fdi(re2, nir, swir):
    cte = (833-665)/(1614-665)
    print('cte', cte)
    try:
        print('op = ', (nir - (re2 + (swir - re2) * cte * 10)))
        return (nir - (re2 + (swir - re2) * cte * 10))
    except Exception as e:
        print("Error: " + str(e))


def calculate_fdi(path):
    print("Running FDI index...")

    # Set input directory
    in_dir = path

    # Regex para capturar las bandas y sus extensiones
    pattern = re.compile(r'.*_(B\d{2})_\d+m\.tif$|.*_(B\d{2})\.jp2$')

    # Obtenemos listas conteniendo cada banda que se recorrera en bucle posteriormente
    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(
        band) and 'B04' in band]

    re2_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    re2_files = [band for band in re2_files if pattern.match(
        band) and 'B06' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and 'B08' in band]

    swir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    swir_files = [band for band in swir_files if pattern.match(
        band) and 'B11' in band]

    print(red_files)
    print(re2_files)
    print(nir_files)
    print(swir_files)

    re2_files = resamplear_20_to_10(re2_files)
    swir_files = resamplear_20_to_10(swir_files)

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

        print('red', red)
        print('re2', re2)
        print('nir', nir)
        print('swir', swir)

        # Call the fdi() function on red, Red Edge 2, NIR and SWIR bands
        fdi2 = fdi(re2, nir, swir)
        print(fdi2)

        # Create output filename based on input name
        outfile_name = red_files[i].split('_B')[0] + '_FDI.tif'

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
        "Introduce la ruta donde se van a buscar los .jp2 originales para calcular el FDI: ")

    calculate_fdi(path)
