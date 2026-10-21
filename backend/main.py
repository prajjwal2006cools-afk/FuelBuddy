
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, vehicles, fuel, stations, ev, trip
from .models.db import init_db
import os

app = FastAPI(title="FUEL BUDDY API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register existing API routers — no LLM/AI router
app.include_router(auth.router)
app.include_router(vehicles.router)
app.include_router(fuel.router)
app.include_router(stations.router)
app.include_router(ev.router)
app.include_router(trip.router)


@app.on_event("startup")
def on_startup():
    init_db()


# Serve the frontend
frontend_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "frontend"
)

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
