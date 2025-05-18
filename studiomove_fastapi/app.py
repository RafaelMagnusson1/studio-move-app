from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from studiomove_fastapi.database import get_session
from studiomove_fastapi.models import Patient, SessionReport
from studiomove_fastapi.schemas import (
    PatientSchema,
    PatientSchemalist,
    SessionReportSchema,
    SessionReportSchemaList,
)

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
@app.put('/pacientes/', status_code=HTTPStatus.OK, response_model=PatientSchema)
def update_pacientes(patient_id: int,
                      patient: PatientSchema,
                            session: Session = Depends(get_session)):
    db_patient = session.scalar(
        select(Patient).where(Patient.id == patient_id)
    )
    if not db_patient:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Paciente não encontrado")

    db_patient.nome = patient.nome
    db_patient.data_nascimento = patient.data_nascimento
    db_patient.celular = patient.celular
    db_patient.endereco = patient.endereco
    db_patient.mensalidade = patient.mensalidade
    db_patient.aulas_por_semana = patient.aulas_por_semana

    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)

    return db_patient


# DELETE


@app.delete('/pacientes/')
def delete_pacientes(session: Session = Depends(get_session)): ...

# CRIAÇÃO DE RELATÓRIOS

# CREATE
@app.post('/relatorios/', status_code=HTTPStatus.CREATED, response_model=SessionReportSchema)
def create_report(session_report: SessionReportSchema, session=Depends(get_session)):
    db_patient_report = session.scalar(
        select(Patient).where(Patient.id == session_report.paciente_id)
    )

    if not db_patient_report:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Paciente não encontrado")

    db_session_report = SessionReport(
        paciente_id=session_report.paciente_id,
        data_atendimento=session_report.data_atendimento,
        professor=session_report.professor,
        relatorio=session_report.relatorio
    )

    session.add(db_session_report)
    session.commit()
    session.refresh(db_session_report)

    return db_session_report

# READ
@app.get('/relatorios/', status_code=HTTPStatus.OK, response_model=SessionReportSchemaList)
def read_report(session: Session = Depends(get_session)):
    session_report = session.scalars(select(SessionReport)).all()

    return {'reports': session_report}

    
# UPDATE


# DELETE
