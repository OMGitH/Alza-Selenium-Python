from selenium.webdriver.common.by import By
from Page_Objects.base_page import BasePage
from Config.test_data import TestData


class DeliveryAddressesDetails(BasePage):

	# Identification of objects on delivery addresses details dialog.
	delivery_address_details_dialog_name_surname_input = (By.NAME, "name")
	delivery_address_details_dialog_street_input = (By.NAME, "street")
	delivery_address_details_dialog_zip_input = (By.NAME, "zip")
	delivery_address_details_dialog_city_input = (By.NAME, "city")
	delivery_address_details_dialog_save_button = (By.XPATH, "//button[@data-testid='button-submit']")

	# Initialization.
	def __init__(self, driver):
		super().__init__(driver)

	# Actions on delivery addresses details dialog.
	def delivery_address_details_dialog_fill_in_new_address_details(self, data):
		self.base_send_keys(self.delivery_address_details_dialog_name_surname_input, data["name surname"])
		self.base_send_keys(self.delivery_address_details_dialog_street_input, data["street and number"])
		self.base_send_keys(self.delivery_address_details_dialog_zip_input, data["zip"])
		self.base_send_keys(self.delivery_address_details_dialog_city_input, data["city"])
		self.base_click(self.delivery_address_details_dialog_save_button)
		self.base_is_invisible(self.delivery_address_details_dialog_save_button)

	def delivery_address_details_dialog_edit_address_details(self, index):
		self.base_clear_input_by_pressing_backspace(self.delivery_address_details_dialog_name_surname_input, "value")
		self.base_send_keys(self.delivery_address_details_dialog_name_surname_input, TestData.delivery_addresses_edited[index]["name surname"])
		self.base_clear_input_by_pressing_backspace(self.delivery_address_details_dialog_street_input, "value")
		self.base_send_keys(self.delivery_address_details_dialog_street_input, TestData.delivery_addresses_edited[index]["street and number"])
		self.base_clear_input_by_pressing_backspace(self.delivery_address_details_dialog_zip_input, "value")
		self.base_send_keys(self.delivery_address_details_dialog_zip_input, TestData.delivery_addresses_edited[index]["zip"])
		self.base_clear_input_by_pressing_backspace(self.delivery_address_details_dialog_city_input, "value")
		self.base_send_keys(self.delivery_address_details_dialog_city_input, TestData.delivery_addresses_edited[index]["city"])
		self.base_click(self.delivery_address_details_dialog_save_button)
