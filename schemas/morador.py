from pydantic import BaseModel
from typing import Optional, List
from model.morador import Morador

from schemas.reserva import ReservaSchema


class MoradorSchema(BaseModel):
    """ Define como um novo morador a ser inserido deve ser representado
    """
    apartamento: str = "Número e bloco do apartamento"
    nome: str = "Nome do morador"
    email: str = "Email do morador"


class MoradorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no apartamento do morador.
    """
    apartamento: str = "Apartamento do morador"


class ListagemMoradoresSchema(BaseModel):
    """ Define como uma listagem de moradores será retornada.
    """
    moradores:List[MoradorSchema]


def apresenta_moradores(moradores: List[Morador]):
    """ Retorna uma representação do morador seguindo o schema definido em
        MoradorViewSchema.
    """
    result = []
    for morador in moradores:
        result.append({
            "apartamento": morador.apartamento,
            "nome": morador.nome,
            "email": morador.email
        })

    return {"morador": result}


class MoradorViewSchema(BaseModel):
    """ Define como um morador será retornado: morador + reservas.
    """
    id: int = 1
    apartamento: str = "Número e bloco do apartamento"
    nome: str = "Nome do morador"
    total_reservas: int = 1
    reservas:List[ReservaSchema]


class MoradorDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    apartamento: str

def apresenta_morador(morador: Morador):
    """ Retorna uma representação do morador seguindo o schema definido em
        MoradorViewSchema.
    """
    return {
        "id": morador.id,
        "apartamento": morador.apartamento,
        "nome": morador.nome,
        "email": morador.email
    }
