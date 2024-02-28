from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class WatchdogAdd(ElementHandler):

	# Identification of elements on watchdog add dialog.
	email_input = (By.NAME, "email")
	price_limit_checkbox = (By.XPATH, "//input[contains(@class, 'price-box')][not(@name)]/following-sibling::*[name()='svg']")
	price_limit_input = (By.NAME, "price")
	confirm_button = (By.XPATH, "//button[contains(@class, 'blue')][contains(@class, 'price-box')]")

	# Actions on watchdog add dialog.
	def get_email(self):
		if self.element_handler_is_visible(self.email_input):
			email_address = self.element_handler_get_element_attribute_value(self.email_input, "value")
			return email_address

	def set_price_limit(self, value):
		self.element_handler_hover_click(self.price_limit_checkbox, "'Při snížení ceny pod' checkbox", True)
		self.element_handler_clear_input_by_pressing_backspace(self.price_limit_input, "value", "'Při snížení ceny pod' checkbox", True)
		self.element_handler_send_keys(self.price_limit_input, value, "'Při snížení ceny pod' checkbox", True)

	def click_confirm_button(self):
		self.element_handler_click(self.confirm_button, "'Potvrdit' button", True)
		self.element_handler_is_invisible(self.email_input)
