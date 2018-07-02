from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nyumytimecli.helper import *
import os.path
import configparser
import time
import base64

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + '/config.ini')

LOGIN_URL = config["DEFAULT"]["LOGIN_URL"]

if "USERNAME" in config["DEFAULT"]:
	USERNAME = config["DEFAULT"]["USERNAME"]

if "PASSWORD" in config["DEFAULT"]:
	PASSWORD = config["DEFAULT"]["PASSWORD"]
	PASSWORD = base64.b64decode(PASSWORD).decode('utf-8')

if "MFA_METHOD" in config["DEFAULT"]:
	MFA_METHOD = config["DEFAULT"]["MFA_METHOD"]

if "CHROMEDRIVER_PATH" in config["DEFAULT"]:
	CHROMEDRIVER_PATH = config["DEFAULT"]["CHROMEDRIVER_PATH"]


def load_chrome_driver():
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("window-size=1920x1080")
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROMEDRIVER_PATH)
	driver.implicitly_wait(10)
	return driver

def switch_iframe(iframe_id, driver):
	frame = while_find_element("#{}".format(iframe_id),driver)
	driver.switch_to_frame(frame)

def login(driver):

	driver.get(LOGIN_URL)

	userid_field = driver.find_element_by_css_selector('input[id=netid]')
	password_field = driver.find_element_by_css_selector('input[id=password]')
	login_button = driver.find_element_by_css_selector('button[name="_eventId_proceed"]')

	userid_field.send_keys(USERNAME)
	password_field.send_keys(PASSWORD)
	login_button.click()

	print("Attempting to login...")

	switch_iframe("duo_iframe", driver)	

	print("Credentials accepted.")

	if MFA_METHOD == 'push':
		auth_div = while_find_element(".row-label",driver)
		print("Sending push notification to your device...")
	elif MFA_METHOD == 'call':
		auth_div = while_find_element(".row-label",driver)
		print("Sending verification call to your device...")
	else:
		print("Invalid MFA method:",MFA_METHOD)
		return False

	push_button = auth_div.find_element_by_css_selector("button[type=submit]")
	push_button.click()

	start = time.time()
	while time.time() - start < 60:
		if driver.title == "Home":
			print("Login successful!")
			return True
	print("Login failed.")
	return False

def get_to_webclock(driver):
	if login(driver):
		switch_iframe("EntryFrame", driver)
		webclock_button = driver.find_element_by_link_text("Go to WebClock")
		webclock_button.click()

def print_punch_status(driver):

	try:
		status = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "transientMessageContainer"))
		)
		
		with open(os.path.dirname(os.path.abspath(__file__)) + "/../html/page_source.html", "w") as source_file:
			source = driver.page_source
			source_file.write(source)

		# print("<{} id='{}'>".format(status.tag_name, status.get_attribute("id")))
		message_box = status.find_element_by_css_selector(".x-box-middle-center")
		# print("<{} class='{}'>".format(message_box.tag_name, message_box.get_attribute("class")))
		message = message_box.find_element_by_css_selector("div[id^=\"ext-gen\"]")
		# print("<{} id='{}'>".format(message.tag_name, message.get_attribute("id")))
		# print(message.text)
		return message.text
	finally:
		driver.quit()

def punch(direction):

	button_id = ''
	if direction == 'in':
		button_id = ".IN_FOR_DAY"
	elif direction == 'out':
		button_id = ".OUT_FOR_DAY"
	else:
		print("Abort: invalid punch direction")
		return

	driver = load_chrome_driver()
	get_to_webclock(driver)
	punch_button = while_find_element(button_id, driver)
	punch_button.click()
	result = print_punch_status(driver)
	print(result)
	driver.quit()

def punch_in():	
	punch("in")

def punch_out():
	punch("out")

def print_punch_test():
	driver = load_chrome_driver()
	driver.get("file:///Users/matteosandrin/.fuck-you-virtual-env/nyu-mytime-cli/html/transient2.html")
	print_punch_status(driver)