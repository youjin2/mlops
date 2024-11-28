## 1. Install Seldon-Core
[Seldon-Core] converts your ML models (Tensorflow, Pytorch, H2o, etc.) or language wrappers (Python, Java, etc.) into production REST/GRPC microservices. It enables deployment and management of many machine learning models in Kubernetes Cluster.

In order to use Seldon-Core, we need modules like [Ambassador] or [Istio] which are responsible for Kubernetes Ingress.

1) Add Ambassador - Helm Repository
    ```bash
    $ helm repo add datawire https://www.getambassador.io

    # expected outputs
    "datawire" has been added to your repositories
    ```

2) Update Ambassador - Helm Repository 
    ```bash
    $ helm repo update

    # expected outputs
    Hang tight while we grab the latest from your chart repositories...
    ...Successfully got an update from the "mlops-for-all" chart repository
    ...Successfully got an update from the "datawire" chart repository
    Update Complete. ⎈Happy Helming!⎈
    ```

3) Install Ambassador - Helm
    ```bash
    $ helm install ambassador datawire/ambassador \
        --namespace seldon-system \
        --create-namespace \
        --set image.repository=quay.io/datawire/ambassador \
        --set enableAES=false \
        --set crds.keep=false \
        --version 6.9.3

    # expected outputs
    ...

    NAME: ambassador
    LAST DEPLOYED: Thu Nov 28 18:54:25 2024
    NAMESPACE: seldon-system
    STATUS: deployed
    REVISION: 1
    NOTES:
    -------------------------------------------------------------------------------
      Congratulations! You ve successfully installed Ambassador!

    -------------------------------------------------------------------------------
    To get the IP address of Ambassador, run the following commands:
    NOTE: It may take a few minutes for the LoadBalancer IP to be available.
         You can watch the status of by running 'kubectl get svc -w  --namespace seldon-system ambassador'

      On GKE/Azure:
      export SERVICE_IP=$(kubectl get svc --namespace seldon-system ambassador -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

      On AWS:
      export SERVICE_IP=$(kubectl get svc --namespace seldon-system ambassador -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

      echo http://$SERVICE_IP:

    For help, visit our Slack at http://a8r.io/Slack or view the documentation online at https://www.getambassador.io.
    ```

4) Wait until all 4-pods in `seldon-system` are running
    ```bash
    $ kubectl get pod -n seldon-system

    # expected outputs
    NAME                                READY   STATUS    RESTARTS   AGE
    ambassador-agent-77bccdfcd5-pnr59   1/1     Running   0          101s
    ambassador-7f596c8b57-2269k         1/1     Running   0          101s
    ambassador-7f596c8b57-zp4tj         1/1     Running   0          101s
    ambassador-7f596c8b57-sqx7r         1/1     Running   0          101s
    ```


5) Install Seldon-Core - Helm
    ```bash
    $ helm install seldon-core seldon-core-operator \
        --repo https://storage.googleapis.com/seldon-charts \
        --namespace seldon-system \
        --set usageMetrics.enabled=true \
        --set ambassador.enabled=true \
        --version 1.11.2

    # expected outputs
    ...

    NAME: seldon-core
    LAST DEPLOYED: Thu Nov 28 18:57:07 2024
    NAMESPACE: seldon-system
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    ```

6) Wait until `seldon-controller-manager` pod in `seldon-system` namespace is running
    ```bash
    $ kubectl get pod -n seldon-system | grep seldon-controller

    # expected outputs
    seldon-controller-manager-8457b8b5c7-gb27t   1/1     Running   0          43s
    ```



## References
- [Seldon-Core]
- [Ambassador]
- [Istio]




[Seldon-Core]: https://docs.seldon.io/projects/seldon-core/en/latest/nav/concepts.html
[Ambassador]: https://github.com/basecamp/ambassador
[Istio]: https://istio.io/latest/about/service-mesh/


