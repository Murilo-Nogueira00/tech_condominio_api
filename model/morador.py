from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base
from model.reserva import Reserva
from model.ocorrencia import Ocorrencia


class Morador(Base):
    __tablename__ = 'morador'

    id = Column("pk_apartamento", Integer, primary_key=True)
    apartamento = Column(String(140), unique=True)
    nome = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o morador e a reserva.
    # Essa relação é implicita, não está salva na tabela 'morador',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    reservas = relationship("Reserva")

    def __init__(self, apartamento:str, nome:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Morador

        Arguments:
            apartamento: apartamento do morador.
            nome: nome do morador
            data_insercao: data de quando o morador
        """
        self.apartamento = apartamento
        self.nome = nome


        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def get_nome(self):
        return self.nome

    def adiciona_reserva(self, reserva:Reserva):
        """ Adiciona uma nova reserva ao Morador
        """
        self.reservas.append(reserva)

