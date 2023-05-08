import index_imps as i
import glob
import os


def run(sen2_orig="", acol_dir="", sen2_dir=""):

    if not sen2_orig == "":
        # Calculate Sen2Cor indices without correction

        # Get a list with all .SAFE within the source directory
        safe_dirs = glob.glob(os.path.join(sen2_orig, '**'), recursive=True)
        safe_dirs = [safe_dir for safe_dir in safe_dirs if safe_dir.endswith(
            '.SAFE') and '999' not in safe_dir]
        print('SAFE DIRS:', safe_dirs)

        for dir in safe_dirs:

            # PI
            i.sen2cor_pi.calculate_PI(dir)
            i.sen2cor_pi_filter.filter_pi_values(dir)

            # kNDVI
            i.sen2cor_kndvi.calculate_kNDVI(dir)
            i.sen2cor_kndvi_filter.filter_kndvi_values(dir)

            # NDVI
            i.sen2cor_ndvi.calculate_NDVI(dir)
            i.sen2cor_ndvi_filter.filter_ndvi_values(dir)

            # NDWI
            i.sen2cor_ndwi.calculate_NDWI(dir)
            i.sen2cor_ndwi_filter.filter_ndwi_values(dir)

            # NDMI
            i.sen2cor_ndmi.calculate_NDMI(dir)
            i.sen2cor_ndmi_filter.filter_ndmi_values(dir)

    if not acol_dir == "":
        # Calculate Acolite indices

        # FAI
        i.acol_fai.calculate_fai(acol_dir)
        i.acol_fai_filter.filter_fai_values(acol_dir)

        # EVI
        i.acol_evi.calculate_evi(acol_dir)
        i.acol_evi_filter.filter_evi_values(acol_dir)

        # FDI
        i.acol_fdi.calculate_fdi(acol_dir)
        i.acol_fdi_filter.filter_fdi_values(acol_dir)

        # PI
        i.acol_pi.calculate_PI(acol_dir)
        # i.acol_pi_filter.filter_pi_values(acol_dir)

        # kNDVI
        i.acol_kndvi.calculate_kNDVI(acol_dir)
        # i.acol_kndvi_filter.filter_kndvi_values(acol_dir)

        # NDVI
        i.acol_ndvi.calculate_NDVI(acol_dir)
        # i.acol_ndvi_filter.filter_ndvi_values(acol_dir)

        # NDWI
        i.acol_ndwi.calculate_NDWI(acol_dir)
        # i.acol_ndwi_filter.filter_ndwi_values(acol_dir)

        # NDMI
        i.acol_ndmi.calculate_NDMI(acol_dir)
        # i.acol_ndmi_filter.filter_ndmi_values(acol_dir)

    if not sen2_dir == "":

        # PI
        i.sen2cor_pi.calculate_PI(sen2_dir)
        # i.sen2cor_pi_filter.filter_pi_values(sen2_dir)

        # kNDVI
        i.sen2cor_kndvi.calculate_kNDVI(sen2_dir)
        # i.sen2cor_kndvi_filter.filter_kndvi_values(sen2_dir)

        # NDVI
        i.sen2cor_ndvi.calculate_NDVI(sen2_dir)
        # i.sen2cor_ndvi_filter.filter_ndvi_values(sen2_dir)

        # NDWI
        i.sen2cor_ndwi.calculate_NDWI(sen2_dir)
        # i.sen2cor_ndwi_filter.filter_ndwi_values(sen2_dir)

        # NDMI
        i.sen2cor_ndmi.calculate_NDMI(sen2_dir)
        # i.sen2cor_ndmi_filter.filter_ndmi_values(sen2_dir)


if __name__ == "__main__":
    sen2_orig = input(
        "Enter the path to calculate indices from the original .SAFE files: ")
    acol_dir = input(
        "Enter the path to calculate indices from the Acolite preprocessed files: ")
    sen2_dir = input(
        "Enter the path to calculate indices from the Sen2Cor preprocessed files: ")

    run(sen2_orig, acol_dir, sen2_dir)
