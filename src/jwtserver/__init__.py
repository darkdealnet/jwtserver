"""JWTServer is a lightweight and fast JWT microservice."""
__version__ = '0.0.15'

from .app import app as app
from .server import dev as dev
import jwtserver.api.v1.views as api_v1
