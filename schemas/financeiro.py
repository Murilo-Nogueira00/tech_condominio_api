from pydantic import BaseModel
from typing import Optional, List
from model.financeiro import Financeiro
from model.reserva import Reserva

from schemas.reserva import ReservaSchema

representacao = "Número e bloco do apartamento"

class FinanceiroSchema(BaseModel):
    """ Define como um registro deve ser buscado
    """
    morador: str = representacao

class FinanceiroBuscaSchema(BaseModel):

    morador: str = representacao

class FinanceiroViewSchema(BaseModel):
    """ Define como um morador deverá ser informado para obter registros
    """
    apartamento: str = representacao

def apresenta_valores_da_reserva(financeiro: Financeiro, espaco):
    """ Retorna uma representação dos valores da reserva seguindo o schema definido em
        MoradorViewSchema.
    """
    result_financeiro = []

    result_financeiro.append({
        "apartamento": financeiro.morador,
        "espaço": espaco,
        "valor da reserva": financeiro.get_valor_do_espaco(espaco),
        "valor do condomínio": financeiro.valor,
    })

    return {"financeiro": result_financeiro}

def apresenta_financas(financeiro: Financeiro):
    """ Retorna uma representação dos registros seguindo o schema definido em
        FinanceiroViewSchema.
    """
    return {
        "apartamento": financeiro.morador,
        "Valor do condomínio": financeiro.valor,
    }