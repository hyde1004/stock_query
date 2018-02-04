import requests  

import datetime  

from bs4 import BeautifulSoup as bs  

import pprint  

 
 

#stock = '034950'  

stock = '092130' 

 
 

sums = {}   

url = 'http://finance.naver.com/item/frgn.nhn?code=%s&page=' % stock  

page = 1  

prev = datetime.date(1900, 1, 1) 

per_old = 0 

 
 

while page < 100:  

    query = url + str(page)  

#    print('Query ' + query)  

    r = requests.get(query)   

    html = r.text   

    soup = bs(html, 'html.parser')   

    day_info= soup.select('body > div > div > div > div > table > tr > td:nth-of-type(1) > span')   

    trade_info = soup.select('body > div > div > div > div > table > tr > td:nth-of-type(9) > span')  

    for day, trade in zip(day_info, trade_info):   

        s = datetime.datetime.strptime(day.text, '%Y.%m.%d')   

        current = datetime.date(s.year, s.month, s.day)   

        if (current.year != prev.year or current.month != prev.month): 

            per_cur = float(trade.text.replace('%', '')) 

            diff = per_old - per_cur 

#            print(day.text + ":" + trade.text + '(' + str(diff) + ')' ) 

            output = '{} : {} ({:.2f}%)'.format(day.text, trade.text, diff) 

            print(output) 

            per_old = per_cur 

        prev = current 

    page = page + 1  

ijeong-guui-MacBook-Pro:~ hyde1004$ cat query.py  

import requests  

import datetime  

from bs4 import BeautifulSoup as bs  

import pprint  

 
 

stock = '034950'  

sums = {}   

url = 'http://finance.naver.com/item/frgn.nhn?code=%s&page=' % stock  

page = 1  

 
 

while page < 100:  

    query = url + str(page)  

    print('Query ' + query)  

    r = requests.get(query)   

    html = r.text   

    soup = bs(html, 'html.parser')   

    day_info= soup.select('body > div > div > div > div > table > tr > td:nth-of-type(1) > span')   

    trade_info = soup.select('body > div > div > div > div > table > tr > td:nth-of-type(7) > span')  

    for day, trade in zip(day_info, trade_info):   

        s = datetime.datetime.strptime(day.text, '%Y.%m.%d')   

        t = datetime.date(s.year, s.month, s.day)   

        k = t.strftime('%Y-%m')   

        amount = int((trade.text).replace(',', ''))  

        if k in sums:   

            sums[k] = sums[k] +  amount  

        else:   

            sums[k] = amount  

    page = page + 1  

 
 

pp = pprint.PrettyPrinter(indent=4)  

