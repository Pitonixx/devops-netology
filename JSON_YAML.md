# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

## Обязательные задания

1. Мы выгрузили JSON, который получили через API запрос к нашему сервису:
	```json
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175
            },
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
	```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

	```json
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "port" : 7175
            },
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
	```
	Нашел 3 шт - в первом элементе в пункте IP приехал порт, а во-втором были не закрыты скобки в ip, сам ip-адрес должен быть в кавычках, т.к. не число.


2. В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

``` python
from sys import argv
import sys,socket

output=[]
domain_name=argv
y = len(domain_name)

for n in range(1,y): #добавил получение любого количества аргументов
	a = domain_name[n]
	ip = socket.gethostbyname(a)
	output.insert(n,ip)

for x in output:
        print(" __ "+x+"__")


while y > 1: #цикл теперь бесконечный
	for n in range(1,y):
		ip = socket.gethostbyname(domain_name[n])
		print(domain_name[n]+" "+ip)
		test = output[n-1]
		if test != ip:
			print("[ERROR] "+domain_name[n]+" IP mismatch: "+output[n]+" "+ip)
		output.insert(n,ip)
```

По данному заданию я приложил отдельный файл по адресу
https://github.com/Pitonixx/devops-netology/blob/main/json-yaml/domname.py



## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
