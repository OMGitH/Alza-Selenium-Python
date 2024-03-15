from selenium.webdriver.common.by import By
from element_handler import ElementHandler
from Tests.test_data import delivery_addresses_edited


class DeliveryAddressesDetails(ElementHandler):

	# Identification of elements on delivery addresses details dialog.
	name_surname_input = (By.NAME, "name")
	street_input = (By.NAME, "street")
	zip_input = (By.NAME, "zip")
	city_input = (By.NAME, "city")
	phone_input = (By.NAME, "phone")
	save_button = (By.CSS_SELECTOR, "[data-testid='button-submit']")

	# Actions on delivery addresses details dialog.
	def fill_in_new_address_details(self, data):
		self.element_handler_send_keys(self.name_surname_input, data["name surname"], "'Jméno a příjmení' input field", True)
		self.element_handler_send_keys(self.street_input, data["street and number"], "'Ulice a číslo popisné' input field", True)
		self.element_handler_send_keys(self.zip_input, data["zip"], "'PSČ' input field", True)
		self.element_handler_send_keys(self.city_input, data["city"], "'Město' input field", True)
		self.element_handler_send_keys(self.phone_input, data["phone"], "'Telefon' input field", True)
		self.element_handler_click(self.save_button, "'Uložit' button", True)
		self.element_handler_is_invisible(self.save_button)

	def edit_address_details(self, index):
		self.element_handler_clear_input_by_pressing_backspace(self.name_surname_input, "value", "'Jméno a příjmení' input field", True)
		self.element_handler_send_keys(self.name_surname_input, delivery_addresses_edited[index]["name surname"], "'Jméno a příjmení' input field", True)
		self.element_handler_clear_input_by_pressing_backspace(self.street_input, "value", "'Ulice a číslo popisné' input field", True)
		self.element_handler_send_keys(self.street_input, delivery_addresses_edited[index]["street and number"], "'Ulice a číslo popisné' input field", True)
		self.element_handler_clear_input_by_pressing_backspace(self.zip_input, "value", "'PSČ' input field", True)
		self.element_handler_send_keys(self.zip_input, delivery_addresses_edited[index]["zip"], "'PSČ' input field", True)
		self.element_handler_clear_input_by_pressing_backspace(self.city_input, "value", "'Město' input field", True)
		self.element_handler_send_keys(self.city_input, delivery_addresses_edited[index]["city"], "'Město' input field", True)
		self.element_handler_clear_input_by_pressing_backspace(self.phone_input, "value", "'Telefon' input field", True)
		self.element_handler_send_keys(self.phone_input, delivery_addresses_edited[index]["phone"], "'Telefon' input field", True)
		self.element_handler_click(self.save_button, "'Uložit' button", True)
