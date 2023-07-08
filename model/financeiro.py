from sqlalchemy import Column, Float, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Financeiro(Base):
    __tablename__ = 'financeiro'

    id = Column(Integer, primary_key=True)
    valor = Column("Valor do condomínio", Float)

    # Definição do relacionamento entre o financeiro e um morador.
    # Aqui está sendo definido a coluna 'morador' que vai guardar
    # a referencia ao morador, a chave estrangeira que relaciona
    # um morador ao financeiro.
    morador = Column("apartamento", String(140), ForeignKey("morador.apartamento"), nullable=False)

    def __init__(self, morador:str, valor:float):
        """
        Cria um registro financeiro do morador

        Arguments:
            valor: o valor do condomínio.
            morador: o apartamento do morador relacionado
        """
        self.morador = morador
        self.valor = valor

    # quando for feita uma reserva, retorna o valor do espaço
    def get_valor_do_espaco(self, espaco):
        # se o espaço for salão
        if espaco == "salão":
            return 250
        # se o espaço for a churrasqueira
        return 300
