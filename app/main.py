import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import (
    patient_controller, psychologist_controller, discussion_message_controller,
    consultation_controller, invoice_controller
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patient_controller.router)
app.include_router(psychologist_controller.router)
app.include_router(discussion_message_controller.router)
app.include_router(consultation_controller.router)
app.include_router(invoice_controller.router)
