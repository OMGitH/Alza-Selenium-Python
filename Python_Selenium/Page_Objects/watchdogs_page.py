from selenium.webdriver.common.by import By
from object_handler import ObjectHandler


class Watchdogs(ObjectHandler):

	# Identification of objects on watchdogs page.
	item = (By.XPATH, "//div[@data-testid='page-watchDogs']//a")
	item_remove_button = (By.XPATH, "//div[@data-testid='page-watchDogs']//button")
	item_removal_confirmation_button = (By.XPATH, "//button[contains(@class, 'red')]")
	remove_question_dialog = (By.XPATH, "//div[@role='dialog']")
	price_limit_provided = (By.NAME, "price")
	alert_price_checkbox_checked = (By.XPATH, "//input[not (@name)]/parent::span/*[name()='svg']/*[name()='g' and @transform]")
	all_items_removed_from_watchdogs_page_text = (By.XPATH, "//div[@data-testid='noResults']/span")
	success_add_note_close_button = (By.XPATH, "//*[name()='svg' and contains(@class, 'priceBoxProcessorProxy')]/*[name()='path']")
	success_remove_note_close_button = (By.XPATH, "//div[contains(@class, 'react-page')]//*[name()='svg' and @xmlns]")

	# Initialization.
	def __init__(self, driver):
		super().__init__(driver)

	# Actions on watchdogs page.
	def remove_all_items_from_watchdogs_page(self):
		while self.object_handler_get_state(self.item_remove_button, self.all_items_removed_from_watchdogs_page_text) == self.item_remove_button:
			self.object_handler_click(self.item_remove_button, "'X' button to remove item from watchdogs", True)
			self.object_handler_click(self.item_removal_confirmation_button, "'Zrušit hlídání' button", True)
			self.object_handler_is_invisible(self.remove_question_dialog)
			self.object_handler_click(self.success_remove_note_close_button, "'X' button at 'Hlídací pes smazán.' note", True)

	# def watchdogs_remove_all_items_from_watchdogs_page(self):
	# 	if self.base_is_visible(self.item, 3, True):
	# 		while self.base_is_visible(self.item_remove_button, 1, True):
	# 			self.base_click(self.item_remove_button)
	# 			self.base_click(self.item_removal_confirmation_button)
	# 			self.base_is_invisible(self.remove_question_dialog)

	"""
	Code below uses get state method that is faster as it doesn't wait for timeout to make sure whether or not there is an item
	identifying a state (if there is an item in watchdogs page, True is returned, if not, False is returned).
	"""
	# def watchdogs_remove_all_items_from_watchdogs_page(self):
	# 	if self.base_get_state(self.item, self.all_items_removed_from_watchdogs_page_text):
	# 		while self.base_is_visible(self.item_remove_button, 1):
	# 			self.base_click(self.item_remove_button)
	# 			self.base_click(self.item_removal_confirmation_button)
	# 			self.base_is_invisible(self.remove_question_dialog)

	def get_watchdog_item_name(self):
		if self.object_handler_is_visible(self.item):
			watchdog_item_name = self.object_handler_get_element_text(self.item)
			return watchdog_item_name

	def get_price_limit_provided(self):
		if self.object_handler_is_visible(self.price_limit_provided):
			watchdog_price_limit = self.object_handler_get_element_attribute_value(self.price_limit_provided, "value")
			watchdog_price_limit = watchdog_price_limit.replace(",-", "")
			return watchdog_price_limit

	def check_alert_price_is_checked(self):
		flag = self.object_handler_is_visible(self.alert_price_checkbox_checked, handle_TimeoutException=True)
		return flag

	def get_text_once_all_items_removed(self):
		if self.object_handler_is_visible(self.all_items_removed_from_watchdogs_page_text):
			all_items_removed_message = self.object_handler_get_element_text(self.all_items_removed_from_watchdogs_page_text)
			return all_items_removed_message

	def close_success_note(self):
		self.object_handler_click(self.success_add_note_close_button, "'X' button at 'Hlídací pes nastaven.' note", True)
