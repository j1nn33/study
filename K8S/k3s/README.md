##### INSTALL 
```bash
curl -sfL https://get.k3s.io | sh -

tail -f /var/log/messages
systemctl status k3s.service


# splash systemd.unified_cgroup_hierarchy=1
vi /etc/default/grub

```
```
cat /etc/default/grub
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="crashkernel=auto resume=/dev/mapper/almalinux-swap rd.lvm.lv=almalinux/root rd.lvm.lv=almalinux/swap rhgb quiet splash systemd.unified_cgroup_hierarchy=1"
GRUB_DISABLE_RECOVERY="true"
GRUB_ENABLE_BLSCFG=true
```
```bash
grub2-mkconfig -o /boot/grub2/grub.cfg
reboot

# cp /etc/rancher/k3s/k3s.yaml /root/.kube/kube.yaml
# export KUBECONFIG=/root/.kube/kube.yaml
cp /etc/rancher/k3s/k3s.yaml /root/.kube/config


kubectl get pods -A
```

##### Поставить ArgpCd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml  --server-side --force-conflicts