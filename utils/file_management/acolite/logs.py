# Script to store logs in their corresponding folder
import os
import re
import shutil


def run(path):

    source_dir = path

    print("A directory to store logs will be created in the following path {}".format(source_dir))

    # Regex for settings
    pattern = re.compile('.*log.*')

    # Output directory
    name_dir = "Logs"

    # Try to create it if it does not exist
    if not os.path.exists(os.path.join(source_dir, name_dir)):
        os.makedirs(os.path.join(source_dir, name_dir))

    # Move the files
    for file in os.listdir(source_dir):
        if pattern.match(file):
            settings_path = os.path.join(source_dir, name_dir)
            old_dir = os.path.join(source_dir, file)
            shutil.move(old_dir, settings_path)


if __name__ == '__main__':
    # Path where the output directory for storing logs will be created, and where
    # the logs will be moved
    path = input(
        'Enter the path where the directory to store logs will be created: ')
    run(path)
