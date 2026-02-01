#### Default access log format

Istio will use the following default access log format if accessLogFormat is not specified:
```bash
[%START_TIME%] \"%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%\" %RESPONSE_CODE% %RESPONSE_FLAGS% %RESPONSE_CODE_DETAILS% %CONNECTION_TERMINATION_DETAILS%
\"%UPSTREAM_TRANSPORT_FAILURE_REASON%\" %BYTES_RECEIVED% %BYTES_SENT% %DURATION% %RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)% \"%REQ(X-FORWARDED-FOR)%\" \"%REQ(USER-AGENT)%\" \"%REQ(X-REQUEST-ID)%\"
\"%REQ(:AUTHORITY)%\" \"%UPSTREAM_HOST%\" %UPSTREAM_CLUSTER_RAW% %UPSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_REMOTE_ADDRESS% %REQUESTED_SERVER_NAME% %ROUTE_NAME%\n
```
```
The following table shows an example using the default access log format for a request sent from curl to httpbin:

```

|Log operator            |access log in curl         |access log in httpbin      |
| -----------------------|---------------------------|---------------------------| 
|[%START_TIME%]          |[2020-11-25T21:26:18.409Z] |[2020-11-25T21:26:18.409Z] |
|\"%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%\" |	"GET /status/418 HTTP/1.1" |	"GET /status/418 HTTP/1.1" |
|%RESPONSE_CODE% |	418	|418|
|%RESPONSE_FLAGS%|	- |	-|
|%RESPONSE_CODE_DETAILS% |	via_upstream |	via_upstream|
|%CONNECTION_TERMINATION_DETAILS%|	- |	-|
|\"%UPSTREAM_TRANSPORT_FAILURE_REASON%\"|	"-"|	"-"|
|%BYTES_RECEIVED%	|0	|0|
|%BYTES_SENT%|	135	|135|
|%DURATION%	|4|	3|
|%RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)%|	4|	1|
|\"%REQ(X-FORWARDED-FOR)%\"	|"-"|	"-"|
|\"%REQ(USER-AGENT)%\"|"curl/7.73.0-DEV"|	"curl/7.73.0-DEV"|
|\"%REQ(X-REQUEST-ID)%\"|	"84961386-6d84-929d-98bd-c5aee93b5c88"|	"84961386-6d84-929d-98bd-c5aee93b5c88"|
|\"%REQ(:AUTHORITY)%\"|	"httpbin:8000"	|"httpbin:8000"|
|\"%UPSTREAM_HOST%\"|	"10.44.1.27:80"	|"127.0.0.1:80"|
|%UPSTREAM_CLUSTER_RAW%	|outbound|8000||httpbin.foo.svc.cluster.local|	inbound|8000||
|%UPSTREAM_LOCAL_ADDRESS%	|10.44.1.23:37652	|127.0.0.1:41854|
|%DOWNSTREAM_LOCAL_ADDRESS%	|10.0.45.184:8000|	10.44.1.27:80|
|%DOWNSTREAM_REMOTE_ADDRESS%	|10.44.1.23:46520	|10.44.1.23:37652|
|%REQUESTED_SERVER_NAME%	|-|	outbound_.8000_._.httpbin.foo.svc.cluster.local
|%ROUTE_NAME%	|default	|default|

### Test the access log

```bash
$ kubectl exec "$SOURCE_POD" -c curl -- curl -sS -v httpbin:8000/status/418
...
< HTTP/1.1 418 Unknown
...
< server: envoy
...
I'm a teapot!
...

# curl’s log:
$ kubectl logs -l app=curl -c istio-proxy
[2020-11-25T21:26:18.409Z] "GET /status/418 HTTP/1.1" 418 - via_upstream - "-" 0 135 4 4 "-" "curl/7.73.0-DEV" "84961386-6d84-929d-98bd-c5aee93b5c88" "httpbin:8000" "10.44.1.27:80" outbound|8000||httpbin.foo.svc.cluster.local 10.44.1.23:37652 10.0.45.184:8000 10.44.1.23:46520 - default

# httpbin’s log:
$ kubectl logs -l app=httpbin -c istio-proxy
[2020-11-25T21:26:18.409Z] "GET /status/418 HTTP/1.1" 418 - via_upstream - "-" 0 135 3 1 "-" "curl/7.73.0-DEV" "84961386-6d84-929d-98bd-c5aee93b5c88" "httpbin:8000" "127.0.0.1:80" inbound|8000|| 127.0.0.1:41854 10.44.1.27:80 10.44.1.23:37652 outbound_.8000_._.httpbin.foo.svc.cluster.local default

```

```
[2026-02-01T16:29:24.710Z] "GET /static/js/main.f7659dbb.js HTTP/1.1"                      200             -                via_upstream            -                                 "-"                                    0                 279879       0         0                                      "10.233.66.16"             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36" "8fcedd10-23a4-9b4d-8caa-ade8a92a66a8" "192.168.1.171:8080"      "10.233.66.32:80"  inbound|80||        127.0.0.6:40305         10.233.66.32:80            10.233.66.16:0              outbound_.80_._.sa-frontend.demo.svc.cluster.local default
"[%START_TIME%]           \"%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%\" %RESPONSE_CODE% %RESPONSE_FLAGS% %RESPONSE_CODE_DETAILS% %CONNECTION_TERMINATION_DETAILS% \"%UPSTREAM_TRANSPORT_FAILURE_REASON%\" %BYTES_RECEIVED% %BYTES_SENT% %DURATION% %RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)% \"%REQ(X-FORWARDED-FOR)%\" \"%REQ(USER-AGENT)%\"                                                                                              \"%REQ(X-REQUEST-ID)%                  \" \"%REQ(:AUTHORITY)%\" \"%UPSTREAM_HOST%\" %UPSTREAM_CLUSTER% %UPSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_REMOTE_ADDRESS% %REQUESTED_SERVER_NAME%                            %ROUTE_NAME%\n"

```
