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
    status = relationship ('Equipe', backref = 'astronautas')
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


#METODOS

def adicionar_astronauta (nome,membroEquipe):
    astronauta = session.query (Astronauta).filter_by (nome=nome).first()
    if not astronauta:
        astronauta = Astronauta (nome = nome)
    if membroEquipe:
        membroEquipe.astronautas.append(astronauta)
        session.add
        session.commit()


def remover_astronauta (nome,membroEquipe):
    astronauta = session.query (Astronauta).filter_by (nome=nome).first()
    if not astronauta:
        astronauta = Astronauta (nome = nome)
    if membroEquipe:
        membroEquipe.astronautas.remove(astronauta)
        session.remove 
        session.commit()

def consultar_participacao_missao(astronauta,missao):
    astronauta = session.query (Astronauta).filter_by(missao=missao).first()
    for astronauta in missao:
        print (astronauta.nome)

def relatar_status(astronauta_nome,equipe): #O astronauta relata o status para equipe, e adiciona o status no banco equipe.
    status = session.query(equipe).filter_by (nome= astronauta_nome).first()
    if not status:
        status = equipe (nome = astronauta_nome)
    if status:
        status.equipe.append(equipe)
        session.add (status)
        session.commit()

def iniciar_missao (nomeEquipe,missao): # se a equipe apertar X, inicia a missao. (Precisa deixar o Centro de Controle no parametro?)
    iniciar = session.query(missao).filter_by (equipe = nomeEquipe).first()
    iniciar = input("Gostaria de iniciar a missão? Pressione X")
    if iniciar == 'X':
        iniciar = missao (Equipe=nomeEquipe)
    if iniciar:
        iniciar.CentroDeControle.append (iniciar)
        session.add(iniciar)
        session.commit()

def finalizar_missao (nomeEquipe,missao): #A mesma coisa, porém usando Y
    finalizar = session.query(missao).filter_by (equipe = nomeEquipe).first()
    finalizar = input ("Gostaria de iniciar a missão? Pressione Y")
    if finalizar == 'Y':
        finalizar = missao (Equipe=nomeEquipe)
    if finalizar:
        finalizar.CentroDeControle.append (finalizar)
        session.add(finalizar)
        session.commit()

def mostrar_status ():
    missoes = session.query(Missao).all()
    for missao in missoes :
        print (missao)

