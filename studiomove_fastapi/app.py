from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from studiomove_fastapi.schemas import PatientSchema

app = FastAPI()

# Permitir chamadas do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina o domínio exato
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {'message': 'hello world'}


@app.post(
    '/pacientes/', status_code=HTTPStatus.CREATED, response_model=PatientSchema
)
def register_patient(patient: PatientSchema):
    return patient
