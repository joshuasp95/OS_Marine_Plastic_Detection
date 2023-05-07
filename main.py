# General imports
import re
import os
import glob

# Raster ops
import resampler as resamp

# Executables
import acolite_script as acol
import sen2cor_script as sen2

# UTILS
import file_ops as fop

# INDICES
import index_imps as i


def generate_output_dirs(path):

    # Absolute path of output directory
    out_dir = os.path.join(path, "Results")

    # Names of output directories
    acol_name = 'Results_Acolite'
    sen2_name = 'Results_Sen2Cor'

    # Check if output directories exist, if not, create them
    if not os.path.exists(os.path.join(out_dir, acol_name)):
        os.makedirs(os.path.join(out_dir, acol_name))
    else:
        print('Output directory {} already exists'.format(acol_name))

    if not os.path.exists(os.path.join(out_dir, sen2_name)):
        os.makedirs(os.path.join(out_dir, sen2_name))
    else:
        print('Output directory {} already exists'.format(sen2_name))

    # Absolute path to output directory for acolite
    acol_out_dir = os.path.join(out_dir, acol_name)

    # Absolute path to output directory for sen2cor
    sen2_out_dir = os.path.join(out_dir, sen2_name)

    # Check if directories have been created correctly
    print('acol_out_dir: {}'.format(acol_out_dir))
    print('sen2_out_dir: {}'.format(sen2_out_dir))

    return acol_out_dir, sen2_out_dir


def run(path, out_path):
    # Get the absolute path of the directory where sentinel2 .SAFE files are located
    source_dir = path

    # Get the output directory paths
    acol_out_dir, sen2_out_dir = generate_output_dirs(out_path)

    # ACOLITE
    # First run acolite since it does not alter the original .SAFE
    for file in os.listdir(source_dir):
        print('file: ', file)
        # Filter for directories ending in .SAFE
        if file.endswith('.SAFE'):
            print(os.path.join(source_dir, file))
            # Run acolite passing as parameters each .SAFE file with its absolute path
            # and the output directory
            acol.run_acolite(os.path.join(source_dir, file), acol_out_dir)

    # Acolite structuring --> First delete unnecessary files and then organize in folders

    # Delete unnecessary rhot files
    acol.delete_rhot(acol_out_dir)

    # Function that deletes raa, sza and vza files from acolite
    fop.acol_del_vars.run(acol_out_dir)

    # Function to store logs in a new folder
    fop.acol_logs.run(acol_out_dir)

    # Function to store settings in a new folder
    fop.acol_settings.run(acol_out_dir)

    # Function to create directories based on acolite dates, if there are 2 cells
    # of the same date, they will be placed in the same directory
    fop.acol_mk_dirs.run(acol_out_dir)

    # Function to move tifs to the previously created folders
    fop.acol_mv_tifs.run(acol_out_dir)

    # SEN2COR

    # Once we finish acolite, we run sen2cor
    sen2.run_sen2cor(source_dir, sen2_out_dir)

    # Resample the sen2cor tif files since it does not do it automatically like acolite
    # It also returns the resampled storage path so that the resulting files can be organized later
    sen2_res_out_dir = resamp.resample_to_10m(sen2_out_dir)

    # Structuring sen2cor --> First delete unnecessary files and then organize into folders

    # Functions that delete unnecessary files from sen2cor resampling
    fop.sen2_del_resamp.run(sen2_res_out_dir)
    fop.sen2_del_vars.run(sen2_res_out_dir)

    # Function to create directories based on acolite dates, if there are 2 cells
    # from the same date, they will be placed in the same directory
    fop.sen2_mk_dirs.run(sen2_res_out_dir)

    # Function to move tifs to previously created folders
    fop.sen2_mv_tifs.run(sen2_res_out_dir)

    # Move Sen2Cor True Color Images (TCI) since the bands are resampled
    sen2_TCIs = fop.sen2_mv_TCI.register_TCI(sen2_out_dir)
    fop.sen2_mv_TCI.move_TCI(sen2_TCIs, sen2_out_dir)


