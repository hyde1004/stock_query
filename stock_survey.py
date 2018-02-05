
import requests  
import datetime  
from bs4 import BeautifulSoup as bs  
import pprint  
import gspread
from oauth2client.service_account import ServiceAccountCredentials

my_stocks = ['034950', '092130', '015760', '002960']
stock_name = {'034950': '한국기업평가', '092130': '이크레더블', '015760':'한국전력', '002960':'한국쉘석유'}
index_day = []
result = {}

#def do_init():
	# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

	# Find a workbook by name and open the first sheet
	# Make sure you use the right name here.
sheet = client.open("test").sheet1	
sheet.clear()

def do_index(stocks):
	print('index...')

	sheet.update_cell(1, 1, "Time")
	prev = datetime.date(1900, 1, 1)
	stock = stocks[0]
	row = 2

	for page in range(1, 10):
		query_url = 'http://finance.naver.com/item/frgn.nhn?code=%s&page=%s' % (stock, page) 
		#print(query_url)
		r = requests.get(query_url)   
		html = r.text   
		soup = bs(html, 'html.parser')   
		day_info= soup.select('body > div > div > div > div > table > tr > td:nth-of-type(1) > span')   
		foreign_info = soup.select('body > div > div > div > div > table > tr > td:nth-of-type(9) > span')  

		for day in day_info:   
			s = datetime.datetime.strptime(day.text, '%Y.%m.%d')   
			current = datetime.date(s.year, s.month, s.day)  
			#print(current) 
			if (current.year != prev.year or current.month != prev.month): 
				k = current.strftime('%Y-%m-%d')
				result[k] = []
				sheet.update_cell(row, 1, k)
				row = row + 1
			prev = current 


def do_query(stocks):
	print('query...')

	prev = datetime.date(1900, 1, 1)

	for stock in stocks:
		row = 2
		col = stocks.index(stock) + 2
		sheet.update_cell(1, col, stock_name[stock])
		for page in range(1, 10):
			query_url = 'http://finance.naver.com/item/frgn.nhn?code=%s&page=%s' % (stock, page) 

			r = requests.get(query_url)   
			html = r.text   
			soup = bs(html, 'html.parser')   
			day_info= soup.select('body > div > div > div > div > table > tr > td:nth-of-type(1) > span')   
			foreign_info = soup.select('body > div > div > div > div > table > tr > td:nth-of-type(9) > span') 

			for day, foreign in zip(day_info, foreign_info):   
				s = datetime.datetime.strptime(day.text, '%Y.%m.%d')   
				current = datetime.date(s.year, s.month, s.day)   
				if (current.year != prev.year or current.month != prev.month): 
					k = current.strftime('%Y-%m-%d')
					print('index: %s' % stocks.index(stock))
					result[k].append(foreign.text)
					sheet.update_cell(row, col, foreign.text)
					row = row + 1			
				prev = current 

if __name__ == "__main__":
#	do_init()
	do_index(my_stocks)
	do_query(my_stocks)
	print(result)