from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

__all__ = ['app']

from jwtserver import __version__

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:5000",
    "http://localhost:3000",
]
description = """[Full JWT Server docs](https://jwtserver.darkdeal.net)"""

tags_metadata = [
    {
        "name": "Authorization",
        "description": "authorization",
    },
    {
        "name": "Registration",
        "description": "registration",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://jwtserver.darkdeal.net/en/api_v1/",
        },
    },
]

app = FastAPI(
    title="JWT server",
    description=description,
    version=__version__,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.debug = True
