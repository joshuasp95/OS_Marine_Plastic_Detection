# Script to store settings in their corresponding folder
import os
import re
import shutil


def run(path):

    source_dir = path

    print("A directory will be created to store settings in the following path {}".format(source_dir))

    # Regex for settings
    pattern = re.compile('.*settings.*')

    # Output directory
    name_dir = "Settings"

    # Try to create it if it doesn't exist
    if not os.path.exists(os.path.join(source_dir, name_dir)):
        os.makedirs(os.path.join(source_dir, name_dir))

    # Move the files
    for file in os.listdir(source_dir):
        if pattern.match(file):
            settings_path = os.path.join(source_dir, name_dir)
            old_dir = os.path.join(source_dir, file)
            shutil.move(old_dir, settings_path)


if __name__ == '__main__':
    # Path where the output directory will be created to store the settings and where
    # they will be moved
    path = input(
        'Enter the path where the directory to store the settings will be created: ')
    run(path)
