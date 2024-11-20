## Introduction

## Setup Kubeflow
### Install Docker

### Turn Off Swap Memory


### Install Kubectl
```bash
# 
$ curl -LO https://dl.k8s.io/release/v1.21.7/bin/linux/amd64/kubectl
```

```bash
$ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# check install
$ kubectl version --client
```

```bash
$ kubectl version --client

# Client Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.7", GitCommit:"1f86634ff08f37e54e8bfcd86bc90b61c98f84d4", GitTreeState:"clean", BuildDate:"2021-11-17T14:41:19Z", GoVersion:"go1.16.10", Compiler:"gc", Platform:"linux/amd64"}
```



## References
- [Kubeflow for Machine Learning: From Lab to Production, 1st Edition]
- [mlops-for-all with Kubeflow]

[Kubeflow for Machine Learning: From Lab to Production, 1st Edition]: https://www.amazon.com/Kubeflow-Machine-Learning-Lab-Production/dp/1492050121
[mlops-for-all with Kubeflow]: https://mlops-for-all.github.io/docs/introduction/intro
