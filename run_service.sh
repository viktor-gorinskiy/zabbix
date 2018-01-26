#/bin/bash

if [ -z "$(echo -n $@)" ]
then exit 0
fi

printf "{\"data\":["

for service in $@
do
        if pgrep $service > /dev/null 2>&1
        then printf $var"{\"{#SERVICE}\":\"$service\"}"
        fi
var=","
done

printf "]}"

exit 0

