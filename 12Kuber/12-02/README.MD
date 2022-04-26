### Домашнее задание к занятию "12.2 Команды для работы с Kubernetes"
Кластер — это сложная система, с которой крайне редко работает один человек. Квалифицированный devops умеет наладить работу всей команды, занимающейся каким-либо сервисом.
После знакомства с кластером вас попросили выдать доступ нескольким разработчикам. Помимо этого требуется служебный аккаунт для просмотра логов.

#### Задание 1: Запуск пода из образа в деплойменте
Для начала следует разобраться с прямым запуском приложений из консоли. Такой подход поможет быстро развернуть инструменты отладки в кластере. Требуется запустить деплоймент на основе образа из hello world уже через deployment. Сразу стоит запустить 2 копии приложения (replicas=2).

Требования:
 * пример из hello world запущен в качестве deployment
 * количество реплик в deployment установлено в 2
 * наличие deployment можно проверить командой kubectl get deployment
 * наличие подов можно проверить командой kubectl get pods


```
PS C:\Users\Admin> kubectl create deployment hello-node --image=k8s.gcr.io/echoserver:1.4
deployment.apps/hello-node created
PS C:\Users\Admin> kubectl scale --replicas=2 deployment/hello-node
deployment.apps/hello-node scaled
PS C:\Users\Admin> kubectl get deployment
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
hello-node   0/2     2            0           16s
PS C:\Users\Admin> kubectl get deployment
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
hello-node   2/2     2            2           36s
```

#### Задание 2: Просмотр логов для разработки
Разработчикам крайне важно получать обратную связь от штатно работающего приложения и, еще важнее, об ошибках в его работе.
Требуется создать пользователя и выдать ему доступ на чтение конфигурации и логов подов в app-namespace.

Требования:
 * создан новый токен доступа для пользователя
 * пользователь прописан в локальный конфиг (~/.kube/config, блок users)
 * пользователь может просматривать логи подов и их конфигурацию (kubectl logs pod <pod_id>, kubectl describe pod <pod_id>)

```
# создание пользователя
PS C:\Users\Admin> kubectl create serviceaccount dev1
serviceaccount/dev1 created

# Написан yaml файл для создания роли:

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "watch", "list"]

# создать роль
PS E:\Users\Admin\Documents\DevOps\12-02> kubectl create -f role.yml
role.rbac.authorization.k8s.io/pod-reader created

# привязываем роль к пользователю
PS E:\Users\Admin\Documents\DevOps\12-02> kubectl create rolebinding pod-reader-bind --role=pod-reader --serviceaccount=default:dev1 --namespace=default
rolebinding.rbac.authorization.k8s.io/pod-reader-bind created

# Создан yaml файл для создания токена:

apiVersion: v1
kind: Secret
metadata:
  name: dev1-secret
  annotations:
    kubernetes.io/service-account.name: dev1-secret
 type: kubernetes.io/service-account-token

# создание токена
PS E:\Users\Admin\Documents\DevOps\12-02> kubectl create -f secret.yml
secret/dev1-secret created
```
После команды get secrets токен не нашелся...
```
PS E:\Users\Admin\Documents\DevOps\12-02> kubectl get secrets
NAME                  TYPE                                  DATA   AGE
default-token-pnb4g   kubernetes.io/service-account-token   3      3d21h
dev1-token-kgftm      kubernetes.io/service-account-token   3      3d21h
```
но обнаружил, что для пользователя dev1 появился токен dev1-token-kgftm. Похоже, он создался автоматически при создании serviceaccount и его удалось использовать далее
```
# добавляем пользователя dev1 в локальный конфиг
PS E:\Users\Admin\Documents\DevOps\12-02> kubectl config set-credentials dev1 --token eyJhbGciOiJSUzI1NiIs.........

User "dev1" set.

# переключаемся на нового пользователя и пробуем удалить pod
PS E:\Users\Admin\Documents\DevOps\12-02> kubectl config set-context minikube --user dev1
Context "minikube" modified.
PS E:\Users\Admin\Documents\DevOps\12-02> kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
hello-node-6b89d599b9-6mmpl   1/1     Running   0          3d21h
hello-node-6b89d599b9-ztxhw   1/1     Running   0          3d21h

PS E:\Users\Admin\Documents\DevOps\12-02> kubectl delete pods/hello-node-6b89d599b9-ztxhw
Error from server (Forbidden): pods "hello-node-6b89d599b9-ztxhw" is forbidden: User "system:serviceaccount:default:dev1" cannot delete resource "pods" in API group "" in the namespace "default"

# пробуем посмотреть информацию о поде
PS E:\Users\Admin\Documents\DevOps\12-02> kubectl describe pods/hello-node-6b89d599b9-ztxhw
Name:         hello-node-6b89d599b9-ztxhw
Namespace:    default
Priority:     0
Node:         minikube/192.168.49.2
Start Time:   Fri, 22 Apr 2022 14:18:24 +0300
Labels:       app=hello-node
              pod-template-hash=6b89d599b9
Annotations:  <none>
Status:       Running
IP:           172.17.0.5

# смотрим логи
PS E:\Users\Admin\Documents\DevOps\12-02> kubectl logs -p  pods/hello-node-6b89d599b9-ztxhw
Error from server (BadRequest): previous terminated container "echoserver" in pod "hello-node-6b89d599b9-ztxhw" not found
.....

```
#### Задание 3: Изменение количества реплик
Поработав с приложением, вы получили запрос на увеличение количества реплик приложения для нагрузки. Необходимо изменить запущенный deployment, увеличив количество реплик до 5. Посмотрите статус запущенных подов после увеличения реплик.

Требования:
 * в deployment из задания 1 изменено количество реплик на 5
 * проверить что все поды перешли в статус running (kubectl get pods)

 ```
PS C:\Users\Admin> kubectl scale --replicas=5 deployment/hello-node
deployment.apps/hello-node scaled
PS C:\Users\Admin> kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
hello-node-6b89d599b9-24gxx   1/1     Running   0          6m22s
hello-node-6b89d599b9-6mmpl   1/1     Running   0          4d3h
hello-node-6b89d599b9-jvsbb   1/1     Running   0          6m22s
hello-node-6b89d599b9-mh9t8   1/1     Running   0          6m22s
hello-node-6b89d599b9-ztxhw   1/1     Running   0          4d3h
 ```
