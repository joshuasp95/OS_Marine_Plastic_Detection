# Script to create and organize tif files in folders according to the capture date
# of the image or images (since there may be 2 cells for the same day, in which case
# a mosaic would have to be made)

import os
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

    print("Directories will be created to distribute the acolite tifs by date in the path {}".format(source_dir))

    pattern = re.compile('S2.*')

    # Create the directories
    for file in os.listdir(source_dir):
        if pattern.match(file):
            name_dir = get_date(file)
            # Try to create directories if they don't exist
            if not os.path.exists(os.path.join(source_dir, name_dir)):
                os.makedirs(os.path.join(source_dir, name_dir))


if __name__ == '__main__':
    # Path where the directories based on acolite dates will be created
    path = input(
        'Enter the path where the directories with acolite dates will be created: ')
    run(path)
