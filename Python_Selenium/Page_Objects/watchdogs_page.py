from selenium.webdriver.common.by import By
from element_handler import ElementHandler
from report_logger import logger
from Tests.test_data import text_once_all_items_removed_from_watchdogs_page


class Watchdogs(ElementHandler):

	# Identification of elements on watchdogs page.
	item_name_link = {
		"locator": (By.CSS_SELECTOR, "[data-testid='page-watchDogs'] a"),
		"name": "Item name link at watchdogs page"
	}
	item_remove_button = {
		"locator": (By.CSS_SELECTOR, "[data-testid='page-watchDogs'] button"),
		"name": "'X' button to remove item from watchdogs"
	}
	item_removal_confirmation_button = {
		"locator": (By.CSS_SELECTOR, "button[class*='red']"),
		"name": "'Zrušit hlídání' button"
	}
	remove_question_dialog = {
		"locator": (By.CSS_SELECTOR, "div[role='dialog']"),
		"name": "Watchdog remove question dialog"
	}
	item_price_limit_input = {
		"locator": (By.NAME, "price"),
		"name": "'Při snížení ceny pod' input field"
	}
	item_alert_price_checkbox_checked = {
		"locator": (By.XPATH, "//input[not(@name)]/following-sibling::*[name()='svg']/*[name()='g' and @transform]"),
		"name": "Checked 'Při snížení ceny pod' checkbox"
	}
	all_items_removed_from_watchdogs_page_text = {
		"locator": (By.CSS_SELECTOR, "[data-testid='noResults'] span"),
		"name": f"Text when watchdogs page is empty '{text_once_all_items_removed_from_watchdogs_page}'"
	}
	watchdog_success_remove_note_close_button = {
		"locator": (By.CSS_SELECTOR, "svg[class*='reactPage'][xmlns]"),
		"name": "'X' button at 'Hlídací pes smazán.' note"
	}

	# Actions on watchdogs page.
	def remove_all_items_from_watchdogs_page(self):
		removed_watchdogs = 0
		while self.element_handler_get_state(self.item_remove_button["locator"], self.all_items_removed_from_watchdogs_page_text["locator"]) == self.item_remove_button["locator"]:
			self.element_handler_click(self.item_remove_button["locator"], self.item_remove_button["name"], True)
			self.element_handler_click(self.item_removal_confirmation_button["locator"], self.item_removal_confirmation_button["name"], True)
			self.element_handler_is_invisible(self.remove_question_dialog["locator"], self.remove_question_dialog["name"])
			self.element_handler_click(self.watchdog_success_remove_note_close_button["locator"], self.watchdog_success_remove_note_close_button["name"], True)
			self.element_handler_is_invisible(self.watchdog_success_remove_note_close_button["locator"], self.watchdog_success_remove_note_close_button["name"])
			removed_watchdogs += 1
		if removed_watchdogs == 0:
			logger.info("\t- Nothing removed as there are no watchdogs.")
		else:
			logger.info(f"\t- {removed_watchdogs} watchdog(s) removed.")

	def get_watchdog_item_name(self):
		watchdog_item_name = self.element_handler_get_element_text(self.item_name_link["locator"], f"Text of {self.item_name_link["name"]}")
		return watchdog_item_name

	def get_price_limit_provided(self):
		watchdog_price_limit = self.element_handler_get_element_attribute(self.item_price_limit_input["locator"], "value", self.item_price_limit_input["name"])
		watchdog_price_limit = watchdog_price_limit.replace(",-", "")
		return watchdog_price_limit

	def check_alert_price_is_checked(self):
		flag = self.element_handler_is_visible(self.item_alert_price_checkbox_checked["locator"], self.item_alert_price_checkbox_checked["name"], handle_timeout_exception=True)
		return flag

	def get_text_once_all_items_removed(self):
		all_items_removed_message = self.element_handler_get_element_text(self.all_items_removed_from_watchdogs_page_text["locator"], self.all_items_removed_from_watchdogs_page_text["name"])
		return all_items_removed_message
