ARG PYTHON_BASE=3.12-slim

# Build stage
FROM python:$PYTHON_BASE as build

COPY pyproject.toml pdm.lock README.md ./

# Install pdm
RUN python -m pip install --upgrade pip setuptools wheel &&\
    pip install pdm

# Install dependencies
RUN pdm install --no-lock --no-editable

# Run stage
FROM python:$PYTHON_BASE

RUN apt update -y && apt install ffmpeg -y && apt install -y tzdata \
&& ln -fs /usr/share/zoneinfo/America/Bahia /etc/localtime \
&& dpkg-reconfigure --frontend noninteractive tzdata

# Copy application files
COPY src /src
COPY --from=build /.venv /.venv
ENV PATH="/.venv/bin:{$PATH}"

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]