from selenium.webdriver.common.by import By
from element_handler import ElementHandler
from Tests.test_data import delivery_addresses_edited


class DeliveryAddressesDetails(ElementHandler):

	# Identification of elements on delivery addresses details dialog.
	name_surname_input = {
		"locator": (By.NAME, "name"),
		"name": "'Jméno a příjmení' input field"
	}
	street_input = {
		"locator": (By.NAME, "street"),
		"name": "'Ulice a číslo popisné' input field"
	}
	zip_input = {
		"locator": (By.NAME, "zip"),
		"name": "'PSČ' input field"
	}
	city_input = {
		"locator": (By.NAME, "city"),
		"name": "'Město' input field"
	}
	phone_input = {
		"locator": (By.NAME, "phone"),
		"name": "'Telefon' input field"
	}
	save_button = {
		"locator": (By.CSS_SELECTOR, "[data-testid='button-submit']"),
		"name": "'Uložit' button at delivery address details dialog"
	}

	# Actions on delivery addresses details dialog.
	def fill_in_new_address_details(self, data):
		self.element_handler_send_keys(self.name_surname_input["locator"], data["name surname"], self.name_surname_input["name"], True)
		self.element_handler_send_keys(self.street_input["locator"], data["street and number"], self.street_input["name"], True)
		self.element_handler_send_keys(self.zip_input["locator"], data["zip"], self.zip_input["name"], True)
		self.element_handler_send_keys(self.city_input["locator"], data["city"], self.city_input["name"], True)
		self.element_handler_send_keys(self.phone_input["locator"], data["phone"], self.phone_input["name"], True)
		self.element_handler_click(self.save_button["locator"], self.save_button["name"], True)
		self.element_handler_is_invisible(self.save_button["locator"], self.save_button["name"])

	def edit_address_details(self, index):
		self.element_handler_clear_input_by_pressing_backspace(self.name_surname_input["locator"], "value", self.name_surname_input["name"], True)
		self.element_handler_send_keys(self.name_surname_input["locator"], delivery_addresses_edited[index]["name surname"], self.name_surname_input["name"], True)
		self.element_handler_clear_input_by_pressing_backspace(self.street_input["locator"], "value", self.street_input["name"], True)
		self.element_handler_send_keys(self.street_input["locator"], delivery_addresses_edited[index]["street and number"], self.street_input["name"], True)
		self.element_handler_clear_input_by_pressing_backspace(self.zip_input["locator"], "value", self.zip_input["name"], True)
		self.element_handler_send_keys(self.zip_input["locator"], delivery_addresses_edited[index]["zip"], self.zip_input["name"], True)
		self.element_handler_clear_input_by_pressing_backspace(self.city_input["locator"], "value", self.city_input["name"], True)
		self.element_handler_send_keys(self.city_input["locator"], delivery_addresses_edited[index]["city"], self.city_input["name"], True)
		self.element_handler_clear_input_by_pressing_backspace(self.phone_input["locator"], "value", self.phone_input["name"], True)
		self.element_handler_send_keys(self.phone_input["locator"], delivery_addresses_edited[index]["phone"], self.phone_input["name"], True)
		self.element_handler_click(self.save_button["locator"], self.save_button["name"], True)
