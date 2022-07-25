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

# В тестовом режимен проект работает с БД SQLite

# для подключения БД PostgeSQL 
NAME = 'your-project-name'
USER = 'your-projectuser-user'
PASSWORD = 'your-password'
так же нужно будет отдельно настроить PostgreQQL (не описано)
```

* Для работы с google-shets необходимо будет получить токен авторизации 
в виде .json файла. Документация доступна по ссылке: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values
  - данный файл необходимо переименовать в creds.json и поместить в папку app/exchange_app

* Соберите docker образ:
```
sudo docker build -t te-kan .
```
* Запустите docker образ:
```
docker run -it -p 5000:5000 te-kan
```
* После успешного запуска выполните команды (только после первого деплоя):
    - Примените миграции:
    ```
    sudo docker-compose exec te-kan python manage.py migrate --noinput
    ```
    - Создать суперпользователя Django:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
    - Проект будет доступен по локально по адресу: 127.0.0.1:5000

автор: https://github.com/bobrolevv/