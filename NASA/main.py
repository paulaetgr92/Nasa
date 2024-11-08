from sqlalchemy import create_engine, Column, Integer,String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime
from sqlalchemy import Float 

engine = create_engine('sqlite:///Nasa.db')
Session = sessionmaker(bind=engine) 
session = Session()
Base = declarative_base()

class Astronauta(Base):
    __tablename__ = 'astronautas'
    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)
    especialidades = Column(String)
    equipes = relationship('Equipe', back_populates='membro_equipe')
    
    def __repr__(self):
        return f'<Astronauta(nome={self.nome}, especialidades={self.especialidades})>'

class Equipe(Base):
    __tablename__ = 'equipes'
    
    id = Column(Integer, primary_key=True)
    astronauta_id = Column(Integer, ForeignKey('astronautas.id'))
    membro_equipe = relationship('Astronauta', back_populates='equipes')
    nomeEquipe = Column(String)
    missao_id = Column(Integer, ForeignKey('missoes.id'))
    missao = relationship('Missao', back_populates='equipe')

    def __repr__(self):
        return f'<Equipe(nomeEquipe={self.nomeEquipe}, astronauta={self.membroEquipe.nome})>'

class Missao(Base):
    __tablename__ = 'missoes'
    id = Column(Integer, primary_key=True)
    nomeMissao = Column(String, nullable=False)
    lancamentoData = Column(Date, default=datetime.now) 
    dataInicio = Column(Date, default=datetime.now())
    dataFim = Column(Date, nullable=True)
    missaoAtiva = Column(Boolean, default=True)
    centro_controle_id = Column(Integer, ForeignKey('centrocontrole.id'), nullable=True)
    centros_de_controle = relationship('CentroDeControle', backref='missoes')
    espaconave_id = Column(Integer, ForeignKey('espaconaves.id'), nullable=True)
    espaconavesEmbarcadas = relationship('Espaconave', backref='missao_associada')
    equipe = relationship('Equipe', back_populates='missao')
    
    def __repr__(self):
        return f'<Missao(nome={self.nomeMissao})>'


class Espaconave(Base):
    __tablename__ = 'espaconaves'
    id = Column(Integer, primary_key=True)
    capacidade_carga = Column(Float, nullable=False) 
    modelo = Column(String, nullable=False)
    statusProblema = Column(String, nullable=True)  

    def __repr__(self):
        return f'<Espaconave(modelo={self.modelo}, capacidade_carga={self.capacidade_carga} kg)>'



class CentroDeControle(Base):
    __tablename__ = "centrocontrole"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    localizacao = Column(String)
    
    def __repr__(self):
        return f'<CentroDeControle(nome={self.nome}, localizacao={self.localizacao})>'

try:
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")
except Exception as e:
    print(f"Erro ao criar tabelas: {e}")

def adicionar_astronauta():
    try:
        nome = input("Digite o nome do astronauta: ")
        astronauta = session.query(Astronauta).filter_by(nome=nome).first()
        
        if not astronauta:
            especialidades = input("Digite as especialidades do astronauta: ")
            astronauta = Astronauta(nome=nome, especialidades=especialidades)
            session.add(astronauta)
            session.commit()
            print(f'Astronauta {nome} adicionado com sucesso.')
        else:
            print(f'Astronauta {nome} já existe.')

    except Exception as e:
        print(f"Houve um erro ao adicionar o astronauta: {e}")
        print("Tente novamente.")


def remover_astronauta():
    try:
        nome = input("Digite o nome do astronauta: ")
        astronauta = session.query(Astronauta).filter_by(nome=nome).first()
        
        if astronauta:
            confirmacao = input(f"Deseja remover o astronauta {nome}? (s/n): ")
            if confirmacao.lower() != 's' and confirmacao.lower() != 'sim':
                return
            session.delete(astronauta)
            session.commit()
            print(f'Astronauta {nome} removido com sucesso.')
        else:
            print(f'Astronauta {nome} não encontrado.')

    except Exception as e:
        print(f"Houve um erro ao remover o astronauta: {e}")
        print("Tente novamente.")

