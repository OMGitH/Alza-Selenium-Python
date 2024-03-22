from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class WatchdogAdd(ElementHandler):

	# Identification of elements on watchdog add dialog.
	email_input = (By.NAME, "email")
	item_price_limit_checkbox = (By.CSS_SELECTOR, "svg[class*='Checkbox'][class*='price-box'] g[fill]")
	item_price_limit_input = (By.NAME, "price")
	confirm_button = (By.CSS_SELECTOR, "button[class*='blue'][class*='price-box']")

	# Actions on watchdog add dialog.
	def get_email(self):
		email_address = self.element_handler_get_element_attribute(self.email_input, "value", "E-mail input field value at watchdogs add dialog")
		return email_address

	def set_price_limit(self, value):
		self.element_handler_hover_click(self.item_price_limit_checkbox, "'Při snížení ceny pod' checkbox", True)
		self.element_handler_clear_input_by_pressing_backspace(self.item_price_limit_input, "value", "'Při snížení ceny pod' input field", True)
		self.element_handler_send_keys(self.item_price_limit_input, value, "'Při snížení ceny pod' input field", True)

	def click_confirm_button(self):
		self.element_handler_click(self.confirm_button, "'Potvrdit' button at watchdogs add dialog", True)
		self.element_handler_is_invisible(self.email_input, "E-mail input field at watchdogs add dialog")
