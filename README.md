# zabbix
Мои наработки для zabbix:

1. Iostat-Disk-Utilization-Template_time.xml ==> 
Шаблон для утилизации дисков с гипким заданием параметров нагрузки и отключением тригеров по расписанию
_________________________________________________________________________________

2. autodiscovery/Template_Template service auto discovery ==> 
Шаблон для автообнаружения сервисов
_________________________________________________________________________________

3. autodiscovery/Template Check various services.xml ==> 
Шаблон для автообнаружения сервисов systemctl
_________________________________________________________________________________

4. autodiscovery/run_service.sh ==> 
Bash скрипт который необходимо положить в папку со скриптами на клиенте в шаблоне прописан такой путь: /etc/zabbix/scripts/run_service.sh
_________________________________________________________________________________

5. autodiscovery/auto-discovery.py ==>
Python скрипт который необходимо положить в папку со скриптами на сервере Zabbix
В действии прописан вот такой путь:
/usr/bin/python3 /lib/zabbix/externalscripts/api/auto-discovery.py {HOST.NAME} {TRIGGER.NAME}
