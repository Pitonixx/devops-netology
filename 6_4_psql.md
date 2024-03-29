### Домашнее задание к занятию "6.4. PostgreSQL"
>#### Задача 1
>
>Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.
>
>Подключитесь к БД PostgreSQL используя `psql`.
>
>Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.
>
>**Найдите и приведите** управляющие команды для:
- вывода списка БД -  \l
- подключения к БД - \c [имя базы]
- вывода списка таблиц - \dt
- вывода описания содержимого таблиц - \d [имя таблицы]
- выхода из psql - \q

>#### Задача 2
>
>Используя `psql` создайте БД `test_database`.
>
>Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).
>
>Восстановите бэкап БД в `test_database`.
>
>Перейдите в управляющую консоль `psql` внутри контейнера.
>
>Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.
>
>Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders`
>с наибольшим средним значением размера элементов в байтах.
>
>**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

```mysql-psql
test_database=# ANALYZE orders;
ANALYZE
test_database=# SELECT avg_width, attname FROM pg_stats WHERE tablename ='orders';
 avg_width | attname
-----------+---------
         4 | id
        16 | title
         4 | price
```

Столбец с наибольшим средним значением размера элементов - "title"

>#### Задача 3
>
>Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
>поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
>провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).
>
>Предложите SQL-транзакцию для проведения данной операции.
>
>Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

```mysql-psql
CREATE TABLE orders2 (LIKE orders INCLUDING ALL);

INSERT INTO orders2 SELECT * FROM orders;

TRUNCATE orders;

CREATE TABLE orders_1 (CHECK (price<=499)) INHERITS (orders);
CREATE TABLE orders_2 (CHECK (price>499)) INHERITS (orders);

CREATE RULE insert_to_orders1 AS ON INSERT TO orders WHERE ( price <= 499) DO INSTEAD INSERT INTO orders_1 VALUES (NEW.*);
CREATE RULE insert_to_orders2 AS ON INSERT TO orders WHERE ( price > 499) DO INSTEAD INSERT INTO orders_2 VALUES (NEW.*);

INSERT INTO orders SELECT * FROM orders2;
```
С помощью этих команд произвели шардинг с наследованием.

На стадии проектирования БД можно было сделать те же правила, тогда не понадобилось бы ручное вмешательство.

>#### Задача 4
>
>Используя утилиту `pg_dump` создайте бекап БД `test_database`
```mysql-psql
pg_dump -U postgres test_database > /var/tmp/test_database.dump
```
>Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

В файле дампа нужно добавить к данному столбцу ключевое слово UNIQUE.
```mysql-psql
CREATE TABLE public.orders (
    id integer NOT NULL,
    title character varying(80) UNIQUE NOT NULL,
    price integer DEFAULT 0
);
```
