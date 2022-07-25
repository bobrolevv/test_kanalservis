# Проект test_kanservis
  
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

Задача: Необходимо разработать скрипт на языке Python 3,
который будет выполнять следующие функции:
1. Получать данные с документа при помощи Google API, сделанного в [Google Sheets](https://docs.google.com/spreadsheets/d/1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g/edit) (необходимо копировать в свой Google аккаунт и выдать самому себе права).
2. Данные должны добавляться в БД, в том же виде, что и в файле –источнике, с добавлением колонки «стоимость в руб.»
    a. Необходимо создать DB самостоятельно, СУБД на основе PostgreSQL.
    b. Данные для перевода $ в рубли необходимо получать по курсу [ЦБ РФ](https://www.cbr.ru/development/SXML/).
3. Скрипт работает постоянно для обеспечения обновления данных в онлайн режиме (необходимо учитывать, что строки в Google Sheets таблицу могут удаляться, добавляться и изменяться).
Дополнения, которые дадут дополнительные баллы и поднимут потенциальный уровень оплаты труда:
1. a. Упаковка решения в docker контейнер
    b. Разработка функционала проверки соблюдения «срока поставки» из таблицы. В случае, если срок прошел, скрипт отправляет уведомление в Telegram.
    c. Разработка одностраничного web-приложения на основе Django или Flask. Front-end React.
     
## Подготовка и запуск проекта
### Склонировать репозиторий на локальную машину (ubuntu):
```
git clone https://github.com/bobrolevv/test_kanservis
```

* Установите docker:
```
sudo apt install docker.io 
```

* В папке exchange_app создайте .env файл и впишите:
```
TELEGRAM_TOKEN = 'your-tlg-token'
TELEGRAM_CHAT_ID = 'your-chat-id'

NAME = 'your-project-name'
USER = 'your-projectuser-user'
PASSWORD = 'your-password'
```
  
* Соберите docker образ:
```
sudo docker build -t te-kan .

```
* После успешной сборки на сервере выполните команды (только после первого деплоя):
    - Соберите статические файлы:
    ```
    sudo docker-compose exec backend python manage.py collectstatic --noinput
    ```
    - Примените миграции:
    ```
    sudo docker-compose exec backend python manage.py migrate --noinput
    ```
    - Загрузите ингридиенты  в базу данных (необязательно):  
    
    ```
    sudo docker-compose exec backend python manage.py load_data 
    ```
    - Создать суперпользователя Django:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
    - Проект будет доступен по вашему IP

автор: https://github.com/bobrolevv/