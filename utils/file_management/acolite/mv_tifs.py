# Script to move all resampled tif files to folders according to the capture date
# of the image or images (since there may be 2 cells for the same day, in which case
# a mosaic would have to be made)
import os
import shutil
import re


def get_date(file):
    # Get the date string
    year = file.split('_')[2]
    month = file.split('_')[3]
    day = file.split('_')[4]
    # Directory name
    name_dir = month + "_" + day + "_" + year
    return name_dir


def run(path):

    source_dir = path

    print("Acolite tifs will be moved to the created folders in the path {}".format(path))

    # Regex to filter tif images from settings and logs
    pattern = re.compile('S2.*')

    # Get the folders in a list
    dirs = []

    for file in os.listdir(source_dir):
        if os.path.isdir(os.path.join(source_dir, file)):
            dirs.append(file)

    # Now move the files into the directories
    for file in os.listdir(source_dir):
        if pattern.match(file):
            name_dir = get_date(file)
            # Loop through the folders to filter files by the date of the directory
            for date_dir in dirs:
                if name_dir == date_dir:
                    date_dir_path = os.path.join(source_dir, date_dir)
                    old_dir = os.path.join(source_dir, file)
                    shutil.move(old_dir, date_dir_path)


if __name__ == '__main__':
    # Path where the directories based on acolite dates will be searched to move the tifs inside
    path = input(
        'Enter the path where the directories to organize the acolite tifs will be searched: ')
    run(path)
