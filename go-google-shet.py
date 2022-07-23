# docs: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values
from pprint import pprint

import apiclient.discovery
import httplib2
import requests
import xmltodict
from oauth2client.service_account import ServiceAccountCredentials


def get_gogle():
    # Файл, полученный в Google Developer Console
    CREDENTIALS_FILE = 'creds.json'
    # ID Google Sheets документа (можно взять из его URL)
    spreadsheet_id = '1-fh9NMsarGBp0ILsNFqhpdTBL_Nzlmaub13kdiZU2bI'

    # Авторизуемся и получаем service — экземпляр доступа к API
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    # Пример чтения файла
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:D52',
        # majorDimension='COLUMNS'
        majorDimension='ROWS'
    ).execute()
    pprint(values['values'])

def get_course():
    response = requests.get(
        url='http://www.cbr.ru/scripts/XML_daily.asp').text
    valutes = xmltodict.parse(response).get('ValCurs').get('Valute')
    for val in valutes:
        if val['@ID'] == 'R01235':
            # print('Доллар США: ', val['Value'])
            return val['Value']

    return 'на сегодня курс неизвестен'

print(float(get_course().replace(',', '.')))