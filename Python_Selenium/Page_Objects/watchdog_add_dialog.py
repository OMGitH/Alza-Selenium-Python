from selenium.webdriver.common.by import By
from object_handler import ObjectHandler


class WatchdogAdd(ObjectHandler):

	# Identification of objects on watchdog add dialog.
	email_input = (By.NAME, "email")
	price_limit_checkbox = (By.XPATH, "//input[contains(@class, 'PrivateSwitchBase')][not(contains(@name, 'isTrackingStock'))]")
	price_limit_input = (By.NAME, "price")
	confirm_button = (By.XPATH, "//button[contains(@class, 'blue')][contains(@class, 'price-box')]")

	# Initialization.
	def __init__(self, driver):
		super().__init__(driver)

	# Actions on watchdog add dialog.
	def get_email(self):
		if self.object_handler_is_visible(self.email_input):
			email_address = self.object_handler_get_element_attribute_value(self.email_input, "value")
			return email_address

	def set_price_limit(self, value):
		self.object_handler_hover_click(self.price_limit_checkbox, "'Při snížení ceny pod' checkbox", True)
		self.object_handler_clear_input_by_pressing_backspace(self.price_limit_input, "value")
		self.object_handler_send_keys(self.price_limit_input, value, "'Při snížení ceny pod' checkbox", True)

	def click_confirm_button(self):
		self.object_handler_click(self.confirm_button, "'Potvrdit' button", True)
		self.object_handler_is_invisible(self.email_input)
