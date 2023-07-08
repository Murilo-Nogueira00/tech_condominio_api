from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Ocorrencia(Base):

    advertencias = 0

    __tablename__ = 'ocorrencia'

    id = Column(Integer, primary_key=True)
    # Definição do relacionamento entre a ocorrência e um morador.
    # Aqui está sendo definido a coluna 'morador' que vai guardar
    # a referencia ao morador, a chave estrangeira que relaciona
    # um morador à ocorrência.
    morador = Column("apartamento", String(140), ForeignKey("morador.apartamento"), nullable=False)

    tipo = Column(String(400))
    motivo = Column(String(4000))
    data_ocorrencia = Column(DateTime, nullable=True)

    def __init__(self, morador:str, tipo:str, motivo:str, data_ocorrencia:Union[DateTime, None] = None):
        """
        Cria uma Ocorrência

        Arguments:
            motivo: o motivo da ocorrência.
            data_ocorrência: data de quando a causa da ocorrência ocorreu
        """
        self.morador = morador
        self.tipo = tipo
        self.motivo = motivo
        self.data_ocorrencia = data_ocorrencia
