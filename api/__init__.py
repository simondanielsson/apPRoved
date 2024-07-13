"""API init file.

Logging is configured here to ensure global scope.
"""

import api.common.orm
from api.utils.log import configure_logging

configure_logging()
