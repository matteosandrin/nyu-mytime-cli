def while_find_element(css_selector,driver):
	item = ''
	while True:
		try:
			item = driver.find_element_by_css_selector(css_selector)
			break
		except:
			print("item not found")
	return item

def while_find_elements(css_selector,driver):
	items = ''
	while True:
		try:
			items = driver.find_elements_by_css_selector(css_selector)
			break
		except:
			print("item not found")
	return items