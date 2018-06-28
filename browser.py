from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helper import *
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


def load_chrome_driver():
	chrome_options = Options()
	# chrome_options.add_argument("--headless")
	chrome_options.add_argument("window-size=1920x1080")
	chrome_driver = os.getcwd() + "/chromedriver"
	driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
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
	status = while_find_element("#transientMessageContainer",driver)
	message_box = status.find_element_by_css_selector(".x-box-middle-center")
	message = message_box.find_element_by_css_selector("div[id^=\"ext-gen\"]")
	return message.text

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

def punch_in():	
	punch("in")

def punch_out():
	punch("out")
