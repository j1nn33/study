#!/bin/bash
# что бекапим
SLAPD_DIR=/etc/openldap/slapd.d
#  куда бекапим
BACKUP_ROOT=/var/backup/ldap 
DATE=$(date +%Y%m%d_%H%M%S)
# RETENTION - сколько хранить
RETENTION=14
# set +e если в скрипте ошибка то он просто вываливается (если неопределны какие-либо переменные)
set +e

exec 3>&1 
exec 4>&2 

#exec 1> >(logger -t $0)  перенаправление в /var/log/message
#exec 2>&1

print (){
	echo $* >&3
}

err (){
	echo $* >&4
}

# проверка на существоание каталогов если их нет то создаем
pre_checks(){
	[[ $(id -u) -eq 0 ]] || { err "only root can run this!"; exit 1; }
	[[ -d ${BACKUP_ROOT} ]] || mkdir -p ${BACKUP_ROOT}
	BK_DIR=${BACKUP_ROOT}/${DATE}
	[[ -d ${BK_DIR} ]] || mkdir ${BK_DIR}
}

export_ldif(){
	[[ -z $1 ]] || base="-b ${1}"
	/usr/sbin/slapcat -F ${SLAPD_DIR} ${base}
	return $?
}

backup_db (){
	CTX=database
	[[ -z $1 ]] || CTX=${1}
	BK_FILE=${BK_DIR}/${CTX}
	[[ -s $BK_FILE ]] && { err "$BK_FILE EXITST. Refusing to overwrite"; exit 1; }
	export_ldif "${1}" > ${BK_FILE}.ldif
}

backup_files (){
	tar cf ${BK_DIR}/files.tar /etc/openldap/certs 
}

cleanup (){
	find ${BK_ROOT} -mindepth 1 -maxdepth 1 -type d -mtime +${RETENTION} -exec rm -rt {} \;
}

# ТЕЛО СКРИПТА   
pre_checks

for db in cn=config dc=otus,dc=lnx; do 
	backup_db ${db}
done

backup_files

cleanup