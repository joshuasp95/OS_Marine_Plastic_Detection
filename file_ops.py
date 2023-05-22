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
