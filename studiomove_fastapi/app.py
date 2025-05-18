from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from studiomove_fastapi.database import get_session
from studiomove_fastapi.models import Patient
from studiomove_fastapi.schemas import PatientSchema, PatientSchemalist

app = FastAPI()

# Permitir chamadas do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Em produção, defina o domínio exato
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
def read_root():
    return {'message': 'API ONLINE'}


# CADASTRO DE PACIENTES:


# CREATE
@app.post(
    '/pacientes/', status_code=HTTPStatus.CREATED, response_model=PatientSchema
)
def register_patient(patient: PatientSchema, session=Depends(get_session)):
    db_patient = session.scalar(
        select(Patient).where(Patient.nome == patient.nome)
    )

    if db_patient:
        if db_patient.nome == patient.nome:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Paciente ja existe'
            )

    db_patient = Patient(
        nome=patient.nome,
        data_nascimento=patient.data_nascimento,
        celular=patient.celular,
        endereco=patient.endereco,
        mensalidade=patient.mensalidade,
        aulas_por_semana=patient.aulas_por_semana,
    )

    # Persiste no banco
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)

    return db_patient


# READ
@app.get('/pacientes/', response_model=PatientSchemalist)
def read_pacientes(session: Session = Depends(get_session)):
    patient = session.scalars(select(Patient)).all()
    return {'patients': patient}


# UPDATE
@app.put('/pacientes/')
def update_pacientes(session: Session = Depends(get_session)): ...


# DELETE


@app.delete('/pacientes/')
def delete_pacientes(session: Session = Depends(get_session)): ...
