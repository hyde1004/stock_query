
import requests  
import datetime  
from bs4 import BeautifulSoup as bs  
import pprint  
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# references:
#  - https://gspread.readthedocs.io/en/latest/ (gspread API Reference)
#  - https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html

check_days = [
	'2018-02-06', '2018-01-31', 
	'2017-12-28', '2017-11-30', '2017-10-31', '2017-09-29', '2017-08-31', '2017-07-31', '2017-06-30', '2017-05-31', '2017-04-28', '2017-03-31', '2017-02-28', '2017-01-31', 
	'2016-12-29', '2016-11-30', '2016-10-31', '2016-09-30', '2016-08-31', '2016-07-29', '2016-06-30', '2016-05-31', '2016-04-29', '2016-03-31', '2016-02-29', '2016-01-29', 
	'2015-12-30', '2015-11-30', '2015-10-30', '2015-09-30', '2015-08-31', '2015-07-31', '2015-06-30', '2015-05-29', '2015-04-30', '2015-03-31', '2015-02-27', '2015-01-30', 
	'2014-12-30', '2014-11-28', '2014-10-31', '2014-09-30', '2014-08-29', '2014-07-31', '2014-06-30', '2014-05-30', '2014-04-30', '2014-03-31', '2014-02-28', '2014-01-29', 
	'2013-12-30', '2013-11-29', '2013-10-31', '2013-09-30', '2013-08-30', '2013-07-31', '2013-06-28', '2013-05-31', '2013-04-30', '2013-03-29', '2013-02-28', '2013-01-31', 
	'2012-12-28', '2012-11-30', '2012-10-31', '2012-09-28', '2012-08-31', '2012-07-31', '2012-06-29', '2012-05-31', '2012-04-30', '2012-03-30', '2012-02-29', '2012-01-31', 
	'2011-12-29', '2011-11-30', '2011-10-31', '2011-09-30', '2011-08-31', '2011-07-29', '2011-06-30', '2011-05-31', '2011-04-29', '2011-03-31', '2011-02-28', '2011-01-31', 
	'2010-12-30', '2010-11-30', '2010-10-29', '2010-09-30', '2010-08-31', '2010-07-30', '2010-06-30', '2010-05-31', '2010-04-30', '2010-03-31', '2010-02-26', '2010-01-29', 
	'2009-12-30', '2009-11-30', '2009-10-30', '2009-09-30', '2009-08-31', '2009-07-31', '2009-06-30', '2009-05-29', '2009-04-30', '2009-03-31', '2009-02-27', '2009-01-30', 
	'2008-12-30', '2008-11-28', '2008-10-31', '2008-09-30', '2008-08-29', '2008-07-31'	]
my_stocks = ['034950', '092130', '015760', '002960', '002460', '017670', '114090', '115310']
stock_name = {'034950': '한국기업평가', '092130': '이크레더블', '015760':'한국전력', '002960':'한국쉘석유', '002460':'화성산업', '017670':'SK텔레콤', '114090':'GKL', '115310':'인포바인'}
index_day = []
result = {}
period = range(1, 36)

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

	row = 1
	col = 1
	sheet.update_cell(row, col, 'date')
	
	for check_day in check_days:
		row = row + 1
		result[check_day] = []
		sheet.update_cell(row, col, check_day)

def get_referece_day(row):
	return sheet.cell(row, 1).value

def do_query(stocks):
	print('query...')

	prev = datetime.date(1900, 1, 1)

	for stock in stocks:
		row = 2
		col = stocks.index(stock) + 2
		reference_row = 2
		sheet.update_cell(1, col, stock_name[stock])
		for page in period:
			query_url = 'http://finance.naver.com/item/frgn.nhn?code=%s&page=%s' % (stock, page) 

			r = requests.get(query_url)   
			html = r.text   
			soup = bs(html, 'html.parser')   
			day_info= soup.select('body > div > div > div > div > table > tr > td:nth-of-type(1) > span')   
			foreign_info = soup.select('body > div > div > div > div > table > tr > td:nth-of-type(9) > span') 

			for day, foreign in zip(day_info, foreign_info):   
				s = datetime.datetime.strptime(day.text, '%Y.%m.%d')   
				current = datetime.date(s.year, s.month, s.day)   
				t = datetime.datetime.strptime(get_referece_day(reference_row), '%Y-%m-%d')
				reference = datetime.date(t.year, t.month, t.day)
				print('reference:%s, current:%s' % (reference, current) )
				if current == reference:
					k = current.strftime('%Y-%m-%d')
					print('index: %s' % stocks.index(stock))
					result[k].append(foreign.text)
					sheet.update_cell(row, col, foreign.text)
					row = row + 1
					reference_row = reference_row + 1
				elif current > reference:
					continue
				elif current < reference:
					print("Error")
					return
				prev = current 

if __name__ == "__main__":
#	do_init()
	do_index(my_stocks)
	do_query(my_stocks)
	print(result)