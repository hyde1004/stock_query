import requests  
import datetime  
from bs4 import BeautifulSoup as bs  
import pprint  
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("test").sheet1

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

import collections
ordered_sums = collections.OrderedDict(sorted(sums.items()))

row = 1
sheet.update_cell(row, 1, 'Time')
sheet.update_cell(row, 2, 'Monthly Sum')

for k, v  in ordered_sums.items():
    row = row + 1
    print(k, v)
    sheet.update_cell(row, 1, "'" + str(k))
    sheet.update_cell(row, 2, v)







