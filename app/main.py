from fastapi import FastAPI
from app.controllers import patient_controller

app = FastAPI()

app.include_router(patient_controller.router)
