## 1. Introduction

## 2. Setup Kubeflow
### 2-1. Requirements
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


### 2-2. Install Docker

### 2-3. Turn Off Swap Memory


### 2-4. Install Kubectl
Kubectl is a client tool used to request an API call to the Kubernetes cluster.

Install Kubectl on a client as follows:

1) download kubectl to the current path
    ```bash
    # amd64 (e.g. ubuntu)
    $ curl -LO https://dl.k8s.io/release/v1.21.7/bin/linux/amd64/kubectl

    # arm64 (e.g. apple silicon chip)
    $ curl -LO https://dl.k8s.io/release/v1.21.7/bin/linux/arm64/kubectl
    ```

2) update permission and location of kubectl
    ```bash
    $ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

    # check install
    $ kubectl version --client
    ```

3) check if the installation completed properly
    ```bash
    $ kubectl version --client

    # Client Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.7", GitCommit:"1f86634ff08f37e54e8bfcd86bc90b61c98f84d4", GitTreeState:"clean", BuildDate:"2021-11-17T14:41:19Z", GoVersion:"go1.16.10", Compiler:"gc", Platform:"linux/amd64"}
    ```



## References
- [Kubeflow for Machine Learning: From Lab to Production, 1st Edition]
- [mlops-for-all with Kubeflow]

[Kubeflow for Machine Learning: From Lab to Production, 1st Edition]: https://www.amazon.com/Kubeflow-Machine-Learning-Lab-Production/dp/1492050121
[mlops-for-all with Kubeflow]: https://mlops-for-all.github.io/docs/introduction/intro
