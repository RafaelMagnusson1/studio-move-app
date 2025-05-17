from pydantic import BaseModel


class PatientSchema(BaseModel):
    nome: str
    data_nascimento: str
    celular: str
    endereco: str
    mensalidade: float
    aulas_por_semana: int


class PatientSchemalist(BaseModel):
    patient: list[PatientSchema]
