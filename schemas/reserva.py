from typing import List
from pydantic import BaseModel

from datetime import datetime

from model.reserva import Reserva


class ReservaSchema(BaseModel):
    """ Define como uma nova reserva a ser inserida deve ser representada
    """
    morador: str = "Apartamento do morador"
    espaco: str = "Churrasqueira ou Salão!"
    data: str = "Data combinada com o morador"

def apresenta_reservas(reservas: List[Reserva]):
    """ Retorna uma representação da reserva seguindo o schema definido em
        MoradorViewSchema.
    """
    result = []
    for reserva in reservas:
        result.append({
            "apartamento": reserva.morador,
            "espaco": reserva.espaco,
            "data": reserva.data_reserva.strftime('%d/%m/%Y')
        })

    return {"reserva": result}


