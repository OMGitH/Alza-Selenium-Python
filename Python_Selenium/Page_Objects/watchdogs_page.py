from selenium.webdriver.common.by import By
from element_handler import ElementHandler
from report_logger import logger
from Tests.test_data import text_once_all_items_removed_from_watchdogs_page


class Watchdogs(ElementHandler):

	# Identification of elements on watchdogs page.
	item_name_link = (By.CSS_SELECTOR, "[data-testid='page-watchDogs'] a")
	item_remove_button = (By.CSS_SELECTOR, "[data-testid='page-watchDogs'] button")
	item_removal_confirmation_button = (By.CSS_SELECTOR, "button[class*='red']")
	remove_question_dialog = (By.CSS_SELECTOR, "div[role='dialog']")
	item_price_limit_input = (By.NAME, "price")
	item_alert_price_checkbox_checked = (By.XPATH, "//input[not(@name)]/following-sibling::*[name()='svg']/*[name()='g' and @transform]")
	all_items_removed_from_watchdogs_page_text = (By.CSS_SELECTOR, "[data-testid='noResults'] span")
	watchdog_success_remove_note_close_button = (By.CSS_SELECTOR, "svg[class*='reactPage'][xmlns]")

	# Actions on watchdogs page.
	def remove_all_items_from_watchdogs_page(self):
		removed_watchdogs = 0
		while self.element_handler_get_state(self.item_remove_button, self.all_items_removed_from_watchdogs_page_text) == self.item_remove_button:
			self.element_handler_click(self.item_remove_button, "'X' button to remove item from watchdogs", True)
			self.element_handler_click(self.item_removal_confirmation_button, "'Zrušit hlídání' button", True)
			self.element_handler_is_invisible(self.remove_question_dialog, "Watchdog remove question dialog")
			self.element_handler_click(self.watchdog_success_remove_note_close_button, "'X' button at 'Hlídací pes smazán.' note", True)
			self.element_handler_is_invisible(self.watchdog_success_remove_note_close_button, "'X' button at 'Hlídací pes smazán.' note")
			removed_watchdogs += 1
		if removed_watchdogs == 0:
			logger.info("\t- Nothing removed as there are no watchdogs.")
		else:
			logger.info(f"\t- {removed_watchdogs} watchdog(s) removed.")

	def get_watchdog_item_name(self):
		watchdog_item_name = self.element_handler_get_element_text(self.item_name_link, "Item name link text at watchdogs page")
		return watchdog_item_name

	def get_price_limit_provided(self):
		watchdog_price_limit = self.element_handler_get_element_attribute(self.item_price_limit_input, "value", "'Při snížení ceny pod' input field value")
		watchdog_price_limit = watchdog_price_limit.replace(",-", "")
		return watchdog_price_limit

	def check_alert_price_is_checked(self):
		flag = self.element_handler_is_visible(self.item_alert_price_checkbox_checked, "Checked alert price checkbox", handle_timeout_exception=True)
		return flag

	def get_text_once_all_items_removed(self):
		all_items_removed_message = self.element_handler_get_element_text(self.all_items_removed_from_watchdogs_page_text, f"Text when watchdogs page is empty '{text_once_all_items_removed_from_watchdogs_page}'")
		return all_items_removed_message
