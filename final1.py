from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re, time
from selenium.common.exceptions import WebDriverException
from selenium import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


infile = open('input1.txt')
outfile = open('output1.txt', 'w')	
driver = webdriver.Firefox()	

driver.get("http://www.mca.gov.in/DCAPortalWeb/dca/MyMCALogin.do?method=setDefaultProperty&mode=31")

for letter in infile:
	compnynm = driver.find_element_by_id("companyName")		#compnynm denotes the text field on the page with text before it "Company Name	 :"
	compnynm.send_keys(letter)

	search = driver.find_element_by_id("cinLookup")		#search denotes the search button next to compnynm
	search.click()
	
	driver.implicitly_wait(5)

	driver.switch_to_window(driver.window_handles[-1])
	driver.implicitly_wait(5)

	while(True):
		for x in range(0, 10):
			try:
				name1 = driver.find_element_by_id('strCompanyName' + str(x))
				ID = driver.find_element_by_id('strCin' + str(x))  
				IDvalue = ID.get_attribute('value')
				name1value = name1.get_attribute('value')
				outfile.write('{0}'.format(IDvalue)+"	"+'{0}'.format(name1value)+"\n")
			except NoSuchElementException:
				outfile.write("")

		try:
			nextIcon =  driver.find_element_by_id("nextlistlov")
			nextIcon.click()
		except NoSuchElementException:
			cancelwindow = driver.find_element_by_id("button2")
			cancelwindow.click()
			driver.switch_to_window(driver.window_handles[-1])
			driver.close()
			driver.switch_to_window(driver.window_handles[-1])
			break