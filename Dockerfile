ARG PYTHON_BASE=3.12-slim
# estágio de construção da imagem
FROM python:$PYTHON_BASE AS builder

# instala PDM
RUN pip install -U pdm
# desabilita verificação de atualização
ENV PDM_CHECK_UPDATE=false
# copia arquivos
COPY pyproject.toml pdm.lock README.md /app/
COPY . /app

# instala dependências e projeta no diretório de pacotes locais
WORKDIR /app
RUN pdm install --check --prod --no-editable

# estágio de execução
FROM python:$PYTHON_BASE

# Instala uvicorn globalmente
RUN pip install "uvicorn[standard]"

# recupera pacotes do estágio de construção
COPY --from=builder /app/.venv/ /app/.venv/
COPY --from=builder /app/ /app/
WORKDIR /app

# Configura o PYTHONPATH para incluir o site-packages do ambiente virtual
ENV PYTHONPATH="/app/.venv/lib/python3.12/site-packages:/app:${PYTHONPATH}"

CMD ["/usr/local/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]