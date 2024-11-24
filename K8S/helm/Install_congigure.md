##### Install 

```
wget https://get.helm.sh/helm-v3.7.2-linux-amd64.tar.gz
tar -zxvf helm-v3.7.2-linux-amd64.tar.gz

mv linux-amd64/helm /usr/local/bin/helm

helm version
helm list
# NAME    NAMESPACE       REVISION        UPDATED STATUS  CHART   APP VERSION

rm -r helm-v3.7.2-linux-amd64.tar.gz linux-amd64
```

##### Configure
```
для того чтобы helm мог в k8s
~/.kube/config
```