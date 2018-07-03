from nyumytimecli import browser
import os.path
import pytest

@pytest.fixture()
def driver():
	return browser.load_chrome_driver()


def test_presence_of_global_variables():
	symbols = dir(browser)
	assert "LOGIN_URL" in symbols
	assert "USERNAME" in symbols
	assert "PASSWORD" in symbols
	assert "MFA_METHOD" in symbols
	assert "CHROMEDRIVER_PATH" in symbols

def test_printing_punch_out_status(driver):
	
	driver.get("file://"+os.path.dirname(os.path.abspath(__file__))+"/test_html/test_status_page.html")
	status = browser.print_punch_status(driver)
	status = status.replace(u'\xa0', u' ')
	assert status == "Thu 06/28 12:03 pm: Out Punch Recorded Successfully."
	driver.quit()

def test_iframe_switching(driver):
	driver.get("file://"+os.path.dirname(os.path.abspath(__file__))+"/test_html/test_iframe_page.html")
	browser.switch_iframe("testFrame", driver)
	div = driver.find_element_by_css_selector("#testDiv")
	assert div.text == "This is a test"
	driver.quit()
