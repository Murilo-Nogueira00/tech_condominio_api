# Tech Condomínio API

Este projeto é a entrega do MVP da disciplina Arquitetura de Software do curso de pós-graduação de Engenharia de Software na PUC RIO

---
## Como executar 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

## Dockerização da aplicação

Faça o download e instale o Docker Desktop na versão mais recente e compatível com seu PC.

Crie uma imagem para essa aplicação rodando o seguinte comando, chamaremos esta imagem de componente-b:

```
docker build -t componente-b:latest .
```

Depois da imagem criada, iniciaremos o container com o seguinte comando:

```
docker run -p 5000:5000 componente-b
```

## Integração com a interface de usuário

Para um melhor aproveitamento da aplicação, é recomendado que o usuário acesse o repositório do front-end da aplicação no link:

```
https://github.com/Murilo-Nogueira00/tech_condominio_front.git
```

*Acesse o README do repositório front-end para mais informações.

## Integração com a API de emails

Para um melhor aproveitamento da aplicação, é recomendado que o usuário acesse o repositório da API de emails acessando o link:

```
https://github.com/Murilo-Nogueira00/tech_condominio_email.git
```

*Acesse o README do repositório para mais informações.