def atualizar_astronauta():
    try:
        nome = input("Digite o nome do astronauta: ")
        astronauta = session.query(Astronauta).filter_by(nome=nome).first()
        print(f"ID: {astronauta.id} Astronauta: {astronauta.nome} - Especialidades: {astronauta.especialidades}")
        continuar = input("Deseja atualizar esse astronauta? (s/n): ")
        
        if astronauta and continuar.lower() == 's':
            novo_nome = input("Digite o novo nome do astronauta: ")
            especialidades = input("Digite as novas especialidades do astronauta: ")
            astronauta.especialidades = especialidades
            astronauta.nome = novo_nome
            session.commit()
            print(f'Astronauta {nome} atualizado com sucesso.')
        else:
            print(f'Astronauta {nome} não encontrado.')

    except Exception as e:
        print(f"Houve um erro ao atualizar o astronauta: {e}")
        print("Tente novamente.")

def consultar_astronautas():
    astronautas = session.query(Astronauta).all()
    for astronauta in astronautas:
        print(f'ID : {astronauta.id}, Nome: {astronauta.nome}, Especialidades: {astronauta.especialidades}') 


def criar_equipe():
    nome_equipe = input("Digite o nome da equipe: ")
    astronautas_da_equipe = []
    
    while True:
        nome_astronauta = input("Digite o nome do astronauta (ou 'fim' para finalizar): ")
        
        if nome_astronauta.lower() == 'fim':
            break
        
        astronauta = session.query(Astronauta).filter_by(nome=nome_astronauta).first()

        if not astronauta:
            print(f"Astronauta {nome_astronauta} não encontrado.")
        else:
            astronautas_da_equipe.append(astronauta) 

    addMissao = input("Adicionar missão? (s/n): ")
    
    if addMissao.lower() == "s":
        missao_nome = input("Digite o nome da missão: ")
        missao = session.query(Missao).filter_by(nomeMissao=missao_nome).first()
        if not missao:
            print(f"Missão {missao_nome} não encontrada.")
            return
        missao_id = missao.id
    else:
        missao_id = None

    for astronauta in astronautas_da_equipe:
        equipe = Equipe(
            nomeEquipe=nome_equipe,
            astronauta_id=astronauta.id,
            missao_id=missao_id
        )

        session.add(equipe)
        print(f"Astronauta {astronauta.nome} adicionado à equipe {nome_equipe}.")
    
    session.commit()
    print(f"Equipe {nome_equipe} criada com sucesso com {len(astronautas_da_equipe)} astronautas!")
    session.commit()

def listar_equipes():
    equipes = session.query(Equipe).all()
    for equipe in equipes:
        print(f'ID: {equipe.id}, Nome: {equipe.nomeEquipe}, Astronauta: {equipe.membro_equipe.nome}')


def criar_missao():
    nome_missao = input("Digite o nome da missão: ")
    equipe_nome = input("Atribuir missão para qual equipe? ")

    equipe = session.query(Equipe).filter_by(nomeEquipe=equipe_nome).first()

    if not equipe:
        print(f'Equipe {equipe_nome} não encontrada. Certifique-se de que a equipe foi criada antes.')
        return

    missao = Missao(nomeMissao=nome_missao)
    missao.dataInicio = datetime.now()  

    equipe.missao = missao
    equipe.missao_id = missao.id

    session.add(missao)
    session.commit()  

    print(f'Missão "{nome_missao}" criada com sucesso e atribuída à equipe "{equipe_nome}".')



def consultar_missoes():
    missoes = session.query(Missao).all()

    if not missoes:
        print("Não há missões registradas.")
        return
    
    for missao in missoes:
        
        equipe = session.query(Equipe).filter_by(missao_id=missao.id).first()

        if equipe:
            equipe_nome = equipe.nomeEquipe
        else:
            equipe_nome = "Nenhuma equipe atribuída"
        print(f"ID: {missao.id}")
        print(f"Missão: {missao.nomeMissao}")
        print(f"Equipe responsável: {equipe_nome}")
        print(f"Data de Início: {missao.dataInicio.strftime('%d/%m/%Y') if missao.dataInicio else 'Não definida'}")
        print(f"Data de Fim: {missao.dataFim.strftime('%d/%m/%Y') if missao.dataFim else 'Em andamento'}")
        print("-" * 50)


