from pydantic import BaseModel


class PatientSchema(BaseModel):
    nome: str
    data_nascimento: str
    celular: str
    endereco: str
    mensalidade: float
    aulas_por_semana: int


class PatientSchemalist(BaseModel):
    patients: list[PatientSchema]


class SessionReportSchema(BaseModel):
    paciente_id: int
    data_atendimento: str
    professor: str
    relatorio: str


class SessionReportSchemaList(BaseModel):
    reports: list[SessionReportSchema]
