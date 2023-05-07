# Script to move all resampled tif files to folders according to their capture date
# (there may be 2 cells for the same day, so a mosaic may need to be performed)

import os
import shutil


def get_date(file):
    # Get the date string
    # ! Special regex for sen2cor
    date_string = file.split('_')[2]
    date = date_string[:8]
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    # Folder name
    folder_name = month + "_" + day + "_" + year
    return folder_name


def run(path):

    source_dir = path

    print("Sen2cor tif files will be moved to the folders created in {}".format(path))

    # No need for regex because there are only tifs

    # Get the folders in a list
    dirs = []

    for file in os.listdir(source_dir):
        if os.path.isdir(os.path.join(source_dir, file)):
            dirs.append(file)

    # Now move the files into the directories
    for file in os.listdir(source_dir):
        if file.endswith('.tif'):
            folder_name = get_date(file)
            for date_dir in dirs:
                if folder_name == date_dir:
                    date_dir_path = os.path.join(source_dir, date_dir)
                    old_dir = os.path.join(source_dir, file)
                    shutil.move(old_dir, date_dir_path)


if __name__ == "__main__":
    # Path where to look for sen2cor date-based folders to move the tifs inside
    path = input(
        'Enter the path where to look for the directories to organize sen2cor tifs: ')
    run(path)

