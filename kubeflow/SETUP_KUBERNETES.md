## 1. Requirements
Software requirements are:
| Software | Version |
| -- | -- |
| Ubuntu | 18.04.3 LTS |
| Docker (Server) | 20.10.18 |
| Nvidia-Driver | 510.108.03 |

3rd party softwares need to be installed using helm are:
| Software | Version |
| -- | -- |
| datawire/ambassador | |
| seldonio/seldon-core-operator | |


Client (MacOS; Apple Silicon Chip) requirements are:
| Software | Version |
| -- | -- |
| kubectl | |
| helm | |
| kustomize | |

Minimum system requirements are:
- CPU: 6 core
- RAM: 12 GB
- DISK: 50 GB
- GPU: NVIDIA GPU (Optional)


## 2. Install Prerequisites

### 2-1. Install apt packages
Port-forwarding is required to connect client and cluster.
```bash
$ sudo apt-get update
$ sudo apt-get install -y socat
```

### 2-2. Install Docker

1) Install Docker
    ```bash
    # apt packages required to install docker
    $ sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg lsb-release

    # add docker official GPG key
    $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # when installing docker with apt package, download it from the stable repository
    $ echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # check available docker versions
    $ sudo apt-get update && apt-cache madison docker-ce

    # check if the "5:20.10.11~3-0~ubuntu-focal" exists
    $ apt-cache madison docker-ce | grep 5:20.10.11~3-0~ubuntu-focal

    # expected outputs
    docker-ce | 5:20.10.11~3-0~ubuntu-focal | https://download.docker.com/linux/ubuntu focal/stable amd64 Packages

    # install docker "5:20.10.11~3-0~ubuntu-focal"
    $ sudo apt-get install -y containerd.io docker-ce=5:20.10.11~3-0~ubuntu-focal docker-ce-cli=5:20.10.11~3-0~ubuntu-focal
    ```

2) Check if the installation completed properly
    ```bash
    $ sudo docker run hello-world

    # expected outputs
    Hello from Docker!
    This message shows that your installation appears to be working correctly.

    To generate this message, Docker took the following steps:
    1. The Docker client contacted the Docker daemon.
    2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
       (amd64)
    3. The Docker daemon created a new container from that image which runs the
       executable that produces the output you are currently reading.
    4. The Docker daemon streamed that output to the Docker client, which sent it
       to your terminal.

    To try something more ambitious, you can run an Ubuntu container with:
    $ docker run -it ubuntu bash

    Share images, automate workflows, and more with a free Docker ID:
    https://hub.docker.com/

    For more examples and ideas, visit:
    https://docs.docker.com/get-started/
    ```

3) Use docker commands without the sudo keyword
    ```bash
    $ sudo groupadd docker
    $ sudo usermod -aG docker $USER
    $ newgrp docker
    ```


### 2-3. Turn Off Swap Memory
In order to use kubelet properly, swap memory must be turned-off on the cluster node.
```bash
$ sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
$ sudo swapoff -a
```


### 2-4. Install Kubectl
Kubectl is a client tool used to request an API call to the Kubernetes cluster.

Install Kubectl on a client as follows:

1) Download kubectl to the current path
    ```bash
    # amd64 (e.g. ubuntu)
    $ curl -LO "https://dl.k8s.io/release/v1.21.7/bin/linux/amd64/kubectl"

    # arm64 (e.g. apple silicon chip)
    $ curl -LO "https://dl.k8s.io/release/v1.21.7/bin/darwin/arm64/kubectl"
    ```

2) Update permission and location of kubectl
    ```bash
    # linux
    $ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

    # mac (macOS generally uses wheel as the permission group)
    $ chmod +x ./kubectl
    $ sudo mv ./kubectl /usr/local/bin/kubectl
    $ sudo chown root:wheel /usr/local/bin/kubectl
    ```

