from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


engine = create_engine ('sqlite:///biblioteca.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
class Astronauta (Base):
    __tablename__ = 'astronautas'
    id = Column (Integer, primary_key= True)
    nome = Column (String)
    especialidades = Column (String)
    missao_participadas = Column (String)
    def __repr__(self):
        return f'<Astronauta(nome={self.nome}, esquipes={self.equipes})>'


class Equipe (Base):
    __tablename__ = 'equipes'
    id = Column (Integer, primary_key = True)
    astronauta_id = Column (Integer, ForeignKey('astronautas.id'))
    membroEquipe= relationship ('Astronauta', backref= 'equipes')
    nomeEquipe = Column (String)
    def __repr__(self):
        return f'<Equipe(membroEquipe={self.membroEquipe}, esquipes={self.astronautas.nome})>'

class Missao (Base):
    __tablename__ = 'missoes'
    id = Column (Integer, primary_key = True)
    dataInicio = Column (Date)
    dataFim = Column (Date)
    equipe_id = Column (Integer, ForeignKey('equipes.id'))
    equipesParticipantes = relationship ('Equipe', backref='missao')
    espaconave_id = Column (Integer, ForeignKey('espaconaves.id'))
    espaconavesEmabarcadas = relationship ('Espaconave', backref='missao')

class Espaconave (Base):
     __tablename__ = 'espaconaves'
     id = Column (Integer, primary_key= True)
     capacidadeCarga = Column(Integer)
     modelo = Column (String)


class CentroDeControle (Base):
    __tablename__ = "centrocontrole"
    id = Column (Integer, primary_key = True)
    nome = Column(String)
    localizacao = Column (String)
    missaoAtiva_id = Column (Integer, ForeignKey('missoes.id'))
    missaoAtiva = relationship ('missao', backref= 'centroDeControle')

try:
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")
except Exception as e:
    print(f"Erro ao criar tabelas: {e}")
