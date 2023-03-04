#!/bin/bash

echo "Check receive Kerberos credentials"
if ! klist -s
then
    echo "kerberos ticket not valid; please run kinit"
    exit 1
fi
echo""
#################################
# Создание групп

echo ""
echo "Create GROP for password policy"

ipa group-add --desc='pyz password policy' pyz_policy
ipa group-add --desc='adm password policy' adm_policy
ipa group-add --desc='tyz password policy' tyz_policy

echo ""
echo "-------------"

# Создание парольной политики
echo "Create password policy"
echo ""
ipa pwpolicy_add pyz_policy --minlength 12 --maxlife 80 --minlife 72 --history 10 --minclasses 3 --priority 10 --maxfail 5 --failinterval 60 --lockouttime 600
echo ""
ipa pwpolicy_add adm_policy --minlength 25 --maxlife 365 --minlife 72 --history 10 --minclasses 3 --priority 11
echo ""
ipa pwpolicy_add tyz_policy --minlength 25 --minclasses 3 --priority 12 

echo ""
echo "Report password policy"

ipa pwpolicy_find

echo ""
echo "-------------"