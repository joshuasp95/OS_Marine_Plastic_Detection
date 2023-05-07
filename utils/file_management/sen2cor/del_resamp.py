# Script that will manage all preprocessed Sen2Cor files
# by deleting unnecessary ones

# Sen2Cor results return bands in different lower or higher resolutions
import os


def delete_file(file_path):
    if os.path.exists(file_path):
        print(f"File with path {file_path} exists")
        if os.path.isdir(file_path):
            print(
                f"File is a directory and cannot be deleted!")
        elif os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"File deleted {file_path}")
            except OSError as e:
                print("Error removing: %s - %s" % (e.filename, e.strerror))
    else:
        print(f"File with path {file_path} does not exist")


def run(path):

    resol_10 = ('B02', 'B03', 'B04', 'B08')
    resol_20 = ('B05', 'B06', 'B07', 'B8A', 'B11', 'B12')
    resol_60 = ('B01', 'B09', 'B10')

    source_dir = path

    print(
        f"Resampled files will be deleted from the following path {source_dir}")

    for file in os.listdir(source_dir):
        # First, delete all files of 10 m resolution bands
        # with other endings
        file_path = os.path.join(source_dir, file)

        if not os.path.isdir(file_path):
            if file.split('_')[3] == resol_20[3] and not file.split('_')[4] == '20m.tif':
                print(file)
            if file.split('_')[3] == resol_10[0] and not file.split('_')[4] == '10m.tif':
                delete_file(file_path)
            elif file.split('_')[3] == resol_10[1] and not file.split('_')[4] == '10m.tif':
                delete_file(file_path)
            elif file.split('_')[3] == resol_10[2] and not file.split('_')[4] == '10m.tif':
                delete_file(file_path)
            elif file.split('_')[3] == resol_10[3] and not file.split('_')[4] == '10m.tif':
                delete_file(file_path)
            # Do the same for 20 m resolution bands
            elif file.split('_')[3] == resol_20[0] and not file.split('_')[4] == '20m.tif':
                delete_file(file_path)
            elif file.split('_')[3] == resol_20[1] and not file.split('_')[4] == '20m.tif':
                delete_file(file_path)
            elif file.split('_')[3] == resol_20[2] and not file.split('_')[4] == '20m.tif':
                delete_file(file_path)
            elif file.split('_')[3] == resol_20[3] and not file.split('_')[4] == '20m.tif':
                delete_file(file_path)
            elif file.split('_')[3] == resol_20[4] and not file.split('_')[4] == '20m.tif':
                delete_file(file_path)
            elif file.split('_')[3] == resol_20[5] and not file.split('_')[4] == '20m.tif':
                delete_file(file_path)
            # And finally for the 60 m resolution bands
            elif file.split('_')[3] == resol_60[0] and not file.split('_')[4] == '60m.tif':
                delete_file(file_path)
            elif file.split('_')[3] == resol_60[1] and not file.split('_')[4] == '60m.tif':
                delete_file(file_path)
            elif file.split('_')[3] == resol_60[2] and not file.split('_')[4] == '60m.tif':
                delete_file(file_path)


if __name__ == "__main__":
    # Path to search for unnecessary resampled files
    path = input(
        'Enter the path where the Sen2Cor resampled files to be deleted will be searched: ')
    run(path)
