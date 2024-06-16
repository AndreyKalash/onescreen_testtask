# Тестовое задание

## Задание 1.

Необходимо прочитать, изучить и распарсить файл `data_json.json`. Результирующий датафрейм должен состоять из 30 строк и столбцами:

`operation_id`
`operation_date`
`posting_number`
`sku`
`article`
`type_operation`
`delivery_schema`
`name` (берется из блока `services`)
`price` (берется из блока `services`)
`count_item` (кол-во словарей в блоке items относительно уникального `operation_id`)
`total_price` (`price`/ `item`)
`quantity` (кол-во уникальных `sku` в уникальном `operation_id`)
Вводные по задаче:

Файл `data_json` – это реальный api ответ от маркетплейса, стоит задача разложить вложенные структуры словарей и списков на датафрейм, в котором `operation_id` это уникальный id операции относительно него раскрываются все структуры словарей.

Результат выполнения: `tasks\task1.py`
## Задание 2.

Написать python скрипт, который будет подключаться к списку БД, таблице `accrual_report` и удалять дубликаты строк. Значения в столбце `id_o` должны быть уникальными. SQL запрос должен быть написан для MS SQL и PostgreSQL.


Результат выполнения: `tasks\task2.py`

## Задание 3.

Написать python скрипт, который будет подключаться к списку БД, таблице `rating` и заменять данные в столбце sku. SQL запрос должен быть написан для MS SQL и PostgreSQL.

Вводные по задаче: нужно импортировать файл `df.csv` и заменить в таблице БД `rating` в столбце `sku`, значения `sku_old`, на `sku_new`.
Результат выполнения: `tasks\task3.py`

## Задание 4.

Написать консольное python приложение и конвертировать его в exe формат.

Вводные по задаче: написать простое консольное приложение, которое будет выводить меню с возможностью перемещения с клавиатуры. Меню будет состоять из пунктов:
```
MS
PG
```
При выборе пункта MS выводится под меню:
```
Загрузить данные
Удалить данные
```
При выборе 1 пункта выводится текст «Данные загружены», для 2 пункта «Удалил данные».

При выборе в главном меню `PG`, подменю и вывод текста будет такой же, как и для `MS`.

Результат выполнения: `tasks\task4.py`. Для конвертации py файла в exe использовался модуль `pyinstaller`. Для создания exe файла, необходимо выполнить следующую команду:
```
pyinstaller --onefile .\tasks\task4.py
```