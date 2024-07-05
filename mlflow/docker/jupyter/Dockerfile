FROM condaforge/miniforge3:4.14.0-0

RUN apt-get update --yes && \
    apt-get install htop --yes && \
    apt-get install vim --yes && \
    apt-get install gcc --yes && \
    apt-get install g++ --yes && \
    apt-get install libpq-dev --yes && \
    apt-get install python-dev --yes

ARG MLFLOW_VERSION
ARG MLFLOW_ARTIFACT_STORE
RUN pip install mlflow==${MLFLOW_VERSION} psycopg2==2.8.*

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /opt/project
