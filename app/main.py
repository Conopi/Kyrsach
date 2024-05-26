from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .database import engine
from . import models
from .endpoints import ensemble, music, musician, cd, performance
import logging
import time

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn.error")

app = FastAPI()



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

app.include_router(cd.router, prefix="/api/v1", tags=["cds"])
app.include_router(ensemble.router, prefix="/api/v1", tags=["ensembles"])
app.include_router(music.router, prefix="/api/v1", tags=["musics"])
app.include_router(musician.router, prefix="/api/v1", tags=["musicians"])
app.include_router(performance.router, prefix="/api/v1", tags=["performances"])

