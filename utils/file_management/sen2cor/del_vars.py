# Script to remove specific tifs from sen2cor resampled outputs ...
# These specific tifs are SCL --> Scene Classification, TCI --> True Color Image, WVP --> Water Vapour.

# Additional outputs are an Aerosol Optical Thickness (AOT) map, a Water Vapour (WV) map and a Scene Classification (SCL) map together with Quality Indicators (QI) for cloud and snow probabilities at 60 m resolution. Level-2A output image products are resampled and generated with an equal spatial resolution for all bands (10 m, 20 m or 60 m).
# Standard distributed products contain the envelope of all resolutions in three distinct folders:

# 10 m: containing spectral bands 2, 3, 4 , 8, a True Colour Image (TCI) and an AOT and WVP maps resampled from 20 m.
# 20 m: containing spectral bands 1 - 7, the bands 8A, 11 and 12, a True Colour Image (TCI), a Scene Classification (SCL) map and an AOT and WVP map.
# The band B8 is omitted as B8A provides more precise spectral information.
# 60 m: containing all components of the 20 m product resampled to 60 m and additionally the bands 1 and 9, a True Colour Image (TCI), a Scene Classification (SCL) map and an AOT and WVP map. The cirrus band 10 is omitted, as it does not contain surface information.

# ref --> https://sentinel.esa.int/web/sentinel/user-guides/sentinel-2-msi/processing-levels/level-2
import os
import re


def delete_file(file_path):
    print(file_path)
    if os.path.exists(file_path):
        print(f"File with path {file_path} exists")
        if os.path.isdir(file_path):
            print(
                f"File is a directory, cannot be deleted!")
        elif os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"File deleted {file_path}")
            except OSError as e:
                print("Error removing: %s - %s" % (e.filename, e.strerror))
    else:
        print(f"File with path {file_path} does not exist")


def run(path):

    source_dir = path
    print(f"Deleting sen2cor AOT, TCI, SCL files in {source_dir}")

    # Filter with sen2cor regex for its files
    pattern = re.compile('B.*')

    for file in os.listdir(source_dir):
        if file.endswith(".tif"):
            if not pattern.match(file.split('_')[3]):
                file_path = os.path.join(source_dir, file)
                delete_file(file_path)


if __name__ == '__main__':
    # Path where to look for sen2cor files to delete
    path = input(
        'Enter the path where sen2cor files to delete are located: ')
    run(path)
