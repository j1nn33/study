# Структура 
    - K8S/k8s_install_kubeadm    - Установка кластера с помощью kubeadm
    - K8S/k8s_install_kubespray  - Установка кластера с помощью kubespray
    - K8S/minicube               - Установка minicube            

### Aвтоматизация ansible
  ./K8S/ansible/
      - kubeadm                  - автоматизацивя для kubeadm
      - kubespray                - автоматизацивя для kubespray

### Структура приложения 
  ./K8S/app

### infra
  ./K8S/infra/
     - kubernetes-dashboar       - kubernetes-dashboar
     
### Полезное
  ./K8S/useful/
          - network              - сеть и тестирование сети
          - pod_tuning           - настройка параметров пода
           
### Задачи по изучению K8S
  ./K8S/tasks/
           - sl_base             - Вечерняя школа Слёрма по Kubernetes
           - sl_mega
           - k8s_arch
           - kryukov             - заметки о kubernetes

### STAND
######   - расширеное описаниен ./K8S/k8s_install_kubeadm/readme_stand.md
```
bastion    192.168.1.169   ansible
master     192.168.1.170   DNS NFS      
control1   192.168.1.171
control2   192.168.1.172
control3   192.168.1.173
worker1    192.168.1.174
worker2    192.168.1.175
worker3    192.168.1.176
db1        192.168.1.177
```

### План установки кластера 
#####  1.  Подготвока серверов         - ./K8S/k8s_install_kubeadm/readme_stand.md
#####  2.  Развертывание кластера      - ./K8S/ansible/kubeadm 
#####  3.  Постнастрйка калстере       - ./K8S/infra/utils/README.md
######     - Metallb                   - ./K8S/infra/metallb
######     - Устанвока K8S dasboard    - ./K8S/infra/kubernetes-dashboar
######     - Namespaces                - ./K8S/infra/utils/ 
######     - Metrics server            - ./K8S/infra/utils/  
######     - Priority class            - ./K8S/infra/utils/
######     - Reloader                  - ./K8S/infra/utils/  TODO
######     - Cert-manager              - ./K8S/infra/utils/  TODO
#####  4.  Monitoring                  - TODO
#####  5.  ELK                         - TODO
#####  6.  Test                        - ./K8S/useful/test_case/
#####  7.  NFS                         - ./K8S/infra/NFS/
#####  8.  Vault                       - TODO
#####  9.  Jenkins                     - TODO
#####  10. Nexus                       - TODO
#####  11. Helm                        - TODO
#####  11. арр                         - ./K8S/app/README.md
#####  12. ingress                     - ./K8S/infra/ingress/README.md
#####  13. Docker_Podman               - ./K8S/docker_podman/README.md


### Ресурсы & и теория
#### Kubernetes                                           https://kubernetes.io/ru/docs/home/

#### kryukov
#####    - Общее                                          https://www.kryukov.biz/kubernetes/
#####    - План                                           https://www.kryukov.biz/kubernetes/poryadok-prosmotra-video-na-moyom-kanale-dlya-nachinayushhih/
#####    - Установка кластера (video по kubeadm)          https://www.youtube.com/playlist?list=PLmxqUDFl0XM4sJxAocidRKMNzAB48oEnU
#####    - Хранилища в кубере                             https://www.kryukov.biz/kubernetes/lokalnye-volumes/
######                                                    ./K8S/tasks/kryukov/local_volumes
######          - emptyDir                                https://www.kryukov.biz/kubernetes/lokalnye-volumes/emptydir/
######          - hostPath                                https://www.kryukov.biz/kubernetes/lokalnye-volumes/hostpath/
######          - configMap                               https://www.kryukov.biz/kubernetes/lokalnye-volumes/configmap/
######          - secrets                                 https://www.kryukov.biz/kubernetes/lokalnye-volumes/secrets/
######          - downwardAPI                             https://www.kryukov.biz/kubernetes/lokalnye-volumes/downwardapi/
######          - projected                               https://www.kryukov.biz/kubernetes/lokalnye-volumes/projected/
######                                                    ./K8S/tasks/kryukov/pv_volumes
######          - persistent Volume                       ./K8S/tasks/kryukov/pv_volumes_static
######          - PV provisioner  NFS                     ./K8S/tasks/kryukov/pv_volumes_dynamic  
######          - longhorn                                https://www.youtube.com/watch?v=Q7SSlGnXOLY&list=PLmxqUDFl0XM76Hnmsc2UDSvBT9Wf4W8Zl&index=10
######          - Local Path Provisioner                  https://www.youtube.com/watch?v=9H0Wp1Xnbf4&list=PLmxqUDFl0XM76Hnmsc2UDSvBT9Wf4W8Zl&index=11
######
#####    - Сеть                                           https://www.kryukov.biz/kubernetes/set-kubernetes-teoriya/ 
######                                                    https://www.kryukov.biz/kubernetes/set-kubernetes-teoriya/pered/
#####    - DNS и kubernetes                               https://www.kryukov.biz/kubernetes/dns-i-kubernetes/
#####    - Calico                                         https://www.kryukov.biz/kubernetes/set-kubernetes-teoriya/calico/	
######          - calicoctl Calico IPAM                   ./K8S/tasks/kryukov/network/calico.md
######
#####    - metallb                                        ./K8S/infra/metallb
#####    - ingress                                        https://www.youtube.com/watch?v=-kUr-sExQtg&list=PLmxqUDFl0XM6wDtlCkwdjU55z_WeBgBsZ&index=11
######                                                    ./K8S/tasks/kryukov/network/ingress.md
######
######

#### Вечерняя школа Слёрма по Kubernetes.                  https://www.youtube.com/playlist?list=PL8D2P0ruohOA4Y9LQoTttfSgsRwUGWpu6
####                                                       ./K8S/tasks/sl_base/k8s-object/README.txt
####    Разное 

