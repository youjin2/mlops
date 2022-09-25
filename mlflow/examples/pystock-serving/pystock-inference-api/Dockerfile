FROM condaforge/miniforge3

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /batch_scoring/

#ENV MLFLOW_TRACKING_URI=http://mlflow:5000
#ENV MLFLOW_TRACKING_URI=http://localhost:5000

WORKDIR /batch_scoring/
#ENTRYPOINT ["mlflow run . --env-manager local"]
