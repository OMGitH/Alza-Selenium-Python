from time import sleep
from selenium.webdriver.common.by import By
from element_handler import ElementHandler
from report_logger import logger


class DeliveryAddresses(ElementHandler):

	# Identification of elements on delivery addresses page.
	delivery_address_item = {
		"locator": (By.CSS_SELECTOR, "[data-testid='address']"),
		"name": "Delivery address item"
	}
	delivery_address_remove_button = {
		"locator": (By.CSS_SELECTOR, "[data-testid='button-deleteAddress']"),
		"name": "'X' button to remove address from delivery addresses"
	}
	delivery_address_removal_confirmation_button = {
		"locator": (By.CSS_SELECTOR, "button.green"),
		"name": "'Smazat' button at delivery address remove question dialog"
	}
	remove_question_dialog = {
		"locator": (By.CSS_SELECTOR, "div[role='dialog']"),
		"name": "Delivery address remove question dialog"
	}
	name_and_surname_text = {
		"locator": (By.CSS_SELECTOR, "[data-testid='name']"),
		"name": "Names and surnames at all delivery addresses"
	}
	street_and_number_text = {
		"locator": (By.CSS_SELECTOR, "[data-testid='street']"),
		"name": "Streets and numbers at all delivery addresses"
	}
	zip_and_city_text = {
		"locator": (By.CSS_SELECTOR, "[data-testid='postCodeAndCityContainer']"),
		"name": "Zips and cities at all delivery addresses"
	}
	phone_text = {
		"locator": (By.CSS_SELECTOR, "[data-testid='phone']"),
		"name": "Phones at all delivery addresses"
	}
	add_new_delivery_address_button = {
		"locator": (By.CSS_SELECTOR, "[data-testid='button-addAddress']"),
		"name": "'Přidat novou adresu' button"
	}

	# Actions on delivery addresses page.
	def remove_all_addresses_from_delivery_addresses_page(self, number_of_checks=10, check_wait=0.5):
		removed_delivery_addresses = 0
		while self.element_handler_is_visible(self.delivery_address_remove_button["locator"], self.delivery_address_remove_button["name"], 2, True):
			number_of_addresses = self.element_handler_get_number_of_visible_elements(self.delivery_address_remove_button["locator"], self.delivery_address_remove_button["name"])
			self.element_handler_click(self.delivery_address_remove_button["locator"], self.delivery_address_remove_button["name"], True)
			self.element_handler_click(self.delivery_address_removal_confirmation_button["locator"], self.delivery_address_removal_confirmation_button["name"], True)
			self.element_handler_is_invisible(self.remove_question_dialog["locator"], self.remove_question_dialog["name"])
			removed_delivery_addresses += 1
			# It seems delivery addresses page UI is slow and not refreshed fast enough, following code waits for page to get refreshed.
			if number_of_addresses != 0:
				for _ in range(number_of_checks):
					number_of_addresses_after_removal = self.element_handler_get_number_of_visible_elements(self.delivery_address_remove_button["locator"], self.delivery_address_remove_button["name"])
					if number_of_addresses_after_removal == 0 or number_of_addresses_after_removal == number_of_addresses - 1:
						break
					sleep(check_wait)
		if removed_delivery_addresses == 0:
			logger.info("\t- Nothing removed as there are no delivery addresses.")
		else:
			logger.info(f"\t- {removed_delivery_addresses} delivery address(es) removed.")

	def click_add_new_address_button(self):
		self.element_handler_click(self.add_new_delivery_address_button["locator"], self.add_new_delivery_address_button["name"], True)

	def get_number_of_addresses(self):
		number_of_addresses = self.element_handler_get_number_of_visible_elements(self.delivery_address_item["locator"], self.delivery_address_item["name"])
		return number_of_addresses

	def get_addresses_data(self, number_of_addresses):
		delivery_addresses = []
		# Get name and surname, street and number, zip and city and phone for all delivery addresses.
		addresses_names_surnames = self.element_handler_get_multiple_elements_text(self.name_and_surname_text["locator"], self.name_and_surname_text["name"])
		addresses_street_and_number = self.element_handler_get_multiple_elements_text(self.street_and_number_text["locator"], self.street_and_number_text["name"])
		addresses_zip_and_city = self.element_handler_get_multiple_elements_text(self.zip_and_city_text["locator"], self.zip_and_city_text["name"])
		addresses_phones = self.element_handler_get_multiple_elements_text(self.phone_text["locator"], self.phone_text["name"])
		# Fill list with dictionary per delivery address with data so that it is similar to the list in test_data and return it.
		for index in range(number_of_addresses):
			address = {}
			delivery_addresses.append(address)
			delivery_addresses[index]["name surname"] = addresses_names_surnames[index]
			delivery_addresses[index]["street and number"] = addresses_street_and_number[index]
			zip_city = addresses_zip_and_city[index]
			zip_city = str(zip_city).split()
			delivery_addresses[index]["zip"] = zip_city[0]
			delivery_addresses[index]["city"] = zip_city[1]
			delivery_addresses[index]["phone"] = addresses_phones[index].replace(" ", "").replace("+420", "")
		return delivery_addresses

	def get_delivery_addresses(self):
		delivery_addresses = self.element_handler_get_multiple_visible_elements(self.delivery_address_item["locator"], self.delivery_address_item["name"])
		return delivery_addresses

	def click_delivery_address_item_as_argument(self, delivery_address):
		self.element_handler_click(delivery_address, "Delivery address tile", True)
