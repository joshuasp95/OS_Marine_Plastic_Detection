# The code searches for files within a specific directory that meet a certain pattern
# and then processes them using Sen2Cor,
# generating the output in another directory specified by the user.

# Library for handling directories
import os
# Library for regex
import re
# Library for executing subprocesses
import subprocess

# Function that executes processing of .SAFE files using Sen2Cor


def run_sen2cor(source_dir, sen2_out_dir):
    print('Running Sen2Cor...')
    # Get the default directory for Windows download files
    user_folder = os.path.expanduser("~")
    download_folder = os.path.join(user_folder, "Downloads")

    # Path to Sen2Cor executable, static
    sen2cor = rf'{download_folder}\Sen2Cor-02.11.00-win64\L2A_Process.bat'

    # Mark the pattern that will search for files (in this case, *SAFE* directories)
    pattern = re.compile('.*SAFE*.')

    # Print the directory path to check if it is correct
    # print(os.path.abspath(source_dir))

    # Traverse the files inside the source_dir directory
    for file in os.listdir(source_dir):
        # Check if the file meets the specified pattern
        if pattern.match(file):
            # Print the name of the file to be processed
            print(file)
            # Execute the Sen2Cor command using the file as input and sen2_out_dir as output
            # you will get the results as tiff instead of .jp2 files
            subprocess.run(
                [sen2cor, '--tif', '--output_dir', sen2_out_dir, os.path.join(source_dir, file)])


# If the script is executed directly, ask the user for the directory path and output directory
if __name__ == '__main__':

    path = input("Enter the directory containing the .SAFE files: ")

    out_dir = input("Enter the output directory: ")

    # Call the run_sen2cor function with the parameters specified by the user
    run_sen2cor(path, out_dir)
