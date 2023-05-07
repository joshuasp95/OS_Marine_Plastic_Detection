# Script to remove all Sen2Cor-corrected .SAFE files except the 10m TCI (True Color Image),
# which will be moved to a new folder.

import os
import glob
import shutil

# Move 10m resolution TCIs to a new folder


def register_TCI(path):

    files = glob.glob(os.path.join(path, '**'), recursive=True)

    files = [
        res for res in files if 'TCI' in res and '_10m' in res and res.endswith('.tif')]

    i = 0

    TCI_files = []

    for file in files:
        i += 1
        print(file)
        TCI_files.append(file)

    print('totals:', i)
    print(TCI_files)
    print(len(TCI_files))
    return TCI_files


def move_TCI(TCI_files, path):
    dir_name = "TCI_10m"

    if not os.path.exists(os.path.join(path, dir_name)):
        os.makedirs(os.path.join(path, dir_name))
    else:
        print("Directory {} already exists".format(dir_name))

    for file in TCI_files:
        TCI_dir = os.path.join(path, dir_name)
        try:
            shutil.move(file, TCI_dir)
        except OSError as e:
            print(f"Error: {e.strerror}")


if __name__ == '__main__':
    path = input("Enter the path where to look for TCIs to move: ")

    TCI_files = register_TCI(path)

    TCI_path = input(
        "Enter the path where to create the folder that will contain the TCIs: ")

    move_TCI(TCI_files, TCI_path)
