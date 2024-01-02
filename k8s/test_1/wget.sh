#!/bin/sh
cat <<EOF >/app/index.html
<html>
<head/>
<body>
<h1 style="color: #5e9ca0;"><span style="color: #000080;">TEST PAGE FOR WEB SERVER IN K8</span></h1>
<p>&nbsp;</p>
<!-- IMAGE BEGINS HERE -->
<font size="-3">
<pre><font>
<!-- IMAGE ENDS HERE -->
</pre></font>
<!-- IMAGE ENDS HERE -->
<!-- TEST PHRASE -->
EOF

INFO_ENV=$(export)
INFO_MOUNTS=$(mount)
INFO_RAM=$(free -m)
INFO_RESOLV=$(cat /etc/resolv.conf)
INFO_HOSTS=$(cat /etc/hosts)

cat <<EOF >> /app/index.html
<h3>Mountpoints</h3>
<pre>$INFO_MOUNTS</pre>
<h3>Environment</h3>
<pre>$INFO_ENV</pre>
<h3>Memory info</h3>
<pre>$INFO_RAM</pre>
<h3>DNS resolvers info</h3>
<pre>$INFO_RESOLV</pre>
<h3>Static hosts info</h3>
<pre>$INFO_HOSTS</pre>
</body>
</html>
EOF
