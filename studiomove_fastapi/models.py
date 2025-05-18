from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Patient:
    __tablename__ = 'patients'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str]
    data_nascimento: Mapped[str]
    celular: Mapped[str]
    endereco: Mapped[str]
    mensalidade: Mapped[float]
    aulas_por_semana: Mapped[int]
    data_criacao: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    data_update: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class SessionReport:
    __tablename__ = 'session_reports'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    paciente_id: Mapped[int]
    data_atendimento: Mapped[str]
    professor: Mapped[str]
    relatorio: Mapped[str]
    data_criacao: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    data_update: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
