import requests
import json
import sys

if __name__ == '__main__':
    try:
        HOST_NAME = sys.argv[1]
        TRIGGER_NAME = sys.argv[2]
    except IndexError:
        pass

TEMPLATE_NAME = "Template_" + TRIGGER_NAME.partition('trigger_detected_and_run_')[2]


# Авторизация: получаем ключ пользователя (auth)
url = 'http://127.0.0.1/api_jsonrpc.php'
headers = {'content-type': 'application/json-rpc'}
user_login_payload = json.dumps({
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "user_name",
        "password": "secret_password"
    },
    "id": 1,
#    "auth": null
})
user_login_data = json.loads(requests.post(url, user_login_payload, headers=headers).text)

# Проверка на ошибку авторизации и повторная авторизация
while "error" in user_login_data:
    print ("Была обнаружена ошибка авторизации")
    user_login_data = json.loads(requests.post(url, user_login_payload, headers=headers).text)

# Пишем строчку ответа запроса авторизации:
print ("user_login_data ==> ", user_login_data)

# Присваиваем пременной auth значение поля auth из ответа авторизации
auth = user_login_data['result']

# Пишем auth
print ("auth ==> ", auth)

# Делаем запрос для получения hostid клиента и списка шаблонов, фильтруем по имени хоста
host_get_payload = json.dumps({
     "jsonrpc": "2.0",
     "method": "host.get",
     "params": {
         "output": ["hostid"],
         "selectParentTemplates": [
             "templateid",
 #            "name"
         ],
         "filter": {
             "host": [
                 "test-debian"
             ]
         }
     },
     "auth": auth,
     "id": 1
 })

host_get_data = json.loads(requests.post(url, host_get_payload, headers=headers).text)

# Список текущих шаблонов клиента
parentTemplates = host_get_data['result'][0]['parentTemplates']

hostid = host_get_data['result'][0]['hostid']

print ("hostid ==>", hostid)
print ("parentTemplates ==>", parentTemplates)


# Получаем активный тригер фильрую тригеры по хочту и имени тригера
trigger_get_payload = json.dumps({
    "jsonrpc": "2.0",
    "method": "trigger.get",
    "params": {
        "output": [
            "triggerid",
            "description"
        ],
        "filter": {
            "description": TRIGGER_NAME,
            "hostid": hostid,
            #"active": "0",
            #"value": 1
        }
    },
    "id": 1,
    "auth": auth
})

trigger_get_data = json.loads(requests.post(url, trigger_get_payload, headers=headers).text)
print ("trigger_get_data ==>", trigger_get_data)
triggerid = trigger_get_data['result'][0]['triggerid']
print ("triggerid ==>", triggerid)

# Отключаем тригер на клиенте
trigger_update_payload = json.dumps({
    "jsonrpc": "2.0",
    "method": "trigger.update",
    "params": {
        "triggerid": triggerid,
        "status": "1"
    },
    "auth": auth,
    "id": 1
})

trigger_update_data = json.loads(requests.post(url, trigger_update_payload, headers=headers).text)
print ("trigger_update_data ==>", trigger_update_data)


# Ищем по имени шаблона его templateid для последуещего навешивания его хосту
template_get_payload  = json.dumps({
    "jsonrpc": "2.0",
    "method": "template.get",
    "params": {
        "output": "extend",
        "filter": {
            "host": [
                TEMPLATE_NAME
            ]
        }
    },
    "auth": auth,
    "id": 1
})

template_get_data = json.loads(requests.post(url, template_get_payload, headers=headers).text)
templateid = template_get_data['result'][0]['templateid']
print ("templateid ==>", templateid)

# Создаем новый список шаблонов добавив туда найденный по имени шаблон
templateid_dict = {
    'templateid': templateid
}

# Обновляем список шаблонов на клиенте
parentTemplates.append(templateid_dict)
print ("parentTemplates", parentTemplates)


host_template_update_payload  = json.dumps({
    "jsonrpc": "2.0",
    "method": "host.update",
    "params": {
        "hostid": hostid,
        "templates": parentTemplates
    },
    "auth": auth,
    "id": 1
})

host_template_update_data = json.loads(requests.post(url, host_template_update_payload, headers=headers).text)
print ("host_template_update_data ==>", host_template_update_data)
