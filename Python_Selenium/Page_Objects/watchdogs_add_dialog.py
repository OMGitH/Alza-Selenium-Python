from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class WatchdogAdd(ElementHandler):

	# Identification of elements on watchdog add dialog.
	email_input = {
		"locator": (By.NAME, "email"),
		"name": "E-mail input field at watchdogs add dialog"
	}
	item_price_limit_checkbox = {
		"locator": (By.CSS_SELECTOR, "svg[class*='Checkbox'][class*='price-box'] g[fill]"),
		"name": "'Při snížení ceny pod' checkbox"
	}
	item_price_limit_input = {
		"locator": (By.NAME, "price"),
		"name": "'Při snížení ceny pod' input field"
	}
	confirm_button = {
		"locator": (By.CSS_SELECTOR, "button[class*='blue'][class*='price-box']"),
		"name": "'Potvrdit' button at watchdogs add dialog"
	}

	# Actions on watchdog add dialog.
	def get_email(self):
		email_address = self.element_handler_get_element_attribute(self.email_input["locator"], "value", self.email_input["name"])
		return email_address

	def set_price_limit(self, value):
		self.element_handler_hover_click(self.item_price_limit_checkbox["locator"], self.item_price_limit_checkbox["name"], True)
		self.element_handler_clear_input_by_pressing_backspace(self.item_price_limit_input["locator"], "value", self.item_price_limit_input["name"], True)
		self.element_handler_send_keys(self.item_price_limit_input["locator"], value, self.item_price_limit_input["name"], True)

	def click_confirm_button(self):
		self.element_handler_click(self.confirm_button["locator"], self.confirm_button["name"], True)
		self.element_handler_is_invisible(self.email_input["locator"], self.email_input["name"])
