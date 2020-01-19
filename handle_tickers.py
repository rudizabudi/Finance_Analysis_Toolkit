import bs4 as bs
import requests
import os
import sys


def save_tickers():
    print('--> Currently supported: Wikipedia, Gurufocus, OnVista Index List')
    url = 'https://' + str(input('Enter URL with stock symbol table [without: https://]: '))
    token = str(input('Enter exchange token [optional]: '))

    resp = requests.get(url)
    bsobj = bs.BeautifulSoup(resp.text, 'lxml')
    website_type = 0
    if 'wikipedia' in url:
        tables = bsobj.select('table', {'class': 'wikitable sortable'})
        website_type = 1
    elif 'gurufocus' in url:
        tables = bsobj.select('table', {'class': 'R5'})
        website_type = 1
    elif 'onvista' in url:
        tables = bsobj.select('table', {'class': 'has-light-border'})
        website_type = 2
    else:
        print('-->  URL not supported!')
        return

    if website_type == 1:
        i = 0
        for table in tables:
            if ("Symbol" in str(table) or "Ticker" in str(table)) and ("Name" in str(table) or "Security" in str(table) or "Company" in str(table) or "Constituent" in str(table)):
                break
            i += 1

        j = 0
        for cols in tables[i].findAll('th'):
            if "Symbol" in str(cols) or "Ticker" in str(cols):
                break
            j += 1

        tickers = []
        for row in tables[i].findAll('tr')[1:]:
            ticker = row.findAll('td')[j].text
            if "\n" in ticker:
                ticker = ticker[:-1]
            if 'gurufocus' in url and '.' in ticker and ticker.index('.') + 1 != len(ticker):
                ticker = ticker[:ticker.index('.')]
            if ticker[-1] == '.':
                ticker = ticker[:-1]
            ticker = ticker + token
            # print(ticker)
            tickers.append(ticker)

    elif website_type == 2:
        for i, table in enumerate(tables):
            if 'Name' in str(table) and 'akt. Kurs' in str(table):
                break

        tickers = []
        table_length = int(len(tables[i].findAll('tr')[1:]))
        for j, row in enumerate(tables[i].findAll('tr')[1:], start=1):
            for item in row.findAll('a'):
                link = item.get('href')
                stock_link = requests.get('https://www.onvista.de' + str(link))
                bsobj_stock = bs.BeautifulSoup(stock_link.text, 'lxml')
                stock_tables = bsobj_stock.select('div.WERTPAPIER_DETAILS')
                ticker = str(stock_tables[0])[str(stock_tables[0]).rindex('<dt>Symbol</dt><dd>') + 19:][:str(stock_tables[0])[str(stock_tables[0]).rindex('<dt>Symbol</dt><dd>') + 19:].index('</dd>')]
                ticker = ticker + token
                tickers.append(ticker)

            sys.stdout.write('\r')
            ticks = int(round(j / table_length * 20, 0))
            sys.stdout.write("[%-20s] %d%%" % ('=' * ticks, j * (100 / table_length)))
            sys.stdout.flush()

    if not os.path.exists(os.getcwd() + '\\Stock_Symbol_List\\'):
        os.makedirs(os.getcwd() + '\\Stock_Symbol_List\\')

    # name = url[url.rindex('/') + 1:]
    name = str(input('\nEnter symbol list name: '))

    to_txt = open(os.getcwd() + '\\Stock_Symbol_List\\' + name + '.txt', 'w')
    for ticker in tickers:
        to_txt.write(ticker + '\n')
    to_txt.close()

    print('--> File ' + name + '.txt successfully created!')
    print('--> Path: ' + os.getcwd() + '\\Stock_Symbol_List\\' + name + '.txt')


def select_tickers():
    contents = os.listdir(os.getcwd() + '\\Stock_Symbol_List')
    i = 0
    for file in contents:
        if ".txt" in file:
            print('--> ' + str(i) + ' : ' + file)
            i += 1

    selection = -1
    while int(selection) < 0 or int(selection) > len(contents) - 1:
        selection = input('Select tickers by index: ')

    return contents[int(selection)]


