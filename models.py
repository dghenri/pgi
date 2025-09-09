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
    patrimonio = Column(String)
    marca = Column(String)
    serial = Column(String)
    disco = Column(String)
    hostname = Column(String)
    nome = Column(String)
    login = Column(String)
    setor = Column(String)
    local = Column(String)
    sistemaOperacional = Column(String)
    status = Column(
        Enum('Em uso', 'Estoque', 'Manutenção', name='status_enum'),
        nullable=False, default='Em uso'
    )


class Peca(Base):
    __tablename__ = 'pecas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    categoria = Column(String)
    quantidade = Column(Integer)
    observacao = Column(String)


class Chamado(Base):
    __tablename__ = 'chamados'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    numero = Column(Integer)
    assunto = Column(String)
    tipoChamado = Column(
        Enum('Remoto', 'Presencial', 'Blip', name='tipoChamado_enum'),
        nullable=False, default='Remoto'
    )
    tecnico = Column(String)
    grupo = Column(String)
    data = Column(Date)
