 ### TOML vs YAML 

<table>
<tr>
<td valign="top">
<pre>
title = "TOML Example"
&nbsp;
[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00
&nbsp;
[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true
&nbsp;
[servers]
&nbsp;
  [servers.alpha]
  ip = "10.0.0.1"
  dc = "eqdc10"
  &nbsp;
  [servers.beta]
  ip = "10.0.0.2"
  dc = "eqdc10"
  &nbsp;
[clients]
data = [ ["gamma", "delta"], [1, 2] ]
&nbsp;
hosts = [
  "alpha",
  "omega"
]
</pre>
</td>
<td valign="top">
<pre>
title: YAML Example
&nbsp;
owner:
  name: Tom Preston-Werner
  dob: 1979-05-27T07:32:00-08:00
&nbsp;
database:
  server: 192.168.1.1
  ports: [ 8001, 8001, 8002 ]
  connection_max: 5000
  enabled: true
&nbsp;
servers:
&nbsp;
  alpha:
    ip: 10.0.0.1
    dc: eqdc10
  &nbsp;
  beta:
    ip: 10.0.0.2
    dc: eqdc10
&nbsp;
clients:
  data: [ [gamma, delta], [1, 2] ]
  &nbsp;
  hosts:
    - alpha
    - omega
</pre>
</td>
</tr>
</table>