# Script to resample Sentinel-2 images to 10 meters using gdal library
from osgeo import gdal
import matplotlib.pyplot as plt
import os


def resample_to_10m(source_dir):

    # Get the path to the directory with the sen2cor .tif files
    folder_path = source_dir

    # Define the resampling parameters
    x_res = 10
    y_res = 10

    # Create the directory where the resampled files will be stored
    output_dir = os.path.join(folder_path, 'Sen2Cor_10m_Resampled')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over each .tif file inside the folder with all the sen2cor generated .tif files
    for root, dirs, files in os.walk(folder_path):
        if 'IMG_DATA' in root:
            for file in files:
                # Filter by .tif files
                if file.endswith(".tif"):
                    # Absolute path of each .tif file that will be resampled
                    tif_path = os.path.join(root, file)
                    print('tif_path: ', tif_path)
                    # Open the file with gdal library
                    ds = gdal.Open(tif_path)
                    # Resample defining the resampling algorithm and output directory
                    dsRes = gdal.Warp(os.path.join(folder_path, 'Sen2Cor_10m_Resampled', 'resampled_'+file), ds, xRes=x_res, yRes=y_res,
                                      resampleAlg="near")

                    # To visualize the resampling results
                    # array = ds.GetRasterBand(1).ReadAsArray()
                    # plt.figure()
                    # plt.imshow(array)
                    # plt.colorbar()
                    # plt.show()

                    # Check the generated results in the console
                    print(dsRes.GetGeoTransform())
                    print(dsRes.GetProjection())

                    # Close the datasets
                    ds = dsRes = None
    return output_dir