def consultar_participacao_missao():
    nome_missao = input("Digite o nome da missão para consultar a participação: ")
    missao = session.query(Missao).filter_by(nomeMissao=nome_missao).first()

    if not missao:
        print(f"Missão {nome_missao} não encontrada.")
        return

    equipes = session.query(Equipe).filter_by(missao_id=missao.id).all()

    if not equipes:
        print(f"Não há equipes associadas à missão {nome_missao}.")
        return

    print(f"Astronautas participantes da missão '{missao.nomeMissao}':")
    for equipe in equipes:
        astronauta = equipe.membro_equipe  # Acessar o astronauta da equipe
        print(f"- {astronauta.nome} (Especialidades: {astronauta.especialidades})")

    print("-" * 50)


def iniciar_missao():
    nome_missao = input("Digite o nome da missão que deseja iniciar: ")

    missao = session.query(Missao).filter_by(nomeMissao=nome_missao).first()

    if not missao:
        print(f"Missão {nome_missao} não encontrada.")
        return
    if missao.missaoAtiva:
        print(f"A missão '{nome_missao}' já está ativa.")
        return

    missao.dataInicio = datetime.now() 
    missao.missaoAtiva = True 

    session.commit()  

    print(f"A missão '{nome_missao}' foi iniciada com sucesso!")


def finalizar_missao():
    nome_missao = input("Digite o nome da missão que deseja finalizar: ")

    missao = session.query(Missao).filter_by(nomeMissao=nome_missao).first()

    if not missao:
        print(f"Missão {nome_missao} não encontrada.")
        return

    if not missao.missaoAtiva:
        print(f"A missão '{nome_missao}' já foi finalizada ou não está ativa.")
        return

    missao.dataFim = datetime.now()  
    missao.missaoAtiva = False 

    session.commit()  

    print(f"A missão '{nome_missao}' foi finalizada com sucesso!")

def adicionar_espaconave():
    try:
        modelo = input("Digite o modelo da espaçonave: ")
        capacidade_carga = input("Digite a capacidade de carga da espaçonave (em kg): ")

        # Valida se a capacidade de carga é um número
        try:
            capacidade_carga = float(capacidade_carga)
        except ValueError:
            print("Erro: A capacidade de carga deve ser um número válido.")
            return

        # Cria a nova espaçonave com os dados informados
        nova_espaconave = Espaconave(modelo=modelo, capacidade_carga=capacidade_carga)

        # Adiciona e faz o commit para salvar no banco de dados
        session.add(nova_espaconave)
        session.commit()

        # Exibe uma mensagem de sucesso
        print(f"A espaçonave '{nova_espaconave.modelo}' foi adicionada com sucesso ao banco de dados!")
    
    except Exception as e:
        print(f"Houve um erro ao adicionar a espaçonave: {e}")
        print("Tente novamente.")

# Função para lançar a espaçonave com tratamento de exceção
def lancar_espaconave():
    try:
        nome_missao = input("Digite o nome da missão para lançar a espaçonave: ")
        missao = session.query(Missao).filter_by(nomeMissao=nome_missao).first()

        if not missao:
            print(f"Missão {nome_missao} não encontrada.")
            return

        if not missao.missaoAtiva:
            print(f"A missão '{nome_missao}' não está mais ativa.")
            return

        if missao.espaconave_id:  
            print(f"A missão '{nome_missao}' já tem uma espaçonave associada.")
            return

        nome_espaconave = input("Digite o nome ou modelo da espaçonave para lançar: ")
    
        espaconave = session.query(Espaconave).filter_by(modelo=nome_espaconave).first()

        if not espaconave:
            print(f"Espaçonave '{nome_espaconave}' não encontrada.")
            return

        missao.espaconave_id = espaconave.id
        missao.lancamentoData = datetime.now()  

        session.commit()

        print(f"A espaçonave '{espaconave.modelo}' foi lançada com sucesso na missão '{missao.nomeMissao}'!")

    except Exception as e:
        print(f"Houve um erro ao lançar a espaçonave: {e}")
        print("Tente novamente.")


