import bs4 as bs
import requests
import os

def save_tickers():
    #wiki = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    #token = ''
    print('--> Currently supported: Wikipedia, Gurufocus')
    url = 'https://' + str(input('Enter URL with stock symbol table [without: https://]: '))
    token = str(input('Enter exchange token [optional]: '))

    resp = requests.get(url)
    bsobj = bs.BeautifulSoup(resp.text, 'lxml')
    if 'wikipedia' in url:
        tables = bsobj.select('table', {'class': 'wikitable sortable'})
    elif 'gurufocus' in url:
        tables = bsobj.select('table', {'class': 'R5'})
    else:
        print('-->  URL not supported!')
        return

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
        ticker = (ticker + token)
        #print(ticker)
        tickers.append(ticker)

    if not os.path.exists(os.getcwd() + '\\Stock_Symbol_List\\'):
        os.makedirs(os.getcwd() + '\\Stock_Symbol_List\\')

    #name = url[url.rindex('/') + 1:]
    name = str(input('Enter symbol list name: '))

    to_txt =  open(os.getcwd() + '\\Stock_Symbol_List\\' + name + '.txt', 'w')
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
    while int(selection) < 0 or int(selection) > len(contents)-1:
        selection = input('Select tickers by index: ')

    return contents[int(selection)]


