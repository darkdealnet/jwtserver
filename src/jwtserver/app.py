from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

__all__ = ['app']

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:5000",
    "http://localhost:3000",
]

app = FastAPI(
    title="JWT server"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.debug = True
