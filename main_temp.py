import os
import sys

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from api.v1.router import api_router
from log import setup_logging, logger
from pony.orm import db_session
from api.middleware import AuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware

DEBUG = os.environ.get('ENV', '') == 'dev'
logger.info(f'DEBUG: {DEBUG}')

app_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, app_path)
version = os.environ.get('VERSION', '0.0.1')
logger.info(f'version: {version}')
app = FastAPI(
    version=version
)
app.debug = DEBUG
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    AuthenticationMiddleware,
    backend=AuthenticationBackend()
)

app.include_router(api_router, prefix='/api/v1')


# get static file from directory
# but now is in s3
# upload_path = os.path.join(app_path, 'uploads')
# app.mount("/uploads", StaticFiles(directory=upload_path), name="uploads")


@app.on_event("startup")
async def startup_event():
    setup_logging()


@app.middleware("http")
async def add_pony(request: Request, call_next):
    with db_session:
        response = await call_next(request)
        return response


if __name__ == "__main__":
    if DEBUG:
        uvicorn.run('main:app', host="0.0.0.0", port=5000, log_level="info", reload=True, workers=1)