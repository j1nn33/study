#### Set up the Istio ingress gateway
#### Configure HTTP routing




##### Set up the Istio ingress gateway
```
configure the Istio ingress gateway. The gateway configuration is kept simple and consists of the two required spec sections gatewayClassName and listeners.
```

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: Gateway
metadata:
  name: gw-api
  namespace: istio-system
spec:
  gatewayClassName: istio
  # define two listeners, one for HTTP and one for HTTPS traffic
  listeners:
    - name: http
      hostname: "*.danielstechblog.de"
      port: 80
      protocol: HTTP
      allowedRoutes:
        namespaces:
          from: Same
        kinds:
          - group: gateway.networking.k8s.io
            kind: HTTPRoute
    - name: https
      hostname: "*.danielstechblog.de"
      port: 443
      protocol: HTTPS
      allowedRoutes:
        namespaces:
          from: Selector
          selector:
            matchLabels:
              ingress-configuration: "true"
        kinds:
          - group: gateway.networking.k8s.io
            kind: HTTPRoute
      tls:
        mode: Terminate
        certificateRefs:
          - kind: Secret
            group: ""
            name: istio-ingress-cert
            namespace: istio-system 
```
```
The one for HTTP traffic restricts the route configuration to the same namespace in which the Istio ingress gateway gets deployed. We will talk about the why in the section about the HTTP to HTTPS traffic redirection. Also, the route configuration is restricted to the kind HTTPRoute.

Allowed routes can be configured beside the value Same with two other values. All to allow route configuration from every namespace or Selector to allow them only from namespaces with a specific label as seen in the HTTPS listener configuration below.

The HTTPS listener configuration has an additional tls section for the HTTPS configuration. Which mode should be used, Terminate or Passthrough

Furthermore, we specify at least one certificate reference. Per default, the certificate reference uses the same namespace as the ingress gateway.
```

##### Configure HTTP routing

```
Let us start with the routing configuration for the HTTP to HTTPS redirect.

```

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: HTTPRoute
metadata:
  name: http-to-https-redirect
  namespace: istio-system
spec:
  parentRefs:
    - name: gw-api
      namespace: istio-system
  hostnames:
    - "*.danielstechblog.de"
  rules:
    - filters:
        - type: RequestRedirect
          requestRedirect:
            scheme: https
            statusCode: 301
            port: 443

```
```
In the case of the redirect, we use a filter of type RequestRedirect. Even we use the scheme https, we must specify the port, 443, as otherwise, the redirect uses port 80.
```
