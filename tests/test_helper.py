from nyumytimecli import helper
from nyumytimecli import browser
import os.path
import pytest

@pytest.fixture()
def driver():
	return browser.load_chrome_driver()

def test_while_find_element(driver):
	driver.get("file://"+os.path.dirname(os.path.abspath(__file__))+"/test_html/test_while_find.html")
	element = helper.while_find_element("#testDiv", driver)
	assert element.text == "This is a test"

def test_multiple_while_find_element(driver):
	driver.get("file://"+os.path.dirname(os.path.abspath(__file__))+"/test_html/test_while_find.html")
	elements = helper.while_find_elements("#testDiv", driver)
	assert elements[0].text == "This is a test"