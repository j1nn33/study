def run_bash(cmd):
    """Простая функция для выполнения bash команды"""
    try:
        result = subprocess.run(
                cmd,
                shell=True,                # shell=True позволяет использовать пайпы (|), переменные окружения ($VAR) и wildcards (*)
                capture_output=True,
                #stdout=subprocess.PIPE,
                #sdterr=subprocess.PIPE,
                universal_newlines=True,     # Делает вывод output строковым не байтовым
                text=True
                )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        print(f" COMMAND FAILED" )
        return {'stdout': '', 'stderr': str(e), 'returncode': -1}

# Использование:
output = run_bash("ls -la /etc/")
print(output['stdout'])
print(output['stderr'])




result = run_bash(f"ls -la /etc")


print (result)
#print(type(result))
#print (result.keys())


print ('OUT         ', result['stdout'])
print ('ERROR       ', result['stderr'])
print ('RETURN_CODE ', result['returncode'])