# Calculate Sen2Cor indices without correction

    # Get a list with all the .SAFE inside the source directory
    safe_dirs = glob.glob(os.path.join(source_dir, '**'), recursive=True)
    safe_dirs = [safe_dir for safe_dir in safe_dirs if safe_dir.endswith(
        '.SAFE') and '999' not in safe_dir]

    print('SAFE DIRS:', safe_dirs)

    for safe_dir in safe_dirs:

        # PI
        i.sen2cor_pi.calculate_PI(safe_dir)
        i.sen2cor_pi_filter.filter_pi_values(source_dir)

        # kNDVI
        i.sen2cor_kndvi.calculate_kNDVI(safe_dir)
        i.sen2cor_kndvi_filter.filter_kndvi_values(source_dir)

        # NDVI
        i.sen2cor_ndvi.calculate_NDVI(safe_dir)
        i.sen2cor_ndvi_filter.filter_ndvi_values(source_dir)

        # NDWI
        i.sen2cor_ndwi.calculate_NDWI(safe_dir)
        # i.sen2cor_ndwi_filter.filter_ndwi_values(source_dir)

        # NDMI
        i.sen2cor_ndmi.calculate_NDMI(safe_dir)
        i.sen2cor_ndmi_filter.filter_ndmi_values(source_dir)

# Calculate Acolite indices

    # FAI
    i.acol_fai.calculate_fai(acol_out_dir)
    i.acol_fai_filter.filter_fai_values(acol_out_dir)

    # EVI
    i.acol_evi.calculate_evi(acol_out_dir)
    i.acol_evi_filter.filter_evi_values(acol_out_dir)

    # FDI
    i.acol_fdi.calculate_fdi(acol_out_dir)
    i.acol_fdi_filter.filter_fdi_values(acol_out_dir)

    # PI
    i.acol_pi.calculate_PI(acol_out_dir)
    # i.acol_pi_filter.filter_pi_values(acol_out_dir)

    # kNDVI
    i.acol_kndvi.calculate_kNDVI(acol_out_dir)
    # i.acol_kndvi_filter.filter_kndvi_values(acol_out_dir)

    # NDVI
    i.acol_ndvi.calculate_NDVI(acol_out_dir)
    # i.acol_ndvi_filter.filter_ndvi_values(acol_out_dir)

    # NDWI
    i.acol_ndwi.calculate_NDWI(acol_out_dir)
    # i.acol_ndwi_filter

# Calcular indices Sen2Cor with atmospheric correction

    # PI
    i.sen2cor_pi.calculate_PI(sen2_res_out_dir)
    # i.sen2cor_fdi_filter.filter_pi_values(sen2_res_out_dir)

    # kNDVI
    i.sen2cor_kndvi.calculate_kNDVI(sen2_res_out_dir)
    # i.sen2cor_kndvi_filter.filter_kndvi_values(sen2_res_out_dir)

    # NDVI
    i.sen2cor_ndvi.calculate_NDVI(sen2_res_out_dir)
    # i.sen2cor_ndvi_filter.filter_ndvi_values(sen2_res_out_dir)

    # NDWI
    i.sen2cor_ndwi.calculate_NDWI(sen2_res_out_dir)
    # i.sen2cor_ndwi_filter.filter_ndwi_values(sen2_res_out_dir)

    # NDMI
    i.sen2cor_ndmi.calculate_NDMI(sen2_res_out_dir)
    # i.sen2cor_ndmi_filter.filter_ndmi_values(sen2_res_out_dir)


if __name__ == "__main__":
    path = input(
        "Enter the absolute path of the directory where the Sentinel-2 .SAFE files are located: ")

    out_path = input(
        "Enter the absolute path of the output directory for the results: ")

    run(path, out_path)