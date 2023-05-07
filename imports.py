# This script imports various utilities and indices required for processing
# Sentinel-2 satellite images and detecting plastic using the Sen2Cor and Acolite tools.

# FILE MANAGEMENT

# Acolite UTILS
from utils.file_management.acolite import del_vars as acol_del_vars
from utils.file_management.acolite import logs as acol_logs
from utils.file_management.acolite import settings as acol_settings
from utils.file_management.acolite import mk_dirs as acol_mk_dirs
from utils.file_management.acolite import mv_tifs as acol_mv_tifs

# Sen2Cor UTILS
from utils.file_management.sen2cor import del_resamp as sen2_del_resamp
from utils.file_management.sen2cor import del_vars as sen2_del_vars
from utils.file_management.sen2cor import mk_dirs as sen2_mk_dirs
from utils.file_management.sen2cor import mv_tifs as sen2_mv_tifs
from utils.file_management.sen2cor import mv_TCI as sen2_mv_TCI
from utils.file_management.sen2cor import del_safe as sen2_del_safe

# INDEX IMPORTS
# ACOLITE
import utils.indices.acolite.FDI.FDI as acol_fdi
import utils.indices.acolite.FDI.FDI_Filter as acol_fdi_filter
import utils.indices.acolite.NDMI.NDMI as acol_ndmi
import utils.indices.acolite.NDMI.NDMI_Filter as acol_ndmi_filter
import utils.indices.acolite.NDVI.NDVI as acol_ndvi
import utils.indices.acolite.NDVI.NDVI_Filter as acol_ndvi_filter
import utils.indices.acolite.NDWI.NDWI as acol_ndwi
import utils.indices.acolite.NDWI.NDWI_Filter as acol_ndwi_filter
import utils.indices.acolite.PI.PI as acol_pi
import utils.indices.acolite.PI.PI_Filter as acol_pi_filter
import utils.indices.acolite.kNDVI.kNDVI as acol_kndvi
import utils.indices.acolite.kNDVI.kNDVI_Filter as acol_kndvi_filter
import utils.indices.acolite.FAI.FAI as acol_fai
import utils.indices.acolite.FAI.FAI_filter as acol_fai_filter
import utils.indices.acolite.EVI.EVI as acol_evi
import utils.indices.acolite.EVI.EVI_filter as acol_evi_filter

# SEN2COR
import utils.indices.sen2cor.FDI.FDI as sen2cor_fdi
import utils.indices.sen2cor.FDI.FDI_Filter as sen2cor_fdi_filter
import utils.indices.sen2cor.NDMI.NDMI as sen2cor_ndmi
import utils.indices.sen2cor.NDMI.NDMI_Filter as sen2cor_ndmi_filter
import utils.indices.sen2cor.NDVI.NDVI as sen2cor_ndvi
import utils.indices.sen2cor.NDVI.NDVI_Filter as sen2cor_ndvi_filter
import utils.indices.sen2cor.NDWI.NDWI as sen2cor_ndwi
import utils.indices.sen2cor.NDWI.NDWI_Filter as sen2cor_ndwi_filter
import utils.indices.sen2cor.PI.PI as sen2cor_pi
import utils.indices.sen2cor.PI.PI_Filter as sen2cor_pi_filter
import utils.indices.sen2cor.kNDVI.kNDVI_Filter as sen2cor_kndvi_filter
