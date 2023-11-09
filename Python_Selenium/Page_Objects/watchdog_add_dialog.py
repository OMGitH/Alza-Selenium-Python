from selenium.webdriver.common.by import By
from Page_objects.base_page import BasePage


class WatchdogAdd(BasePage):
	# Identification of objects on watchdog add dialog.
	watchdog_email_input = (By.NAME, "email")
	watchdog_price_limit_checkbox = (By.XPATH, "//input[contains(@class, 'PrivateSwitchBase')][not(contains(@name, 'isTrackingStock'))]")
	watchdog_price_limit_input = (By.NAME, "price")
	watchdog_confirm_button = (By.XPATH, "//button[contains(@class, 'blue')][contains(@class, 'price-box')]")

	# Initialization.
	def __init__(self, driver):
		super().__init__(driver)

	# Actions on watchdog add dialog.
	def watchdog_add_dialog_get_email(self):
		if self.base_is_visible(self.watchdog_email_input):
			email_address = self.base_get_element_attribute_value(self.watchdog_email_input, "value")
			return email_address

	def watchdog_add_dialog_set_price_limit(self, value):
		self.base_hover_click(self.watchdog_price_limit_checkbox)
		self.base_clear_input_by_pressing_backspace(self.watchdog_price_limit_input, "value")
		self.base_send_keys(self.watchdog_price_limit_input, value)

	def watchdog_add_dialog_click_confirm_button(self):
		self.base_click(self.watchdog_confirm_button)
		self.base_is_invisible(self.watchdog_email_input)