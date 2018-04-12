#/bin/bash
# Автообнаружение сервисов для заббикс-агента
# Скрипт получает от Zabbix сервера список сервисов и программ которые необходимо замониторить и
# возвращает JSON со списком обнаруженых сервисовю и программ если их обнаржил.
#
# В первой части происходит поиск  в списке макросов сервиса со знаком "*", который подразумеват множетво сервисов попадающих под общий шаблон.
#
# Прекращаем работу скрипта, если ему ничего не передано.
if [ -z "$(echo -n $@)" ]
then exit 0
fi

vars=$@

#########################################################################################
# Часть 1. Запускаем цикл для поиска в списке мохнатой точки:

        for service in $vars
        do
                if $(echo $service|grep -q "*") # Если найдена точка, то запрашиваем у systemctl список севисов
                then
                sys_services=$(systemctl status $service 2>/dev/null| grep ● |tr -d '● ')
                vars=$(echo -n $vars $sys_services)     # И дополняем оригинальный список новым списом сервисов
                fi
         vars=$(for variable in $vars;do echo $variable| grep -v "\*" ;done)    # Удаляем из нового списка сервис о звездочкой
        done
#echo "Новый список сервисов:" $vars

#########################################################################################
# Часть 2. Формируем json ответ.
printf "{\"data\":["

for service in $vars
do

        if pgrep $service > /dev/null 2>&1
        then printf $var"{\"{#SERVICE}\":\"$service\"}"
        else

                if ( systemctl is-active --quiet $service 2>/dev/null ) || ( systemctl is-enabled --quiet $service 2>/dev/null )
                then printf $var"{\"{#SERVICE}\":\"$service\"}"
                fi

        fi
var=","
done

printf "]}"

exit 0

