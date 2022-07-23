# docs: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values
from pprint import pprint

import apiclient.discovery
import httplib2
import requests
import xmltodict
from oauth2client.service_account import ServiceAccountCredentials
from sheetfu import SpreadsheetApp

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
        range='Лист1!A1:D52',
        # majorDimension='COLUMNS'
        majorDimension='ROWS'
    ).execute()
    # count = service.spreadsheets().values().get_data_range()
    pprint(values['values'],)

def get_gogle2():
    CREDENTIALS_FILE = 'creds.json'
    spreadsheet_id = '1-fh9NMsarGBp0ILsNFqhpdTBL_Nzlmaub13kdiZU2bI'
    sa = SpreadsheetApp(CREDENTIALS_FILE)
    spreadsheet = sa.open_by_id(spreadsheet_id=spreadsheet_id)
    sheet = spreadsheet.get_sheet_by_name('Лист1')
    data_range = sheet.get_data_range()
    pprint(type(data_range))

def get_course():
    response = requests.get(
        url='http://www.cbr.ru/scripts/XML_daily.asp').text
    valutes = xmltodict.parse(response).get('ValCurs').get('Valute')
    for val in valutes:
        if val['@ID'] == 'R01235':
            # print('Доллар США: ', val['Value'])
            return val['Value']

    return 'на сегодня курс неизвестен'

# print(float(get_course().replace(',', '.')))
get_gogle2()