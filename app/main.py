from fastapi import FastAPI
from app.controllers import patient_controller, psychologist_controller, discussion_message_controller, consultation_controller, invoice_controller

app = FastAPI()

app.include_router(patient_controller.router)
app.include_router(psychologist_controller.router)
app.include_router(discussion_message_controller.router)
app.include_router(consultation_controller.router)
app.include_router(invoice_controller.router)
