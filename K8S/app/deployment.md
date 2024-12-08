

####
#### annotations


###### annotations: 
```
- подя для других программ 
  пример - указание для reloader перезагружать поды если менятеся configmap
           ./study/K8S/infra/utils/test-app.yaml
           ./study/K8S/infra/utils/README.md
```
```yaml
annotations:
  reloader.stakater.com/auto: "true"
  configmap.reloader.stakater.com/reload: "index-html"
```  