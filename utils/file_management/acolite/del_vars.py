# OPTIONAL script to remove unnecessary files from Acolite preprocessing
import os


def delete_file(file_path):
    if os.path.exists(file_path):
        print(f"File with path {file_path} exists")
        if os.path.isdir(file_path):
            print(f"File is a directory and cannot be deleted!")
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

    print(f"Deleting raa, sza, and vza files in path {source_dir}")

    patterns_to_remove = ['raa', 'sza', 'vza']

    for file in os.listdir(source_dir):
        for pattern in patterns_to_remove:
            # !! Unique Acolite regex format
            if file.split('.')[0].endswith(pattern):
                file_path = os.path.join(source_dir, file)
                delete_file(file_path)


if __name__ == '__main__':
    # Path where Acolite files to be deleted will be searched
    path = input(
        'Enter the source path where the Acolite files to be deleted are located: ')
    run(path)
