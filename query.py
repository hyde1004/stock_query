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
pp.pprint(sums) 

																			  

																			   

																			    

																			     
