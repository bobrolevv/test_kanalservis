import apiclient.discovery
import httplib2
import requests
import xmltodict
from django.shortcuts import render
from oauth2client.service_account import ServiceAccountCredentials
from .models import Data


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
        range='A2:D52',
        majorDimension='ROWS'
    ).execute()
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
    for val in valutes:
        if val['@ID'] == 'R01235':
            return float(val['Value'].replace(',', '.'))

    return 'на сегодня курс неизвестен'


def exhange(request):
    data = get_google_data()
    course = get_course()
    Data.objects.all().delete()

    for item in data:
        Data.objects.create(
            serial_numb=item[0],
            order_numb=item[1],
            price_usd=item[2],
            price_rub=float(item[2]) * course,
            delivery_date=item[3],
        )

    data = Data.objects.all()

    name = 'mr. And'
    context = {
        'course': course,
        'data': data
    }

    return render(
        request=request,
        template_name='exchange_app/index.html',
        context=context
    )
