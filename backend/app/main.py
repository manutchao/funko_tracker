from fastapi import FastAPI
from app.routes.funkos import router as funkos_router

app = FastAPI(title="Funko Tracker API")

app.include_router(funkos_router, prefix="/funkos")
