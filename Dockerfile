# Imagem base.
FROM python:3.7.4

# Configura o diretório base do container.
WORKDIR /app

# Copia o requirements.txt para o container e instala as deps.
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copia o restante do projeto.
COPY . /app

# Roda o server de desenvolvimento.
CMD python manage.py run -h 0.0.0.0