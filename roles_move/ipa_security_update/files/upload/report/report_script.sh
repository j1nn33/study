#!/bin/bash
# список файлов находится в каталоге со скриптом
list_file=./list_file.txt
echo "Check receive Kerberos credentials"

if ! klist -s
then
    echo "kerberos ticket not valid; please run kinit"
    exit 1
fi

echo""
#################################
# Получение отчета по настройкам
echo "LDAP - report"
echo "-------------"

grep -e nsslapd-securePort \
     -e nsslapd-security \
     -e sslVersionMin \
     -e sslVersionMax \
     -e nsslapd-auditlog-logging-enabled \
     -e nsslapd-errorlog-logging-enabled \
     -e nsslapd-auditfaillog-logging-enabled \
     -e nsslapd-accesslog-level \
     -e nsslapd-errorlog-level \
     -e nsslapd-auditlog \
     -e nsslapd-accesslog \
     -e nsslapd-errorlog \
     -e nsslapd-allow-anonymous-access \
/etc/dirsrv/slapd-*/dse.ldif

echo ""
echo "-------------"
#################################
echo ""
echo "krb5kdc - report"

grep -e default_ccache_name \
     -e permitted_enctypes \
     -e permitted_enctypes \
     -e master_key_type \
     -e restrict_anonymous_to_tgt \
     -e requires_pre_auth \
/etc/krb5.conf

echo ""
echo "-------------"
#################################
echo ""
echo "bind - report"

grep -e allow-transfer \
     -e allow-update \
/etc/named.conf

echo ""
echo "-------------"
#################################
echo ""
echo "FILES - report"

for files in $(cat $list_file)
do 
ls -la $files
done

echo ""
echo "-------------"
#################################
echo ""
echo "Report AUDITD check file /etc/audit/rules.d/krb5kdc.rules"

cat cat /etc/audit/rules.d/krb5kdc.rules

echo ""
echo "-------------"
#################################
echo ""
echo "Report RSYSLOG check file /etc/audit/rules.d/krb5kdc.rules"

cat /etc/rsyslog.d/ipa.conf

echo ""
echo "-------------"
#################################
echo ""
echo "Report password policy"

ipa pwpolicy_find

echo ""
echo "-------------"
#################################