3) Check if the installation completed properly
    ```bash
    $ kubectl version --client

    # Client Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.7", GitCommit:"1f86634ff08f37e54e8bfcd86bc90b61c98f84d4", GitTreeState:"clean", BuildDate:"2021-11-17T14:41:19Z", GoVersion:"go1.16.10", Compiler:"gc", Platform:"darwin/arm64"}
    ```

## 3. Install Kubernetes
Before installing the kubernetes cluster, make sure that all the components in [2. Install Prerequisite](#2.-install-prerequisite) are installed.

### 3-1. Install K3s
Although k3s uses `containerd` as the default backend, since we're going to use GPU, we we will use `docker` as the backend.

1) Install prerequisite  
    ```bash
    $ curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=v1.21.7+k3s1 sh -s - server --disable traefik --disable servicelb --disable local-storage --docker
    ```

2) Check if the installation completed properly
    ```bash
    $ sudo cat /etc/rancher/k3s/k3s.yaml

    # expected outputs
    apiVersion: v1
    clusters:
    - cluster:
        certificate-authority-data: ...
        server: https://127.0.0.1:6443
      name: default
    contexts:
    - context:
        cluster: default
        user: default
      name: default
    current-context: default
    kind: Config
    preferences: {}
    users:
    - name: default
      user:
        client-certificate-data: ...
        client-key-data: ...
    ```

Copy k3s config to use it as the cluster's kubeconfig and add permission to the current user

3) Setup kubernetes cluster
    ```bash
    $ mkdir ~/.kube
    $ sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config

    # allow user's permission
    $ sudo chown $USER:$USER ~/.kube/config
    ```


Copy kubeconfig configured in the cluster to the local client and modify the server ip address from `https://127.0.0.1:6443` to `https://{CLUSTER_IP_ADDRESS}.6443`.

4) Setup kubernetes client
    ```bash
    $ mkdir ~/.kube
    $ scp {CLUSTER_USER_ID}@{CLUSTER_IP}:~/.kube/config ~/.kube/config
    ```

5) Check if the node status is ready
    ```bash
    $ kubectl get nodes -o wide

    # expected outputs
    NAME                         STATUS   ROLES                  AGE   VERSION        INTERNAL-IP       EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION      CONTAINER-RUNTIME
    ubuntu                       Ready    control-plane,master   17h   v1.21.7+k3s1   192.168.219.103   <none>        Ubuntu 18.04.3 LTS   5.4.0-150-generic   docker://20.10.18
    ```



### 3-2. Install Kubernetes Modules

1) Install helm (deploy & manage kubernetes packages)
    ```bash
    $ wget https://get.helm.sh/helm-v3.7.1-darwin-arm64.tar.gz
    $ tar -xzvf helm-v3.7.1-darwin-arm64.tar.gz
    $ sudo mv darwin-arm64/helm /usr/local/bin/helm
    ```

2) Install kustomize (deploy & manage multiple kubernetes resources)
    ```bash
    $ wget https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.0.0/kustomize_v5.0.0_darwin_arm64.tar.gz
    $ tar -xzvf kustomize_v5.0.0_darwin_arm64.tar.gz
    $ sudo mv kustomize /usr/local/bin/kustomize
    ```

3) Install local path provisioner csi plugin
    ```bash
    $ kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/v0.0.20/deploy/local-path-storage.yaml

    # expected outputs
    namespace/local-path-storage created
    serviceaccount/local-path-provisioner-service-account created
    clusterrole.rbac.authorization.k8s.io/local-path-provisioner-role created
    clusterrolebinding.rbac.authorization.k8s.io/local-path-provisioner-bind created
    deployment.apps/local-path-provisioner created
    storageclass.storage.k8s.io/local-path created
    configmap/local-path-config created
    ```

4) Check if the provisioner pod in local-path-storage namespace is running
    ```bash
    $ kubectl -n local-path-storage get pod

    # expected outputs
    NAME                                      READY   STATUS    RESTARTS   AGE
    local-path-provisioner-556d4466c8-574rr   1/1     Running   0          126m

    # modify deafult storage class
    $ kubectl patch storageclass local-path  -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

    # expected outputs
    storageclass.storage.k8s.io/local-path patched


    # check if the "local-path (default)" storage class exist
    $ kubectl get sc

    # expected outputs
    NAME                   PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
    local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  127m
    ```

