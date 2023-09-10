from typing import List
from pydantic import BaseModel

from datetime import datetime

from model.ocorrencia import Ocorrencia


class OcorrenciaSchema(BaseModel):
    """ Define como uma nova reserva a ser inserida deve ser representada
    """
    morador: str = "Apartamento do morador"
    motivo: str = "O motivo que fez o morador levar uma advertência"
    data: str = "Data da causa da advertência"

def apresenta_ocorrencia(ocorrencia: Ocorrencia):
    """ Retorna uma representação da ocorrência seguindo o schema definido em
        MoradorViewSchema.
    """
    result_ocorrencia = []

    result_ocorrencia.append({
        "morador": ocorrencia.morador,
        "tipo": ocorrencia.tipo,
        "motivo": ocorrencia.motivo,
        "data": ocorrencia.data_ocorrencia.strftime('%d/%m/%Y')
    })

    return {"ocorrência": result_ocorrencia}

def apresenta_ocorrencias(ocorrencias: List[Ocorrencia]):
    """ Retorna uma representação da ocorrência seguindo o schema definido em
        MoradorViewSchema.
    """
    result_ocorrencia = []
    for ocorrencia in ocorrencias:
        result_ocorrencia.append({
            "morador": ocorrencia.morador,
            "tipo": ocorrencia.tipo,
            "motivo": ocorrencia.motivo,
            "data": ocorrencia.data_ocorrencia.strftime('%d/%m/%Y')
        })

    return {"ocorrência": result_ocorrencia}


