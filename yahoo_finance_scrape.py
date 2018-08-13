import json
import re
import requests
from bs4 import BeautifulSoup


BASE_URI = 'https://au.finance.yahoo.com/quote/{}/{}?p={}'

PAYLOADS = [['balance-sheet', 'APX.AX'],
            ['financials', 'APX.AX'],
            ['cash-flow', 'APX.AX']]


def get_html_table_data(soup):
    data = []

    for row in soup.find_all('tr'):
        row_data = []
        for td in row.find_all('td'):
            if td.get_text() == '-':
                row_data.append('0')
            else:
                row_data.append(td.get_text())

        data.append(row_data)

    return data


def get_balance_sheet(table_data):
    rec = re.compile(r'\S+\.?$', re.IGNORECASE)
    dict_data = {}
    heading_key = ''

    for i in range(1, len(table_data)):
        if len(table_data[i]) == 1:  # means its a main heading
            heading_key = rec.search(table_data[i][0]).group()
            dict_data[heading_key] = {}
            continue

        dict_data[heading_key][table_data[i][0]] = {}

        year_values = {k: float(v.replace(',', ''))
                       for k, v in zip(table_data[0][1:],
                                       table_data[i][1:])}

        dict_data[heading_key][table_data[i][0]] = year_values

    return dict_data


def get_income_cash_flow(table_data):
    dict_data = {}
    heading_key = ''

    for i in range(1, len(table_data)):
        if (i - 1) == 0:
            heading_key = table_data[i-1][0]
            dict_data[heading_key] = {}
        elif len(table_data[i]) == 1:
            heading_key = table_data[i][0]
            dict_data[heading_key] = {}
            continue

        dict_data[heading_key][table_data[i][0]] = {}

        year_values = {k: float(v.replace(',', ''))
                       for k, v in zip(table_data[0][1:],
                                       table_data[i][1:])}

        dict_data[heading_key][table_data[i][0]] = year_values

    return dict_data


def compile_financials():
    data = {}
    count = 1
    for i in PAYLOADS:
        statement, ticker = i
        req = requests.get(BASE_URI.format(i[1], i[0], i[1]))
        soup = BeautifulSoup(req.text, 'lxml')

        if count % 3 == 1:
            data[ticker] = {}

        table_data = get_html_table_data(soup)

        if statement == 'balance-sheet':
            data[ticker][statement] = get_balance_sheet(table_data)
        else:
            data[ticker][statement] = get_income_cash_flow(table_data)

        count += 1

    return data


if __name__ == '__main__':
    comp_data = compile_financials()
    json_data = json.dumps(comp_data, sort_keys=True, indent=4)

    with open('financial_statements.json', 'w') as f:
        f.write(json_data)
