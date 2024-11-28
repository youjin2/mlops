## 1. Introduction
According to the whitepaper [Practitioners guide to MLOps: A framework for continuous delivery and automation of machine learning], MLOps consists of several components including `Experiment`, `Data Processing`, `Model Training`, `Model Evaluation`, `Model Serving`, `ML Pipeline`, etc. In order to manage and operate these components efficiently, the need for container and orchestration system emerges.

[Kubernetes], also known as K8s, is an open source system for automating deployment, scaling, and management of containerized applications. It is widely applied to build MLOps system because it's scalabiliy, orchestration and resource management enable efficient workflow for model training, deployment and inference.

In this tutorial, we will first setup a Kubernetes cluster. And then setup several MLOps components including [Kubeflow] and finally implement a Kubeflow pipeline.


## 2. Setup
### 2-1. Setup Kubernetes
See [SETUP_KUBERNETES.md]


### 2-2. Setup Components
We will cover MLOps pipeline working with [Kubeflow], [MLflow Tracking Server], [Seldon-Core], [Prometheus] and [Grafana]. Install each component by following the guidelines below.
- `Kubeflow`
    - Kubeflow is a community and ecosystem of open-source projects to address each stage in the machine learning (ML) lifecycle with support for best-in-class open source tools and frameworks.
    - Install Kubeflow by following [SETUP_KUBEFLOW.md]
- `MLflow Tracking Server`
    - MLflow tracking server is a stand-alone HTTP server that serves multiple REST API endpoints for tracking runs/experiments.
    - Install MLflow by following [SETUP_MLFLOW_TRACKING_SERVER.md]
- `Seldon-Core`
    - Seldon core converts your ML models (Tensorflow, Pytorch, H2o, etc.) or language wrappers (Python, Java, etc.) into production REST/GRPC microservices.
    - Install Seldon-Core by following [SETUP_SELDON_CORE.md]
- `Prometheus & Grafana`
    - Prometheus is an open-source systems monitoring and alerting toolkit originally built at SoundCloud.
    - Grafana is the open source analytics & monitoring solution for every database.
    - Install Prometheus & Grafana by following [SETUP_PROMETHEUS_GRAFANA.md]

### 3-2. MLflow Tracking Server


### 3-3. Seldon-Core

### 3-4. Prometheus & Grafana


## 3. Kubeflow UI Guide


## 4. Kubeflow


<!-- ## 6. API Deployment -->


## References
- [Kubeflow for Machine Learning: From Lab to Production, 1st Edition]
- [mlops-for-all with Kubeflow]
- [Practitioners guide to MLOps: A framework for continuous delivery and automation of machine learning]
- [Kubernetes Install Tools]
- [Helm Releases]
- [Kubeflow]
- [MLflow Tracking Server]
- [Seldon-Core]
- [Prometheus]
- [Grafana]

[Kubeflow for Machine Learning: From Lab to Production, 1st Edition]: https://www.amazon.com/Kubeflow-Machine-Learning-Lab-Production/dp/1492050121
[mlops-for-all with Kubeflow]: https://mlops-for-all.github.io/docs/introduction/intro
[Practitioners guide to MLOps: A framework for continuous delivery and automation of machine learning]: https://services.google.com/fh/files/misc/practitioners_guide_to_mlops_whitepaper.pdf
[Kubernetes]: https://kubernetes.io/
[Kubernetes Install Tools]: https://kubernetes.io/docs/tasks/tools/
[Helm Releases]: https://github.com/helm/helm/releases
[Kubeflow]: https://www.kubeflow.org/docs/started/introduction/
[MLflow Tracking Server]: https://mlflow.org/docs/latest/tracking/server.html
[Seldon-Core]: https://docs.seldon.io/projects/seldon-core/en/latest/nav/concepts.html
[Prometheus]: https://prometheus.io/docs/introduction/overview/
[Grafana]: https://grafana.com/docs/grafana/latest/
[SETUP_KUBERNETES.md]: https://github.com/youjin2/mlops/blob/main/kubeflow/SETUP_KUBERNETES.md
[SETUP_KUBEFLOW.md]: https://github.com/youjin2/mlops/blob/main/kubeflow/SETUP_KUBEFLOW.md
[SETUP_MLFLOW_TRACKING_SERVER.md]: https://github.com/youjin2/mlops/blob/main/kubeflow/SETUP_MLFLOW_TRACKING_SERVER.md
[SETUP_SELDON_CORE.md]: https://github.com/youjin2/mlops/blob/main/kubeflow/SETUP_SELDON_CORE.md
[SETUP_PROMETHEUS_GRAFANA.md]: https://github.com/youjin2/mlops/blob/main/kubeflow/SETUP_PROMETHEUS_GRAFANA.md
