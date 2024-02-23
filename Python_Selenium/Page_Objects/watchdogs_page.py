from selenium.webdriver.common.by import By
from element_handler import ElementHandler
from report_logger import logger


class Watchdogs(ElementHandler):

	# Identification of elements on watchdogs page.
	item = (By.XPATH, "//div[@data-testid='page-watchDogs']//a")
	item_remove_button = (By.XPATH, "//div[@data-testid='page-watchDogs']//button")
	item_removal_confirmation_button = (By.XPATH, "//button[contains(@class, 'red')]")
	remove_question_dialog = (By.XPATH, "//div[@role='dialog']")
	price_limit_provided = (By.NAME, "price")
	alert_price_checkbox_checked = (By.XPATH, "//input[not (@name)]/parent::span/*[name()='svg']/*[name()='g' and @transform]")
	all_items_removed_from_watchdogs_page_text = (By.XPATH, "//div[@data-testid='noResults']/span")
	success_add_note_close_button = (By.XPATH, "//*[name()='svg' and contains(@class, 'priceBoxProcessorProxy')]/*[name()='path']")
	success_remove_note_close_button = (By.XPATH, "//div[contains(@class, 'react-page')]//*[name()='svg' and @xmlns]")

	# Actions on watchdogs page.
	def remove_all_items_from_watchdogs_page(self):
		removed_watchdogs = 0
		while self.element_handler_get_state(self.item_remove_button, self.all_items_removed_from_watchdogs_page_text) == self.item_remove_button:
			self.element_handler_click(self.item_remove_button, "'X' button to remove item from watchdogs", True)
			self.element_handler_click(self.item_removal_confirmation_button, "'Zrušit hlídání' button", True)
			self.element_handler_is_invisible(self.remove_question_dialog)
			self.element_handler_click(self.success_remove_note_close_button, "'X' button at 'Hlídací pes smazán.' note", True)
			self.element_handler_is_invisible(self.success_remove_note_close_button)
			removed_watchdogs += 1
		if removed_watchdogs == 0:
			logger.info("\t- Nothing removed as there are no watchdogs.")
		else:
			logger.info(f"\t- {removed_watchdogs} watchdog(s) removed.")

	def get_watchdog_item_name(self):
		if self.element_handler_is_visible(self.item):
			watchdog_item_name = self.element_handler_get_element_text(self.item)
			return watchdog_item_name

	def get_price_limit_provided(self):
		if self.element_handler_is_visible(self.price_limit_provided):
			watchdog_price_limit = self.element_handler_get_element_attribute_value(self.price_limit_provided, "value")
			watchdog_price_limit = watchdog_price_limit.replace(",-", "")
			return watchdog_price_limit

	def check_alert_price_is_checked(self):
		flag = self.element_handler_is_visible(self.alert_price_checkbox_checked, handle_timeout_exception=True)
		return flag

	def get_text_once_all_items_removed(self):
		if self.element_handler_is_visible(self.all_items_removed_from_watchdogs_page_text):
			all_items_removed_message = self.element_handler_get_element_text(self.all_items_removed_from_watchdogs_page_text)
			return all_items_removed_message

	def close_success_add_note(self):
		self.element_handler_click(self.success_add_note_close_button, "'X' button at 'Hlídací pes nastaven.' note", True)
		self.element_handler_is_invisible(self.success_add_note_close_button)
