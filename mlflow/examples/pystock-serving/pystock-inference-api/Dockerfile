FROM condaforge/miniforge3

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /opt/api/
CMD ["mlflow", "models", "serve", \
     "-m", "models:/training-model-pystock/Production", \
     "--env-manager", "local", "--host", "0.0.0.0", "--port", "12000"]
