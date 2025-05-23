# PRimeira etapa: instalar os pacotes do Python
# Monstar a estrutura de arquivos da aplicac'ão
FROM python:3.12-slim as construtor

SHELL ["/bin/bash", "-c"]


WORKDIR /projeto

COPY requirements.txt /projeto

# Instalar meus pacotes
RUN python -m venv venv && \
  .  venv/bin/activate && \
  pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Imagem final a ser entregue / conterá a minha aplicação
FROM python:3.12-slim

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH=/projeto/venv/bin:$PATH


WORKDIR /projeto
COPY --from=construtor /projeto/venv /projeto/venv
COPY app /projeto/app
COPY requirements.txt /projeto

RUN python -m compileall app

EXPOSE 8000

CMD [ "uvicorn", "app.main_api:app", "--host", "0.0.0.0", "--port", "8000" ]

# Montagem
# docker build -f ./devtools/Dockerfile -t pc/todolist:0.0.1 .
# Execução
# docker run --rm -p 8000:8000 pc/todolist:0.0.1