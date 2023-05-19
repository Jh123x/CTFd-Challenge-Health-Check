from .http_handler import check_http
from .nc_handler import check_nc

SERVICE_DICT = {
    'http': check_http,
    'nc': check_nc,
}