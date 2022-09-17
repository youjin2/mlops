FROM condaforge/miniforge3

RUN apt-get update --yes && \
    apt-get install htop --yes && \
    apt-get install vim --yes && \
    apt-get install gcc --yes && \
    apt-get install g++ --yes

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /opt/project
