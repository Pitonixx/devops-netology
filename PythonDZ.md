# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательные задания

1. Есть скрипт:
	```python
    #!/usr/bin/env python3
	a = 1
	b = '2'
	c = a + b
	```
	* Какое значение будет присвоено переменной c?
	* Как получить для переменной c значение 12?
	* Как получить для переменной c значение 3?
	
	У переменной c будет ошибка вывода, т.к. мы пытаемся сложить строку с числом.
	Чтобы получилось число 12, нужно либо а объявить строкой, либо b обявить числом 11
	Чтобы получить 3, надо у b убрать кавычки.
	
	

1. Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

	```python
    #!/usr/bin/env python3

    import os

	bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
	result_os = os.popen(' && '.join(bash_command)).read()
    is_change = False
	for result in result_os.split('\n'):
        if result.find('modified') != -1:
            prepare_result = result.replace('\tmodified:   ', '')
            print(prepare_result)
            break

	```

По-поводу пути можно ~ поменять на папку, в которой лежат файлы - т.е. /home/USERNAME/netology/sysadm-homeworks	

Про не все показывает - после запуска :) выяснил, что break - лишнее, без него показывает все изменения и штатно выходит.

	```python
    #!/usr/bin/env python3

	import os

	bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
	result_os = os.popen(' && '.join(bash_command)).read()
	is_change = False
	print(result_os)
	for result in result_os.split('\n'):
   	 if result.find('modified') != -1:
       		 prepare_result = result.replace('\tmodified:   ', '')
       		 print(prepare_result)
	pathtodir = ["pwd"]
	resultpath = os.popen(' && '.join(pathtodir)).read()
	print(resultpath) #печатаем путь, где репозиторий


	```
	
	
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

```python
#!/usr/bin/env python3
from sys import argv
import os

bash_command = ["cd ",argv[1], "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
print(result_os)

if os.path.isdir(argv[1]+'.git') == true: #проверяем, является-ли директория репозиторием
	for result in result_os.split('\n'):
		if result.find('modified') != -1:
		prepare_result = result.replace('\tmodified:   ', '')
		print(prepare_result)
else:
	print('Dir not repo')
pathtodir = ["pwd"]
resultpath = os.popen(' && '.join(pathtodir)).read()
print(resultpath) #печатаем путь, где репозиторий
```

Добавил получение пути по argv


1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.

```python
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

Запрос к такому скрипту будет выглядеть так: 
```
python3 domname.py drive.google.com google.com mail.google.com
```
