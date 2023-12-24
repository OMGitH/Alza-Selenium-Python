from selenium.webdriver.common.by import By
from object_handler import ObjectHandler
from test_data import TestData


class DeliveryAddressesDetails(ObjectHandler):

	# Identification of objects on delivery addresses details dialog.
	name_surname_input = (By.NAME, "name")
	street_input = (By.NAME, "street")
	zip_input = (By.NAME, "zip")
	city_input = (By.NAME, "city")
	save_button = (By.XPATH, "//button[@data-testid='button-submit']")

	# Initialization.
	def __init__(self, driver):
		super().__init__(driver)

	# Actions on delivery addresses details dialog.
	def fill_in_new_address_details(self, data):
		self.object_handler_send_keys(self.name_surname_input, data["name surname"], "'Jméno a příjmení' input field", True)
		self.object_handler_send_keys(self.street_input, data["street and number"], "'Ulice a číslo popisné' input field", True)
		self.object_handler_send_keys(self.zip_input, data["zip"], "'PSČ' input field", True)
		self.object_handler_send_keys(self.city_input, data["city"], "'Město' input field", True)
		self.object_handler_click(self.save_button, "'Uložit' button", True)
		self.object_handler_is_invisible(self.save_button)

	def edit_address_details(self, index):
		self.object_handler_clear_input_by_pressing_backspace(self.name_surname_input, "value", "'Jméno a příjmení' input field", True)
		self.object_handler_send_keys(self.name_surname_input, TestData.delivery_addresses_edited[index]["name surname"], "'Jméno a příjmení' input field", True)
		self.object_handler_clear_input_by_pressing_backspace(self.street_input, "value", "'Ulice a číslo popisné' input field", True)
		self.object_handler_send_keys(self.street_input, TestData.delivery_addresses_edited[index]["street and number"], "'Ulice a číslo popisné' input field", True)
		self.object_handler_clear_input_by_pressing_backspace(self.zip_input, "value", "'PSČ' input field", True)
		self.object_handler_send_keys(self.zip_input, TestData.delivery_addresses_edited[index]["zip"], "'PSČ' input field", True)
		self.object_handler_clear_input_by_pressing_backspace(self.city_input, "value", "'Město' input field", True)
		self.object_handler_send_keys(self.city_input, TestData.delivery_addresses_edited[index]["city"], "'Město' input field", True)
		self.object_handler_click(self.save_button, "'Uložit' button", True)
