import re
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from schemas.financeiro import *
from schemas.reserva import *
from schemas.ocorrencia import *

from model import Session
from model.morador import Morador
from model.reserva import Reserva
from model.financeiro import Financeiro
from model.ocorrencia import Ocorrencia

from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Tech Condomínio", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
morador_tag = Tag(name="Morador", description="Adição, visualização e remoção de moradores à base")
reserva_tag = Tag(name="Reserva", description="Adição e visualização de uma reserva à um morador cadastrado na base")
financeiro_tag = Tag(name="Financeiro", description="Visualização de registros financeiros dos moradores")
ocorrencia_tag = Tag(name="Ocorrência", description="Adição e visualização de uma ocorrência à um morador cadastrado na base")

# definindo valor padrão do condomínio
valor_condomínio = 2000

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

############## MORADORES ##############
@app.post('/morador', tags=[morador_tag],
          responses={"200": MoradorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_morador(form: MoradorSchema):
    """Adiciona um novo Morador à base de dados

    Retorna uma representação dos moradores.
    """
    morador = Morador(
        apartamento=form.apartamento,
        nome=form.nome)
    logger.debug(f"Adicionando morador de apartamento: '{morador.apartamento}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando morador
        session.add(morador)
        # efetivando o comando de adição de novo morador na tabela
        session.commit()
        logger.debug(f"Adicionado morador de apartamento: '{morador.apartamento}'")

        financeiro = Financeiro(
            morador=form.apartamento,
            valor=valor_condomínio)
        # adicionando registro financeiro do morador
        session.add(financeiro)
        # efetivando o comando de adição de novo registro na tabela
        session.commit()
        return apresenta_morador(morador), 200

    except IntegrityError as e:
        # como a duplicidade do apartamento é a provável razão do IntegrityError
        error_msg = "Morador de mesmo apartamento já salvo na base"
        logger.warning(f"Erro ao adicionar morador '{morador.apartamento}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível adicionar morador"
        logger.warning(f"Erro ao adicionar morador de apartamento '{morador.apartamento}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/moradores', tags=[morador_tag],
         responses={"200": ListagemMoradoresSchema, "404": ErrorSchema})
def get_moradores():
    """Faz a busca por todos os Moradores cadastrados

    Retorna uma representação da listagem de moradores.
    """
    logger.debug("Coletando moradores...")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    moradores = session.query(Morador).all()

    if not moradores:
        # se não há moradores cadastrados
        return {"moradores": []}, 200
    else:
        logger.debug(f"%d Moradores econtrados" % len(moradores))
        # retorna a representação de moradores
        return apresenta_moradores(moradores), 200


@app.get('/morador', tags=[morador_tag],
         responses={"200": MoradorViewSchema, "404": ErrorSchema})
def get_morador(query: MoradorBuscaSchema):
    """Faz a busca por um morador a partir do apartamento.

    Retorna uma representação dos moradores à partir do apartamento.
    """
    morador_apartamento = query.apartamento
    logger.debug(f"Coletando dados sobre morador de apartamento #{morador_apartamento}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    morador = session.query(Morador).filter(Morador.apartamento == morador_apartamento)
    apartamento = morador.first()

    if not apartamento:
        # se o morador não foi encontrado
        error_msg = "Morador não encontrado na base :/"
        logger.warning(f"Erro ao buscar morador de apartamento '{morador_apartamento}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Morador econtrado, apartamento: '{morador_apartamento}'")
        # retorna a representação do morador
        return apresenta_morador(apartamento), 200


@app.delete('/morador', tags=[morador_tag],
            responses={"200": MoradorDelSchema, "404": ErrorSchema})
def del_morador(query: MoradorBuscaSchema):
    """Deleta um Morador a partir do apartamento do morador informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    morador_apartamento = unquote(unquote(query.apartamento))
    print(morador_apartamento)
    logger.debug(f"Deletando dados sobre morador #{morador_apartamento}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Morador).filter(Morador.apartamento == morador_apartamento).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado morador #{morador_apartamento}")
        return {"message": "Morador removido", "id": morador_apartamento}
    else:
        # se o morador não foi encontrado
        error_msg = "Morador não encontrado na base :/"
        logger.warning(f"Erro ao deletar morador #'{morador_apartamento}', {error_msg}")
        return {"message": error_msg}, 404


############## RESERVAS ##############
@app.post('/reserva', tags=[reserva_tag],
          responses={"200": MoradorViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def add_reserva(form: ReservaSchema):
    """Adiciona uma nova reserva à um morador cadastrado na base identificado pelo apartamento

    Retorna uma representação dos morador e reservas associadas.
    """
    morador_id  = form.morador
    logger.debug(f"Adicionando reserva ao morador de apartamento #{morador_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo morador
    morador = session.query(Morador).filter(Morador.apartamento == morador_id).first()

    if not morador:
        # se o morador não for encontrado
        error_msg = "Morador não encontrado na base"
        logger.warning(f"Erro ao adicionar reserva do morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 404

    # criando a reserva
    espaco_str = form.espaco
    data_str = form.data
    espaco = espaco_str.lower()

    if (espaco != "salão" and espaco != "churrasqueira"):
        # se o espaço informado for invalido
        error_msg = "O espaço informado deve ser Salão ou Churrasqueira"
        logger.warning(f"Erro ao adicionar reserva do morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 400
    
    if not data_str:
        # se a data for vazia
        error_msg = "Data não informada"
        logger.warning(f"Erro ao adicionar reserva do morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 400

    # Validar o formato da data
    date_pattern = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"
    found = re.match(date_pattern, data_str) # Returns Match object

    if not found:
        # se o formato não for correto
        error_msg = "Data deve ser informada no formato dd/mm/aaaa"
        logger.warning(f"Erro ao adicionar reserva do morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 400

    # convertendo string para tipo data
    data = datetime.strptime(data_str, "%d/%m/%Y")

    if data < datetime.now():
        # se a data for menor que a atual
        error_msg = "Não pode ser feito reservas para o passado"
        logger.warning(f"Erro ao adicionar reserva do morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 400

    # busca pela data e espaço solicitados
    validacao_espaco = session.query(Reserva).filter(Reserva.data_reserva == data).filter(Reserva.espaco == espaco).first()
    if validacao_espaco:
        # se já existir uma reserva para mesma data e espaço
        error_msg = "Já existe uma reserva para esse espaço nessa data"
        logger.warning(f"Erro ao adicionar reserva do morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 400

    # criando a reserva
    reserva = Reserva(morador_id, espaco, data)

    # adicionando reserva do morador
    morador.adiciona_reserva(reserva)
    session.commit()

    # cobrando o valor da reserva
    financeiro = session.query(Financeiro).filter(Financeiro.morador == morador_id).first()

    if financeiro:
        valor_reserva = financeiro.get_valor_do_espaco(espaco)
        session.query(Financeiro).filter(Financeiro.morador == morador_id).\
        update({Financeiro.valor: Financeiro.valor + valor_reserva}, synchronize_session=False)
        session.commit()

    logger.debug(f"Adicionado reserva do morador #{morador_id}")

    # retorna a representação dos valores da reserva
    return apresenta_valores_da_reserva(financeiro, espaco), 200

@app.get('/reserva', tags=[reserva_tag],
         responses={"200": ListagemMoradoresSchema, "404": ErrorSchema})
def get_reservas():
    """Faz a busca por todos as reservas cadastradas

    Retorna uma representação da listagem de reservas.
    """
    logger.debug("Coletando reservas...")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    reservas = session.query(Reserva).all()

    if not reservas:
        # se não há reservas cadastradas
        return {"reservas": []}, 200
    else:
        logger.debug(f"%d Reservas econtradas" % len(reservas))
        # retorna a representação de reservas
        print(reservas)
        return apresenta_reservas(reservas), 200

############## FINANCEIRO ##############
@app.get('/financeiro', tags=[financeiro_tag],
         responses={"200": FinanceiroViewSchema, "404": ErrorSchema})
def get_financas(query: FinanceiroBuscaSchema):
    """Faz a busca por todos os registros financeiros cadastrados

    Retorna uma representação da listagem de registros.
    """
    logger.debug("Coletando registros...")

    morador_id = query.morador
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    financeiro = session.query(Financeiro).filter(Financeiro.morador == morador_id).first()

    if not financeiro:
        # se o registro não for encontrado
        error_msg = "Registro desse morador não encontrado na base"
        logger.warning(f"Erro ao buscar registro do morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Morador econtrado, apartamento: '{morador_id}'")
        # retorna a representação financeira do morador
        return apresenta_financas(financeiro), 200

############## OCORRÊNCIAS ##############
@app.post('/ocorrencia', tags=[ocorrencia_tag],
          responses={"200": MoradorViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def add_ocorrencia(form: OcorrenciaSchema):
    """Adiciona de uma nova ocorrência à um morador cadastrado na base identificado pelo apartamento

    Retorna uma representação dos morador e ocorrência associadas.
    """
    advertencia = "Advertência"
    multa = "Multa"
    morador_id  = form.morador

    logger.debug(f"Adicionando ocorrência ao morador #{morador_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo morador
    morador = session.query(Morador).filter(Morador.apartamento == morador_id).first()

    if not morador:
        # se o morador não for encontrado
        error_msg = "Morador não encontrado na base"
        logger.warning(f"Erro ao adicionar ocorrência ao morador '{morador_id}', {error_msg}")
        return {"message": error_msg}, 404

    # criando a reserva
    motivo = form.motivo
    data_str = form.data

    if not motivo:
        # se não for informado o motivo
        error_msg = "O motivo da advertência deve ser informado"
        logger.warning(f"Erro ao adicionar ocorrência ao morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 400
    
    if not data_str:
        # se a data for vazia
        error_msg = "Data não informada"
        logger.warning(f"Erro ao adicionar ocorrência ao morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 400

    # validar o formato da data
    date_pattern = "^[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}$"
    found = re.match(date_pattern, data_str) # Returns Match object

    if not found:
        # se o formato não for correto
        error_msg = "Data deve ser informada no formato dd/mm/aaaa"
        logger.warning(f"Erro ao adicionar ocorrência ao morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 400

    # convertendo string para tipo data
    data = datetime.strptime(data_str, "%d/%m/%Y")

    if data > datetime.now():
        # se a data for menor que a atual
        error_msg = "Não pode ser registrada uma ocorrência futura"
        logger.warning(f"Erro ao adicionar ocorrência ao morador de apartamento '{morador_id}', {error_msg}")
        return {"message": error_msg}, 400

    # criando a ocorrência
    ocorrencia = Ocorrencia(morador_id, advertencia, motivo, data)

    # adicionando ocorrência ao morador
    session.add(ocorrencia)
    session.commit()

    count = session.query(Ocorrencia).filter(Ocorrencia.morador == morador_id).filter(Ocorrencia.tipo == advertencia).count()
    count_advertencia = count % 3
    logger.warning("Numero de advertencias %d" % count)
    if(count_advertencia == 0):
        # cobrando o valor da multa
        financeiro = session.query(Financeiro).filter(Financeiro.morador == morador_id).first()
        if financeiro:
            valor_multa = financeiro.get_valor_da_multa()
            session.query(Financeiro).filter(Financeiro.morador == morador_id).\
            update({Financeiro.valor: Financeiro.valor + valor_multa}, synchronize_session=False)
            session.commit()
        
        motivo_multa = ("O Morador do apartamento %s atingiu 3 advertências e recebeu uma multa no valor de R$ %d." % (morador_id, valor_multa))
        ocorrencia_multa = Ocorrencia(morador_id, multa, motivo_multa, data)
        session.add(ocorrencia_multa)
        session.commit()
        
        ocorrencias = [ocorrencia, ocorrencia_multa]
        return apresenta_ocorrencias(ocorrencias)
    
    # retorna a representação da ocorrência
    return apresenta_ocorrencia(ocorrencia), 200

@app.get('/ocorrencia', tags=[ocorrencia_tag],
         responses={"200": ListagemMoradoresSchema, "404": ErrorSchema})
def get_ocorrencias():
    """Faz a busca por todas as ocorrências cadastradas

    Retorna uma representação da listagem de ocorrências.
    """
    logger.debug("Coletando ocorrências...")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    ocorrencias = session.query(Ocorrencia).all()

    if not ocorrencias:
        # se não há ocorrências cadastradas
        return {"ocorrências": []}, 200
    else:
        logger.debug(f"%d Ocorrências econtradas" % len(ocorrencias))
        # retorna a representação de reservas
        print(ocorrencias)
        return apresenta_ocorrencias(ocorrencias), 200
