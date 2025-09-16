from sqlalchemy import create_engine, Column, String, Integer, Enum, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ----------------------- TABELAS -----------------------
class Ativo(Base):
    __tablename__ = 'ativos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipoEquip = Column(
        Enum('Notebook', 'Desktop', 'Telefonia', 'Estoque', name='tipoEquip_enum'),
        nullable=False, default='Notebook'
    )
    patrimonio = Column(String, nullable=False)
    marca = Column(String, nullable=True)
    serial = Column(String, nullable=False)
    disco = Column(String, nullable=True)
    hostname = Column(String, nullable=False)
    nome = Column(String, nullable=True)
    login = Column(String, nullable=True)
    setor = Column(String, nullable=False)
    local = Column(String, nullable=False)
    sistemaOperacional = Column(String, nullable=True)
    status = Column(
        Enum('Em uso', 'Estoque', 'Manutenção', name='status_enum'),
        nullable=False, default='Em uso'
    )


class Peca(Base):
    __tablename__ = 'pecas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    observacao = Column(String, nullable=False)


class Chamado(Base):
    __tablename__ = 'chamados'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)
    assunto = Column(String, nullable=False)
    tipoChamado = Column(
        Enum('Remoto', 'Presencial', 'Blip', name='tipoChamado_enum'),
        nullable=False, default='Remoto'
    )
    tecnico = Column(String, nullable=False)
    grupo = Column(String, nullable=False)
    data = Column(Date, nullable=False)
