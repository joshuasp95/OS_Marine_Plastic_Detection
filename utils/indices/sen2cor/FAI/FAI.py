# Script to calculate the Floating Algae Index (FAI) of Sentinel-2 images with atmospheric correction (rhos)
# using Acolite .tif files
# The formula for FAI = (nir - (red + (swir - red) * ((833-665)/(1614-665))))

# Import libraries
import glob
import os
from osgeo import gdal  
import re


# Resample the original images to 20m resolution to match other bands (10m)
def resampler(file, folderpath):

    path = file

    ds = gdal.Open(path)

    # Resample
    dsRes = gdal.Warp(os.path.join(folderpath + '_resampled.tif'), ds, xRes=10, yRes=10,
                      resampleAlg="near")

    array = ds.GetRasterBand(1).ReadAsArray()
    print('array', array)

    print(dsRes.GetGeoTransform())
    print(dsRes.GetProjection())

    ds = dsRes = None

    return os.path.join(folderpath + '_resampled.tif')


def resample_20_to_10(files):
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


def calculate_fai(path):
    print("Running FAI index...")

    # Set input directory
    in_dir = path

    # Regex to capture the bands and their extensions
    pattern = re.compile(r'.*_(B\d{2})_\d+m\.tif$|.*_(B\d{2})\.jp2$')

    # Get lists containing each band that will be iterated over later
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

    swir_files = resample_20_to_10(swir_files)

    for i in range(len(red_files)):

        # Open each band using GDAL
        red_link = gdal.Open(red_files[i])
        nir_link = gdal.Open(nir_files[i])
        swir_link = gdal.Open(swir_files[i])

        # Read each band as an array and convert it to float for calculations
        red = red_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)
        swir = swir_link.ReadAsArray().astype(float)

        print('red', red)
        print('nir', nir)
        print('swir', swir)

        # Call the fai() function on red, NIR, and SWIR bands
        fai2 = fai(red, nir, swir)
        print(fai2)

        # Create an output filename based on the input name
        outfile_name = red_files[i].split('_B')[0] + '_FAI.tif'

        x_pixels = fai2.shape[0]  # number of pixels in x
        y_pixels = fai2.shape[1]  # number of pixels in y

        try:
            # Set up output GeoTIFF
            driver = gdal.GetDriverByName('GTiff')

            # Create a driver using the output filename, x and y pixels, number of bands, and datatype
            fai_data = driver.Create(outfile_name, x_pixels,
                                     y_pixels, 1, gdal.GDT_Float32)

            # Set the FAI array as the 1 output raster band
            fai_data.GetRasterBand(1).WriteArray(fai2)

            # Setting up the coordinate reference system of the output GeoTIFF
            geotrans = red_link.GetGeoTransform()  # Grab input GeoTransform information
            proj = red_link.GetProjection()  # Grab projection information from the input file

            # Now set GeoTransform parameters and projection on the output file
            fai_data.SetGeoTransform(geotrans)
            fai_data.SetProjection(proj)
            fai_data.FlushCache()
            fai_data = None

        except Exception as e:
            print("Error creating output file: " + str(e))


if __name__ == '__main__':
    path = input(
        "Enter the path where the original .jp2 files are located to calculate the FAI: ")

    calculate_fai(path)
