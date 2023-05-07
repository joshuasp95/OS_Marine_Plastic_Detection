# Script to create and organize by folders all resampled tifs according to their image capture date
# (since there may be 2 cells for the same day, which would require a mosaic)

import os


def get_date(file):
    # Get the string with the dates
    # ! Special regex for sen2cor
    date_str = file.split('_')[2]
    date = date_str[:8]
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    # Directory name
    dir_name = month + "_" + day + "_" + year
    return dir_name


def run(path):

    source_dir = path

    print("Creating directories to distribute sen2cor resampled tifs by their capture date in the path {}".format(source_dir))

    # Create the directories
    for file in os.listdir(source_dir):
        dir_name = get_date(file)
        # Try to create the directories if they do not exist
        if not os.path.exists(os.path.join(source_dir, dir_name)):
            os.makedirs(os.path.join(source_dir, dir_name))
        else:
            print("Directory {} already exists".format(
                os.path.join(source_dir, dir_name)))


if __name__ == "__main__":
    # Path where to create the directories based on sen2cor dates
    path = input(
        'Enter the path where to create directories with sen2cor dates: ')
    run(path)
