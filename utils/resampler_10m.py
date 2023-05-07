from osgeo import gdal
import os


def run(file, folderpath):

    print(file, folderpath)

    path = file

    ds = gdal.Open(path)

    # resample

    dsRes = gdal.Warp(os.path.join(folderpath + '_resampled.tif'), ds, xRes=10, yRes=10,
                      resampleAlg="near")

    # visualize
    array = ds.GetRasterBand(1).ReadAsArray()
    # plt.figure()
    # plt.imshow(array)
    # plt.colorbar()
    # plt.show()
    print(dsRes.GetGeoTransform())
    print(dsRes.GetProjection())

    # close your datasets!
    ds = dsRes = None

    return os.path.join(folderpath + '_resampled.tif')


if __name__ == '__main__':
    # file = input("Introduce el archivo para resamplear a 10 m de resolucion: ")
    run()
