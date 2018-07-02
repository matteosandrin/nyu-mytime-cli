import time

def while_find_element(css_selector,driver, timeout=30):
	items = None
	start = time.time()
	while time.time() - start < timeout:
		try:
			items = driver.find_element_by_css_selector(css_selector)
			return items
		except:
			pass
	return None

def while_find_elements(css_selector,driver, timeout=30):
	items = None
	start = time.time()
	while time.time() - start < timeout:
		try:
			items = driver.find_elements_by_css_selector(css_selector)
			return items
		except:
			pass
	return None
	