from selenium.common.exceptions import NoSuchElementException
import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re, time
from selenium.common.exceptions import WebDriverException
from selenium import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

infile = open('output1.txt')
outfile = open('output2.txt', 'w')
charges_outfile = open('output3.txt', 'w')

data = []   #declaring an empty list that will store data of table rows 
tds = []
not_required = ["ROC Code", "Company Category", "Company Subcategory", "Class of Company", "Authorised Capital(in Rs.)", "Paid up capital(in Rs.)", "Number of Members(Applicable only in case of company without Share Capital)", "Date of Incorporation", "Country", "Whether listed or not", "Date of Last AGM", "Date of Balance sheet"]	#company parameters that are not included in main output
sig_data = []	#list that will store data about signatories
sig_tds = []
CINno=""  #it stores the CIN no. of the company
charge_tds = []


driver = webdriver.Firefox()
driver.get("http://www.mca.gov.in/DCAPortalWeb/dca/MyMCALogin.do?method=setDefaultProperty&mode=31")

for line in infile:
	data_array = line.split('	')
	compnyID = driver.find_element_by_id("cin")
	compnyID.send_keys(data_array[0])	
	submitbutton = driver.find_element_by_id("Default")
	submitbutton.click()

	driver.switch_to_window(driver.window_handles[-1])

	#scraping and storing company data
	rows = driver.find_elements_by_xpath('.//table[@id="DataBlock1"]//tr')
	data[:] = []
	for tr in rows:
		tds = tr.find_elements_by_tag_name('td')
		if(len(tds)==2):
			for td in tds:			
				data.append(td.text)					#data[] stores data of various columns in a row of the table
			if((data[0] in not_required) == False):
				if(data[0] == 'CIN '):
					CINno = data[1]
				outfile.write(data[0]+" = "+data[1]+", ")
		data[:] = []
		tds[:] = []			

	#scraping and storing signatory data
	signatories = driver.find_element_by_link_text("Signatories of the Company")
	signatories.click()
	driver.switch_to_window(driver.window_handles[-1])
	outfile.write("Signatories :- ")
	driver.implicitly_wait(10)
	sig_rows = driver.find_elements_by_xpath('.//table[@id="DataBlock1"]//tr')
	
	for tr in sig_rows:
		sig_tds = tr.find_elements_by_tag_name('td')
		if(len(sig_tds)>1):
			for td in sig_tds:
				sig_data.append(td.text)
			if(sig_data[1] != "Director Name"):				#see
				outfile.write(sig_data[1]+" - "+sig_data[2]+", ")
		sig_data[:] = []
		sig_tds[:] = []

	outfile.write("\n")
	outfile.write("\n")

	driver.close()
	driver.switch_to_window(driver.window_handles[-1])

	#scraping and storing charges data
	charges = driver.find_element_by_link_text("Charges Registered")
	charges.click()
	driver.switch_to_window(driver.window_handles[-1])
	driver.implicitly_wait(10)
	charges_outfile.write("CIN :- "+CINno+"\n")
	try:
		charge_table = driver.find_element_by_id('list1')
		charge_table_rows = driver.find_elements_by_xpath('.//table[@id="list1"]//tr')
		charges_outfile.write("S.No."+"	"+"Charge ID"+"	"+"Date of Charge Creation/Modification"+"	"+"Charge amount secured"+"	"+"Charge Holder"+"	"+"Address"+"Service Request Number (SRN)")
		for tr in charge_table_rows:
			charge_tds = tr.find_elements_by_tag_name('td')
			for td in charge_tds:
				charges_outfile.write(td.text+"	,")
			charges_outfile.write("\n")
			charge_tds[:] = []
		charges_outfile.write("\n")
		CINno = ""
		driver.close()
		driver.switch_to_window(driver.window_handles[-1])


	except NoSuchElementException:
		charges_outfile.write("No charges on this company \n")
		charges_outfile.write("\n")
		CINno = ""
		driver.close()
		driver.switch_to_window(driver.window_handles[-1])
		driver.close()
		driver.switch_to_window(driver.window_handles[-1])

	back_button = driver.find_element_by_id("Default")
	back_button.click()