def monitorar_missao():
    nome_missao = input("Digite o nome da missão que deseja monitorar: ")
    missao = session.query(Missao).filter_by(nomeMissao=nome_missao).first()

    if not missao:
        print(f"Missão '{nome_missao}' não encontrada.")
        return

    print(f"Missão: {missao.nomeMissao}")
    print(f"Data de Início: {missao.dataInicio.strftime('%d/%m/%Y %H:%M:%S') if missao.dataInicio else 'Não definida'}")
    print(f"Data de Fim: {missao.dataFim.strftime('%d/%m/%Y %H:%M:%S') if missao.dataFim else 'Em andamento'}")
    
    status_missao = "Ativa" if missao.missaoAtiva else "Finalizada"
    print(f"Status: {status_missao}")

    equipe = session.query(Equipe).filter_by(missao_id=missao.id).first()
    if equipe:
        print(f"Equipe responsável: {equipe.nomeEquipe}")
        astronautas = [e.membro_equipe.nome for e in session.query(Equipe).filter_by(missao_id=missao.id).all()]
        print(f"Astronautas: {', '.join(astronautas)}")
    else:
        print("Nenhuma equipe atribuída à missão.")


    if missao.espaconave_id:
        espaconave = session.query(Espaconave).filter_by(id=missao.espaconave_id).first()
        if espaconave:
            print(f"Espaçonave associada: {espaconave.modelo}")
            print(f"Capacidade de Carga: {espaconave.capacidade_carga} kg")
        else:
            print("Espaçonave não encontrada.")
    else:
        print("Nenhuma espaçonave associada à missão.")

    if missao.lancamentoData:
        print(f"Data de Lançamento: {missao.lancamentoData.strftime('%d/%m/%Y %H:%M:%S')}")
    else:
        print("Espaçonave não foi lançada ainda.")

def reportar_problema():
    nome_missao = input("Digite o nome da missão onde o problema ocorreu: ")
    missao = session.query(Missao).filter_by(nomeMissao=nome_missao).first()

    if not missao:
        print(f"Missão '{nome_missao}' não encontrada.")
        return
    if not missao.missaoAtiva:
        print(f"A missão '{nome_missao}' já está finalizada, não é possível reportar problemas.")
        return

    nome_espaconave = input("Digite o nome da espaçonave associada à missão: ")

    espaconave = session.query(Espaconave).filter_by(id=missao.espaconave_id).first()

    if not espaconave or espaconave.modelo != nome_espaconave:
        print(f"A espaçonave '{nome_espaconave}' não está associada à missão '{nome_missao}'.")
        return

    descricao_problema = input("Descreva o problema relacionado à capacidade de carga da espaçonave: ")

    if espaconave.capacidade_carga <= 0:
        print("A capacidade de carga da espaçonave é zero ou negativa. Verifique as configurações da espaçonave.")
        return

    problema_reportado = f"Problema reportado: {descricao_problema}. Capacidade de carga: {espaconave.capacidade_carga}kg."

    missao.statusProblema = problema_reportado  
    espaconave.statusProblema = problema_reportado 
    

    session.commit()

    print(f"Problema reportado na missão '{missao.nomeMissao}' e espaçonave '{espaconave.modelo}'. Descrição do problema: {descricao_problema}")



def main():
    while True:
        try:
            print("╔══════════════════════════════════════════════╗")
            print("\n1 - Adicionar astronauta")
            print("2 - Remover astronauta")
            print("3 - Atualizar Astronautas")
            print("4 - Consultar Astronautas Cadastrados")
            print("5 - Criar uma nova equipe")
            print("6 - Consultar Equipes")
            print("7 - Criar uma nova missão")
            print("8 - Consultar Missoes")
            print("9 - Consultar Participação em missão")
            print("10 - Iniciar missão")
            print("11 - Finalizar missão")
            print("12 - Adicionar espaçonave")
            print("13 - Lançar Espaçonave")
            print("14 - Monitorar missão")
            print("15 - Reportar problema")
            print("\n╚══════════════════════════════════════════════╝")

            escolha = input("Escolha uma opção: ")

            match escolha:
                case '1':
                    adicionar_astronauta()
                case '2':
                    remover_astronauta()                 
                case '3':
                    atualizar_astronauta()                 
                case '4':
                    consultar_astronautas()
                case '5':
                    criar_equipe()
                case '6':
                    listar_equipes()
                case '7':
                    criar_missao()
                case '8':
                    consultar_missoes()
                case '9':
                    consultar_participacao_missao()
                case '10':
                    iniciar_missao()
                case '11':
                    finalizar_missao()
                case '12':
                    adicionar_espaconave()
                case '13':
                    lancar_espaconave()
                case '14':
                    monitorar_missao()
                case '15':
                    reportar_problema()
                case _:
                    print("Opção inválida. Tente novamente.")
        
        except Exception as e:
            print(f"Houve um erro inesperado: {e}")
            print("Tente novamente.")

if __name__ == '__main__':
    main()