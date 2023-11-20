from selenium.webdriver.common.by import By
from Page_Objects.base_page import BasePage


class Watchdogs(BasePage):

	# Identification of objects on watchdogs page.
	watchdog_item = (By.XPATH, "//div[@data-testid='page-watchDogs']//a")
	watchdog_item_remove_button = (By.XPATH, "//div[@data-testid='page-watchDogs']//button")
	watchdog_item_removal_confirmation_button = (By.XPATH, "//button[contains(@class, 'red')]")
	watchdog_remove_question_dialog = (By.XPATH, "//div[@role='dialog']")
	watchdog_price_limit_provided = (By.NAME, "price")
	watchdog_checked_alert_price_checkbox = (By.XPATH, "//input[not (@name)]/parent::span/*[name()='svg']/*[name()='g' and @transform]")
	watchdog_text_all_items_removed_from_watchdog_list = (By.XPATH, "//div[@data-testid='noResults']/span")

	# Initialization.
	def __init__(self, driver):
		super().__init__(driver)

	# Actions on watchdogs page.
	def watchdogs_remove_all_items_from_watchdogs_list(self):
		while self.base_get_state(self.watchdog_item_remove_button, self.watchdog_text_all_items_removed_from_watchdog_list) == self.watchdog_item_remove_button:
			self.base_click(self.watchdog_item_remove_button)
			self.base_click(self.watchdog_item_removal_confirmation_button)
			self.base_is_invisible(self.watchdog_remove_question_dialog)

	# def watchdogs_remove_all_items_from_watchdogs_list(self):
	# 	if self.base_is_visible(self.watchdog_item, 3, True):
	# 		while self.base_is_visible(self.watchdog_item_remove_button, 1, True):
	# 			self.base_click(self.watchdog_item_remove_button)
	# 			self.base_click(self.watchdog_item_removal_confirmation_button)
	# 			self.base_is_invisible(self.watchdog_remove_question_dialog)

	"""
	Code below uses get state method that is faster as it doesn't wait for timeout to make sure whether or not there is an item
	identifying a state (if there is an item in watchdog list, True is returned, if not, False is returned).
	"""
	# def watchdogs_remove_all_items_from_watchdogs_list(self):
	# 	if self.base_get_state(self.watchdog_item, self.watchdog_text_all_items_removed_from_watchdog_list):
	# 		while self.base_is_visible(self.watchdog_item_remove_button, 1):
	# 			self.base_click(self.watchdog_item_remove_button)
	# 			self.base_click(self.watchdog_item_removal_confirmation_button)
	# 			self.base_is_invisible(self.watchdog_remove_question_dialog)

	def watchdogs_get_watchdog_item_name(self):
		if self.base_is_visible(self.watchdog_item):
			watchdog_item_name = self.base_get_element_text(self.watchdog_item)
			return watchdog_item_name

	def watchdogs_get_price_limit_provided(self):
		if self.base_is_visible(self.watchdog_price_limit_provided):
			watchdog_price_limit = self.base_get_element_attribute_value(self.watchdog_price_limit_provided, "value")
			watchdog_price_limit = watchdog_price_limit.replace(",-", "")
			return watchdog_price_limit

	def watchdogs_check_alert_price_is_checked(self):
		flag = self.base_is_visible(self.watchdog_checked_alert_price_checkbox, 1)
		return flag

	def watchdogs_get_text_once_all_items_removed(self):
		if self.base_is_visible(self.watchdog_text_all_items_removed_from_watchdog_list):
			all_items_removed_message = self.base_get_element_text(self.watchdog_text_all_items_removed_from_watchdog_list)
			return all_items_removed_message
