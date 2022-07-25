import apiclient.discovery
import httplib2
import requests
import xmltodict
from django.shortcuts import render
from oauth2client.service_account import ServiceAccountCredentials
from .models import Data
from .services import main as TG_bot


def get_google_data():
    '''
    функция получает данные из google-shets
    возвращает: список списков (строк документа) из заданного диапазона
    '''

    # Авторизуемся и получаем доступ к API
    CREDENTIALS_FILE = 'exchange_app/creds.json'
    spreadsheet_id = '1-fh9NMsarGBp0ILsNFqhpdTBL_Nzlmaub13kdiZU2bI'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Читаем файл
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A2:D52', # TODO: получать диап. заполненных ячеек динамически
        majorDimension='ROWS'
    ).execute()

    # запускаем бота проверки даты поставки
    TG_bot(values['values'])

    return (values['values'])


def get_course():
    '''
    функция получает курс доллара с сайта ЦБ РФ на текущую дату
    возвращает: число(float) - курс доллара к рублю
    '''
    # запрос на сайт ЦБ РФ
    response = requests.get(
        url='http://www.cbr.ru/scripts/XML_daily.asp').text
    valutes = xmltodict.parse(response).get('ValCurs').get('Valute')

    # из ответа сайт ЦБ РФ находим "доллар США" по его ID
    for val in valutes:
        if val['@ID'] == 'R01235':
            return float(val['Value'].replace(',', '.'))

    return 'на сегодня курс неизвестен'


def index(request):
    data = get_google_data()        # получаем данные из таблицы
    course = get_course()           # получаем курс доллара
    Data.objects.all().delete()     # удаляем старые данные из базы
    total = 0

    # добавляем новые данные в базу
    for item in data:
        total = total + float(item[2])
        Data.objects.create(
            serial_numb=item[0],
            order_numb=item[1],
            price_usd=item[2],
            price_rub=float(item[2]) * course,
            delivery_date=item[3],
        )

    data = Data.objects.all()

    # формируем набор данных
    context = {
        'course': course,
        'data': data,
        'total': total,
    }

    # возвращаем рендер страницы, используя шаблон index.html
    return render(
        request=request,
        template_name='exchange_app/index.html',
        context=context
    )
