"""JWTServer is a lightweight and fast JWT microservice."""

from .app import app as app
from .server import dev as dev
import jwtserver.api.v1.views as api_v1

__version__ = '0.0.8'

