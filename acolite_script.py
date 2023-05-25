# This script process Sentinel-2 satellite images using the Acolite tool,
# which performs atmospheric correction
# and derives water quality parameters. The script imports the Acolite library, processes the images,
# and exports the processed images as
# GeoTIFF files. Additionally, you can use the function which
# deletes the "rhot" files generated by Acolite if they are not necessary.

import re
import os
import sys


# Add Acolite clone to Python path and import Acolite from your default user home directory
# e.g C:\Users\Username\Git\Acolite

# To avoid running the code in the same folder as .SAFE files and not having to compress
# the executable together with the original Acolite, it is necessary to import the folder of
# Acolite into the sys path
user_home = os.path.expanduser("~")
sys.path.append(
    user_home+r'\Git\acolite')

# Be careful and do not move or format this section (autopep8 will put
# the imports to the top and the acolite import will not work!)
import acolite as ac

def run_acolite(bundle_path, ac_out_dir):
    print("Running Acolite...")
    print("Bundle path: {}".format(bundle_path))
    print("Output directory: {}".format(ac_out_dir))

    bundle = bundle_path

    # Output directory
    odir = ac_out_dir

    # Optional 4 element limit list [S, W, N, E]
    limit = None

    # Optional file with processing settings
    # If set to None, defaults will be used
    settings_file = None

    # Run through bundles
    print("Running bundle: {}".format(bundle))

    # Import settings
    settings = ac.acolite.settings.parse(settings_file)

    # Set settings provided above
    settings['limit'] = limit
    settings['inputfile'] = bundle
    settings['output'] = odir

    # Other settings can also be provided here, e.g.
    # settings['s2_target_res'] = 60
    # settings['dsf_aot_estimate'] = 'fixed'
    # settings['l2w_parameters'] = ['t_nechad', 't_dogliotti']
    settings['l1r_export_geotiff'] = True
    settings['l2r_export_geotiff'] = True
    settings['l2t_export_geotiff'] = True
    settings['l2w_export_geotiff'] = True
    settings['l1r_delete_netcdf'] = True
    settings['l2r_delete_netcdf'] = True

    # Process the current bundle
    ac.acolite.acolite_run(settings=settings)


def delete_rhot(ac_out_dir):
    # Compile a regex pattern to match files with "rhot" in their name
    pattern = re.compile('.*rhot.*')

    # Iterate through the files in the output directory
    for file in os.listdir(ac_out_dir):
        # If the file matches the pattern, delete it
        if pattern.match(file):
            file_path = os.path.join(ac_out_dir, file)
            os.remove(file_path)
            print('Deleted file: {}'.format(file))


if __name__ == '__main__':
    path = input("Enter the path where .SAFE files will be searched for: ")
    out_path = input(
        "Enter the path where the processed files will be created: ")
    run_acolite(path, out_path)
