from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Reserva(Base):
    __tablename__ = 'reserva'

    id = Column(Integer, primary_key=True)
    espaco = Column(String(4000))
    data_reserva = Column(DateTime, nullable=True)

    # Definição do relacionamento entre a reserva e um morador.
    # Aqui está sendo definido a coluna 'morador' que vai guardar
    # a referencia ao morador, a chave estrangeira que relaciona
    # um morador à reserva.
    morador = Column("apartamento", String(140), ForeignKey("morador.apartamento", ondelete="CASCADE"), nullable=False)

    def __init__(self, morador:str, espaco:str, data_reserva:Union[DateTime, None] = None):
        """
        Cria uma Reserva

        Arguments:
            espaco: o espaco da reserva.
            data_insercao: data de quando a reserva foi feita ou inserida
                           à base
        """
        self.morador = morador
        self.espaco = espaco
        self.data_reserva = data_reserva
