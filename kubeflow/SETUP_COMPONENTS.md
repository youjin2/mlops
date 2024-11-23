## 1. Install Kubeflow

### 1-1. Prepare Setup File
We will use `Kubeflow v1.4.0` in this project. Clone [kubeflow/manifests Repository] repo and checkout to v1.4.

```bash
$ git clone -b v1.4-branch https://github.com/kubeflow/manifests.git
$ cd manifests
```


### 1-2. Install Cert-manager
[Cert-Manager] is a widely-used Kubernetes operator that declaratively manages TLS certificates using Kubernetes resources.

1) Install cert-manager
    ```bash
    $ kustomize build common/cert-manager/cert-manager/base | kubectl apply -f -
    ```
    
2) Wait until all 3-pods are running
    ```bash
    $ kubectl get pod -n cert-manager

    # expected result
    NAME                                       READY   STATUS    RESTARTS   AGE
    cert-manager-webhook-6b57b9b886-srxvh      1/1     Running   0          28s
    cert-manager-cainjector-64c949654c-t8cng   1/1     Running   0          28s
    cert-manager-7dd5854bb4-25kcj              1/1     Running   0          28s
    ```

3) Install kubeflow-issuer (manage the lifecycle of TLS certificates with cert-manager)
    ```bash
    $ kustomize build common/cert-manager/kubeflow-issuer/base | kubectl apply -f -

    # expected result
    clusterissuer.cert-manager.io/kubeflow-self-signing-issuer created
    ```


### 1-3. Install Istio


## 2. Install MLflow Tracking Server


## 3. Install Seldon-Core


## 4. Install Prometheus & Grafana



[kubeflow/manifests Repository]: https://github.com/kubeflow/manifests
[Cert-Manager]: https://www.deploykf.org/guides/dependencies/cert-manager/
