# Script to calculate the Floating Debris Index (FDI) of Sentinel-2 images with atmospheric correction (rhos)
# using Acolite .tif files
# The formula for FDI = (nir - (re2 + (swir - re2) * ((833-665)/(1614-665) * 10)))

# Import libraries
import glob
import os
from osgeo import gdal  
import re


# Resample the SWIR files to match the resolution of other bands in the original images
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

    # Regex to capture the bands and their extensions
    pattern = re.compile(r'.*_(B\d{2})_\d+m\.tif$|.*_(B\d{2})\.jp2$')

    # Get lists containing each band that will be iterated over later
    red_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    red_files = [band for band in red_files if pattern.match(band) and 'B04' in band]

    re2_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    re2_files = [band for band in re2_files if pattern.match(band) and 'B06' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(band) and 'B08' in band]

    swir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    swir_files = [band for band in swir_files if pattern.match(band) and 'B11' in band]

    print(red_files)
    print(re2_files)
    print(nir_files)
    print(swir_files)

    re2_files = resample_20_to_10(re2_files)
    swir_files = resample_20_to_10(swir_files)

    for i in range(len(red_files)):

        # Open each band using GDAL
        red_link = gdal.Open(red_files[i])
        re2_link = gdal.Open(re2_files[i])
        nir_link = gdal.Open(nir_files[i])
        swir_link = gdal.Open(swir_files[i])

        # Read each band as an array and convert it to float for calculations
        re2 = re2_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)
        swir = swir_link.ReadAsArray().astype(float)

        # Call the fdi() function on red, Red Edge 2, NIR, and SWIR bands
        fdi2 = fdi(re2, nir, swir)

        # Create the output filename based on the input name
        outfile_name = red_files[i].split('_B')[0] + '_FDI_Filtered.tif'

        # Boolean matrix
        fdi_mask = (fdi2 >= 0.01) & (fdi2 <= 0.11)

        # Convert the matrix to a mask
        fdi_threshold = fdi_mask.astype(int)

        x_pixels = fdi2.shape[0]  # number of pixels in x
        y_pixels = fdi2.shape[1]  # number of pixels in y

        # Set up the output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create a driver using the output filename, x and y pixels, number of bands, and datatype
        fdi_data = driver.Create(outfile_name, x_pixels, y_pixels, 1, gdal.GDT_Float32)

        # Set the FDI array as the 1 output raster band
        fdi_data.GetRasterBand(1).WriteArray(fdi_threshold)

        # Set up the coordinate reference system of the output GeoTIFF
        geotrans = red_link.GetGeoTransform()  # Grab input GeoTransform information
        proj = red_link.GetProjection()  # Grab projection information from the input file

        # Set GeoTransform parameters and projection on the output file
        fdi_data.SetGeoTransform(geotrans)
        fdi_data.SetProjection(proj)
        fdi_data.FlushCache()
        fdi_data = None


if __name__ == '__main__':

    path = input("Enter the path where the images are located to filter the FDI values within a specified range: ")

    calculate_fdi(path)

