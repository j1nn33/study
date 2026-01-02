### Структура 
    - K8S/k8s_install_kubeadm    - Установка кластера с помощью kubeadm
    - K8S/k8s_install_kubespray  - Установка кластера с помощью kubespray
    - K8S/minicube               - Установка minicube            

### Aвтоматизация ansible
    - ./K8S/ansible/
    - kubeadm                    - автоматизацивя для kubeadm
    - kubespray                  - автоматизацивя для kubespray

### Структура приложения 
    - ./K8S/app

### infra
    - ./K8S/infra/
    - kubernetes-dashboar       - kubernetes-dashboar
     
### Полезное
    - ./K8S/useful/
    - network                   - сеть и тестирование сети
    - pod_tuning                - настройка параметров пода
    - tets_case                 - тестовые кейсы
    - timezone                  - настройка времени в поде
    - cert_update               - обновление сертификатов 
           
#### Задачи по изучению K8S
    - ./K8S/tasks/
      - sl_base                 - Вечерняя школа Слёрма по Kubernetes
      - sl_mega
      - k8s_arch
      - kryukov                 - заметки о kubernetes по материалам сайта (с некоторой попровакой) https://www.kryukov.biz/kubernetes/ 

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
MetalLB    192.168.1.180
```

### План установки кластера 
```
  1.  Подготвока серверов         - ./K8S/k8s_install_kubeadm/readme_stand.md
  2.  Развертывание кластера      - ./K8S/ansible/kubeadm 
  3.  Постнастрйка калстере       - ./K8S/infra/utils/README.md
      - Namespaces                - ./K8S/infra/utils/ 
      - Metrics server            - ./K8S/infra/utils/  
      - Priority class            - ./K8S/infra/utils/
      - Reloader                  - ./K8S/infra/utils/                                     
      - Cert-manager              - ./K8S/infra/utils/                                     
  4.  Test                        - ./K8S/useful/test_case/
  5.  ingress                     - ./K8S/infra/ingress/README.md
  6.  Устанвока K8S dasboard      - ./K8S/infra/kubernetes-dashboar
  7.  Monitoring                  - ./K8S/infra/monotoring/README.md  
  8.  ELK                         - ./K8S/infra/ELK/README.md                         
  
```  
### OTHER 
```

   1. NFS                         - ./K8S/infra/NFS/
   2. Vault                       -                                                        TODO
   3. Jenkins                     -                                                        TODO
   4. Nexus                       -                                                        TODO
   5. Helm                        - ./K8S/helm/READ.ME                                     
   6. арр                         - ./K8S/app/README.md
   7. Docker_Podman               - ./K8S/docker_podman/README.md
   8. metallb                     - ./K8S/infra/metallb
   9. Security                    - ./K8S/security                                         
        - Network Policies        - ./K8S/tasks/kryukov/network_policies/README.md       
        - Calico Network Polices  - ./K8S/tasks/kryukov/calico_network_polices/README.md      
        - RBAC                    - ./K8S/security/RBAC.md
  10. ArgoCD                      - 
  11. GATEWAY API                 - ./K8S/gateway_api/gateway_api.md
  12. istio                       - ./K8S/istio/istio.md
  13. tracing                     - 
```
### Ресурсы & и теория
##### Kubernetes                                   https://kubernetes.io/ru/docs/home/

##### kryukov
```
  - Общее                                          https://www.kryukov.biz/kubernetes/
  - План                                           https://www.kryukov.biz/kubernetes/poryadok-prosmotra-video-na-moyom-kanale-dlya-nachinayushhih/
  - Установка кластера (video по kubeadm)          https://www.youtube.com/playlist?list=PLmxqUDFl0XM4sJxAocidRKMNzAB48oEnU
  - Хранилища в кубере                             https://www.kryukov.biz/kubernetes/lokalnye-volumes/
                                                   ./K8S/tasks/kryukov/local_volumes
         - emptyDir                                https://www.kryukov.biz/kubernetes/lokalnye-volumes/emptydir/
         - hostPath                                https://www.kryukov.biz/kubernetes/lokalnye-volumes/hostpath/
         - configMap                               https://www.kryukov.biz/kubernetes/lokalnye-volumes/configmap/
         - secrets                                 https://www.kryukov.biz/kubernetes/lokalnye-volumes/secrets/
         - downwardAPI                             https://www.kryukov.biz/kubernetes/lokalnye-volumes/downwardapi/
         - projected                               https://www.kryukov.biz/kubernetes/lokalnye-volumes/projected/
                                                   ./K8S/tasks/kryukov/pv_volumes
         - persistent Volume                       ./K8S/tasks/kryukov/pv_volumes_static
         - PV provisioner  NFS                     ./K8S/tasks/kryukov/pv_volumes_dynamic  
         - longhorn                                https://www.youtube.com/watch?v=Q7SSlGnXOLY&list=PLmxqUDFl0XM76Hnmsc2UDSvBT9Wf4W8Zl&index=10
         - Local Path Provisioner                  https://www.youtube.com/watch?v=9H0Wp1Xnbf4&list=PLmxqUDFl0XM76Hnmsc2UDSvBT9Wf4W8Zl&index=11

  - Сеть                                           https://www.kryukov.biz/kubernetes/set-kubernetes-teoriya/ 
                                                   https://www.kryukov.biz/kubernetes/set-kubernetes-teoriya/pered/
    - DNS и kubernetes                             https://www.kryukov.biz/kubernetes/dns-i-kubernetes/
    - Calico                                       https://www.kryukov.biz/kubernetes/set-kubernetes-teoriya/calico/	
         - calicoctl Calico IPAM                   ./K8S/tasks/kryukov/network/calico.md
  
    - metallb                                      ./K8S/infra/metallb
    - ingress                                      https://www.youtube.com/watch?v=-kUr-sExQtg&list=PLmxqUDFl0XM6wDtlCkwdjU55z_WeBgBsZ&index=11
                                                   ./K8S/tasks/kryukov/network/ingress.md
    - Network Policies                             ./K8S/tasks/kryukov/network_policies/README.md       
    - Calico Network Polices                       ./K8S/tasks/kryukov/calico_network_polices/README.md      
    - Calico eBPF                                  ./K8S/tasks/kryukov/calico/Calico_eBPF.md
  - RBAC                                           ./K8S/security/RBAC.md
  - Resource Quota                                 ./K8S/tasks/kryukov/resource_quota/readme.md  
  - Priority Class                                 ./K8S/tasks/kryukov/priority_class/readme.md  

```

##### Вечерняя школа Слёрма по Kubernetes.         https://www.youtube.com/playlist?list=PL8D2P0ruohOA4Y9LQoTttfSgsRwUGWpu6
```
                                                   ./K8S/tasks/sl_base/k8s-object/README.txt
```

#####   Разное 

