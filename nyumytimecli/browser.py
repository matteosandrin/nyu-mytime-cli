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
import click

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
	driver.implicitly_wait(1)
	return driver

def get_to_webclock(driver):
	if login(driver):
		switch_iframe("EntryFrame", driver)
		webclock_button = driver.find_element_by_link_text("Go to WebClock")
		webclock_button.click()
		return True
	else:
		driver.quit()
		return False

def login(driver):

	driver.get(LOGIN_URL)

	userid_field = driver.find_element_by_css_selector('input[id=netid]')
	password_field = driver.find_element_by_css_selector('input[id=password]')
	login_button = driver.find_element_by_css_selector('button[name="_eventId_proceed"]')

	userid_field.send_keys(USERNAME)
	password_field.send_keys(PASSWORD)
	login_button.click()

	click.secho("[info] Attempting to login...")

	if not check_successful_login(driver):
		click.secho("[error] Login failed: incorrect credentials.",fg='red')
		return False

	click.secho("[ ok ] Credentials accepted.", fg='green')

	if not switch_iframe("duo_iframe", driver):
		click.secho("[error] Failed to identify 2FA window", fg='red')
		return False

	if MFA_METHOD == 'push':
		auth_div = driver.find_element_by_css_selector(".row-label")
		click.secho("[info] Sending push notification to your device...")
	elif MFA_METHOD == 'call':
		auth_div = driver.find_element_by_css_selector(".row-label")
		click.secho("[info] Sending verification call to your device...")
	else:
		click.secho("[error] Invalid MFA method: "+MFA_METHOD, fg='red')
		return False

	push_button = auth_div.find_element_by_css_selector("button[type=submit]")
	push_button.click()

	if not check_successful_mfa(driver):
		click.secho("[error] MFA authentication failed.", fg='red')
		return False

	click.secho("[ ok ] MFA authentication successful.", fg='green')
	return True

def check_successful_login(driver):
	try:
		check_element = driver.find_element_by_css_selector("div[id=loginError]")
		return False
	except:
		return True # Successful login

def switch_iframe(iframe_id, driver):
	frame = while_find_element("#{}".format(iframe_id),driver, timeout=10)
	if frame is None:
		return False
	driver.switch_to_frame(frame)
	return True

def check_successful_mfa(driver):
	start = time.time()
	seconds = range(30,0,-1)

	bar_style = {
		"iterable": seconds,
		"show_percent" : False,
		"show_eta" : False,
		"item_show_func" : (lambda x: "[info] {}s remaining to authenticate...\n".format(x)),
		"bar_template": "%(info)s"
	}

	with click.progressbar(**bar_style) as bar:
		for s in bar:
			if driver.title == "Home":
				return True
			time.sleep(1)
	return False

def print_punch_status(driver):

	try:
		status = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.ID, "transientMessageContainer"))
		)
		
		with open(os.path.dirname(os.path.abspath(__file__)) + "/../html/page_source.html", "w") as source_file:
			source = driver.page_source
			source_file.write(source)

		message_box = status.find_element_by_css_selector(".x-box-middle-center")
		message = message_box.find_element_by_css_selector("div[id^=\"ext-gen\"]")
		return message.get_attribute("innerText")
	finally:
		driver.quit()

def punch(direction):

	button_id = ''
	if direction == 'in':
		button_id = ".IN_FOR_DAY"
	elif direction == 'out':
		button_id = ".OUT_FOR_DAY"
	else:
		click.secho("[error] Abort: invalid punch direction", fg='red')
		return

	driver = load_chrome_driver()
	if get_to_webclock(driver):
		punch_button = while_find_element(button_id, driver)
		punch_button.click()
		result = print_punch_status(driver)
		click.secho("[info] "+result)
		driver.quit()
		return True
	driver.quit()
	return False

def punch_in():	
	return punch("in")

def punch_out():
	return punch("out")