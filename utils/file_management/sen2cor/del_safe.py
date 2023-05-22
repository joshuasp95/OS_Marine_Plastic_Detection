import os
import glob
import shutil


def delete_sen2_safe(path):
    files = glob.glob(os.path.join(path, '**'), recursive=True)

    files = [res for res in files if '999' in res and res.endswith('.SAFE')]

    i = 0

    for file in files:
        i += 1
        print(file)
        try:
            shutil.rmtree(file)
        except OSError as e:
            print(f'Error: {e.strerror}')

    print('Total:', i)


if __name__ == '__main__':
    path = input("Enter the path with files to delete: ")
    delete_sen2_safe(path)
