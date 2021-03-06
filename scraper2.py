#Scraper 2 Flipkart

import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

#Path for chrome driver in local machine
#Change it accordingly
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
url = "https://www.flipkart.com"

def get_url(search_term):
	template = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
	search_term = search_term.replace(' ','+')
	return template.format(search_term)

data_list = []
rank = 0
#page = 0
#flag = 1

#First 5 pages
#Change range to increase the no of pages to traverse
for page in range(1, 2):
	#page = page + 1
	print('Processing page no: ', page, ' ****************************************************************************************')
	url = get_url('shoes')
	extension = '&page=' + str(page)
	url += extension
	driver.get(url)

	soup = BeautifulSoup(driver.page_source, 'html.parser')

	#for every row
	results = soup.find_all('div',{'class': '_1AtVbE col-12-12'})
	for result in results:
		next_div = result.find_all('div',{'class': '_13oc-S'})

		for item in next_div:
			divs = item.find_all('div', {'style': 'width:25%'})
			divs2 = item.find_all('div', {'style': 'width:100%'})


			#for 4 elements in a row
			if len(divs) != 0:

				for div_tab in divs:
					element_list = []
					rank = rank + 1
					element_list.append(rank)
					element_list.append(div_tab.get('data-id'))

					fassured = div_tab.find_all('img', {'src': '//static-assets-web.flixcart.com/www/linchpin/fk-cp-zion/img/fa_62673a.png'})
					if len(fassured) >= 1:
						element_list.append(1)#product is flipkart assured
					else:
						element_list.append(0)

					spantag = div_tab.find_all('span')
					#for checking AD
					flag = 0
					for span in spantag:
						if span.text == 'Ad':
							flag = 1 #1 means it is advertised
							break
					element_list.append(flag)

					#dont need following line
					#atags = div_tab.find_all('a')
					#for a in atags:
					#	if a.get('title'):
					#		element_list.append(a.get('title'))

					data_list.append(element_list)

			#for 1 element in a row
			elif len(divs2) != 0:
				for div_tab in divs2:
					element_list = []
					element_list.append(div_tab.get('data-id'))
					rank = rank + 1
					element_list.append(rank)
					fassured = div_tab.find_all('img', {'src': '//static-assets-web.flixcart.com/www/linchpin/fk-cp-zion/img/fa_62673a.png'})
					if len(fassured) >= 1:
						element_list.append(1)#product is flipkart assured
					else:
						element_list.append(0)
					spantag = div_tab.find_all('span')

					#for checking AD
					flag = 0
					for span in spantag:
						if span.text == 'Ad':
							flag = 1 #1 means it is advertised
					element_list.append(flag)
					a = div_tab.find('a')
					#dont need next line
					#element_list.append(a.text)

					data_list.append(element_list)

frame = pd.DataFrame(data_list, columns = ['Rank', 'Data-id', 'Flipkart-Assured?', 'Advertised?'])
frame.to_csv('Product_info_scraper2.csv')
#for listele in data_list:
#	print(listele)
