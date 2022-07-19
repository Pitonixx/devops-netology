# Домашнее задание к занятию "14.5 SecurityContext, NetworkPolicies"

## Задача 1: Рассмотрите пример 14.5/example-security-context.yml

Создайте модуль

```
kubectl apply -f 14.5/example-security-context.yml
```

![1](1.PNG)

Проверьте установленные настройки внутри контейнера

```
kubectl logs security-context-demo
uid=1000 gid=3000 groups=3000
```

![2](2.PNG)

## Задача 2 (*): Рассмотрите пример 14.5/example-network-policy.yml

Создайте два модуля. Для первого модуля разрешите доступ к внешнему миру
и ко второму контейнеру. Для второго модуля разрешите связь только с
первым контейнером. Проверьте корректность настроек.

Сделано два пода - mypod и nwtool, и [NetworkPolicy](example-network-policy.yml) для каждого:

![4](4.PNG)

Для пода nwtool теперь доступен mypod и внешний мир:

![5](5.PNG)

А для пода mypod доступен nwtool:

![6](6.PNG)
---