## 4. Setup GPU
1) Install nvidia-driver
    ```bash
    $ sudo add-apt-repository ppa:graphics-drivers/ppa
    $ sudo apt update && sudo apt install -y ubuntu-drivers-common
    $ sudo ubuntu-drivers autoinstall
    $ sudo reboot
    ```

2) Check if the installation completed property
    ```bash
    $ nvidia-smi

    # expected outputs
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 510.108.03   Driver Version: 510.108.03   CUDA Version: 11.6     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |                               |                      |               MIG M. |
    |===============================+======================+======================|
    |   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0 Off |                  N/A |
    | 41%   30C    P0    42W / 175W |      0MiB /  8192MiB |      0%      Default |
    |                               |                      |                  N/A |
    +-------------------------------+----------------------+----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |  No running processes found                                                 |
    +-----------------------------------------------------------------------------+
    ```

3) Install nvidia-docker
    ```bash
    $ curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
      sudo apt-key add -distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    $ curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
    $ sudo apt-get update
    $ sudo apt-get install -y nvidia-docker2 &&
    $ sudo systemctl restart docker
    ```

4) Check if the installation completed property
    ```bash
    # pull docker image
    $ docker pull nvidia/cuda:11.8.0-base-ubuntu18.04

    # run docker image
    $ docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu18.04 nvidia-smi

    # expected outputs
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 510.108.03   Driver Version: 510.108.03   CUDA Version: 11.8     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |                               |                      |               MIG M. |
    |===============================+======================+======================|
    |   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0 Off |                  N/A |
    | 45%   30C    P0    40W / 175W |      0MiB /  8192MiB |      0%      Default |
    |                               |                      |                  N/A |
    +-------------------------------+----------------------+----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |  No running processes found                                                 |
    +-----------------------------------------------------------------------------+
    ```

5) Set nvidia-docker as the default container runtime (add `default-runtime` line below)
    ```bash
    $ sudo vi /etc/docker/daemon.json
    ```
    ```json
    {
        "default-runtime": "nvidia",
        "runtimes": {
            "nvidia": {
                "path": "nvidia-container-runtime",
                "runtimeArgs": []
            }
        },
        "features": {
            "buildkit" : true
        }
    }
    ```

6) Restart docker and check if the update applied successfully
    ```bash
    # restart
    $ sudo systemctl daemon-reload
    $ sudo service docker restart

    # check
    $ sudo docker info | grep nvidia

    # expected outputs
    WARNING: No swap limit support
     Runtimes: io.containerd.runc.v2 io.containerd.runtime.v1.linux nvidia runc
     Default Runtime: nvidia
    ```

7) Create `nvidia-device-plugin` daemonset (run commands below on the local client)
    ```bash
    # create "nvidia-device-plugin" daemonset
    $ kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.10.0/nvidia-device-plugin.yml

    # check if "nvidia-device-plugin" is running
    $ kubectl get pod -n kube-system | grep nvidia

    # expected outputs
    nvidia-device-plugin-daemonset-2lq94   1/1     Running   2          15m

    # check if gpus are available in node info
    $ kubectl get nodes "-o=custom-columns=NAME:.metadata.name,GPU:.status.allocatable.nvidia\.com/gpu"

    # expected outputs
    NAME                         GPU
    ygene2-system-product-name   1
    ```


## References
- [mlops-for-all with Kubeflow]
- [Kubernetes Install Tools]
- [Helm Releases]

[mlops-for-all with Kubeflow]: https://mlops-for-all.github.io/docs/introduction/intro
[Kubernetes Install Tools]: https://kubernetes.io/docs/tasks/tools/
[Helm Releases]: https://github.com/helm/helm/releases
