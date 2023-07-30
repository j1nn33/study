Структрута jenkins job  

jenkins     
	|_____<job_name.groovie>	// имя джобы 
playbook
	|_____role1.yml      		// базоый файл выхова роли и описание такски
	|_____role2.yml
	|_____secret.yml            // ansible-vault encrypt
          user: user
          password: pass
	|_____precheck.yml
	|_____postcheck.yml
	
roles
	|_____role1					// содержание роли 
	|_____role2
	|_____precheck
	|_____postcheck

	
ansible.cfg


--------------------------------------
create role 
cd ./Jenkins/jenkins_structure/roles/

ansible-galaxy init <role_name>

ansible-galaxy init role_1
ansible-galaxy init role_2
ansible-galaxy init post_action
ansible-galaxy init precheck