# Script to calculate the Normalized Difference Moisture Index (NDMI) for all Sentinel-2 images without atmospheric correction (.jp2)
# or with atmospheric correction (.tif)
# The formula for NDMI is (nir-swir)/(swir+nir)

# Import libraries
import glob
import re
import os
from osgeo import gdal  


# Resample the original images to 20m resolution to match the resolution of the other bands (10m)
def resampler(file, folderpath):

    path = file

    ds = gdal.Open(path)

    # Resample
    dsRes = gdal.Warp(os.path.join(folderpath + '_resampled.tif'),
                      ds, xRes=10, yRes=10, resampleAlg="near")

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

# Define a function to calculate NDMI values


def ndmi(swir, nir):
    try:
        return ((nir-swir)/(nir + swir))
    except Exception as e:
        print("Error: " + str(e))


def calculate_NDMI(path):
    print("Running NDMI index...")

    # Set input directory
    in_dir = path

    # Regex to capture the bands and their extensions
    pattern = re.compile(r'.*_(B\d{2})_\d+m\.tif$|.*_(B\d{2})\.jp2$')

    # Get lists containing each band that will be iterated over later
    swir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    swir_files = [band for band in swir_files if pattern.match(
        band) and 'B11' in band]

    nir_files = glob.glob(os.path.join(in_dir, '**'), recursive=True)
    nir_files = [band for band in nir_files if pattern.match(
        band) and 'B08' in band]

    print(swir_files)
    print(nir_files)

    swir_files = resample_20_to_10(swir_files)

    for i in range(len(swir_files)):

        # Open each band using gdal
        swir_link = gdal.Open(swir_files[i])
        nir_link = gdal.Open(nir_files[i])

        # Read each band as an array and convert it to float for calculations
        swir = swir_link.ReadAsArray().astype(float)
        nir = nir_link.ReadAsArray().astype(float)

        # Call the ndmi() function on swir, NIR bands
        ndmi2 = ndmi(swir, nir)

        # Create output filename based on input name
        outfile_name = swir_files[i].split('_B')[0] + '_NDMI.tif'

        x_pixels = ndmi2.shape[0]  # number of pixels in x
        y_pixels = ndmi2.shape[1]  # number of pixels in y

        # Set up output GeoTIFF
        driver = gdal.GetDriverByName('GTiff')

        # Create driver using the output filename, x and y pixels, # of bands, and datatype
        ndmi_data = driver.Create(
            outfile_name, x_pixels, y_pixels, 1, gdal.GDT_Float32)

        # Set the NDMI array as the 1 output raster band
        ndmi_data.GetRasterBand(1).WriteArray(ndmi2)

        # Set up the coordinate reference system of the output GeoTIFF
        geotrans = swir_link.GetGeoTransform()  # Grab input GeoTranform information
        proj = swir_link.GetProjection()  # Grab projection information from the input file

        # Set the GeoTransform parameters and projection on the output file
        ndmi_data.SetGeoTransform(geotrans)
        ndmi_data.SetProjection(proj)
        ndmi_data.FlushCache()
        ndmi_data = None


if __name__ == "__main__":
    path = input(
        "Enter the path where the Acolite files are located to calculate the NDMI: ")

    calculate_NDMI(path)
