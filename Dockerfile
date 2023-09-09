# Imagem base de Python
FROM python:3.8-slim

# Define o diretório de trabalho
WORKDIR /usr/src/app

# Copia o arquivo de dependências
COPY requirements.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Indica ao Docker que a aplicação vai escutar na porta 5000
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"] # Ou o comando que você usa para rodar sua aplicação Flask
