#!/bin/bash
# скрипт обновления политики LDAP

#!/bin/bash
# скрипт обновления политики LDAP

# Задание REALM
REALM=IPA-LAN


ldapmodify -D "cn=directory manager" -W << EOF
dn: cn=config
changetype: modify
replace: nsslapd-securePort
nsslapd-securePort: 636
-
replace: nsslapd-security
nsslapd-security: on
-
replace: nsslapd-auditlog-logging-enabled
nsslapd-auditlog-logging-enabled: on
-
replace: nsslapd-errorlog-logging-enabled
nsslapd-errorlog-logging-enabled: on
-
replace: nsslapd-accesslog-logging-enabled
nsslapd-accesslog-logging-enabled: on
-
replace: nsslapd-auditfaillog-logging-enabled
nsslapd-auditfaillog-logging-enabled: on
-
replace: nsslapd-accesslog-level
nsslapd-accesslog-level: 256
-
replace: nsslapd-errorlog-level
nsslapd-errorlog-level: 16384
-
replace: nsslapd-auditlog
nsslapd-auditlog: /var/log/dirsrv/slapd-$REALM/audit
-
replace: nsslapd-accesslog
nsslapd-accesslog: /var/log/dirsrv/slapd-$REALM/access
-
replace: nsslapd-errorlog
nsslapd-errorlog: /var/log/dirsrv/slapd-$REALM/errors
-
replace: nsslapd-allow-anonymous-access
nsslapd-allow-anonymous-access: rootdse
-
EOF
