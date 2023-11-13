from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from Config.test_data import TestData
from Page_objects.base_page import BasePage


class DeliveryAddresses(BasePage):
	# Identification of objects on delivery addresses page.
	delivery_address_item = (By.XPATH, "//div[@data-testid='address']")
	delivery_address_first_item_remove_button = (By.XPATH, "//div[@data-testid='address'][1]//button[@data-testid='button-deleteAddress']")
	delivery_address_item_removal_confirmation_button = (By.XPATH, "//button[contains(@class, 'green')]")
	delivery_address_remove_question_dialog = (By.XPATH, "//div[@role='dialog']")
	delivery_address_add_new_address_button = (By.XPATH, "//button[@data-testid='button-addAddress']")
	delivery_address_add_dialog_name_surname_input = (By.NAME, "name")
	delivery_address_add_dialog_street_input = (By.NAME, "street")
	delivery_address_add_dialog_zip_input = (By.NAME, "zip")
	delivery_address_add_dialog_cíty_input = (By.NAME, "city")
	delivery_address_add_dialog_save_button = (By.XPATH, "//button[@data-testid='button-submit']")
	delivery_address_name_text = (By.XPATH, "//span[@data-testid='name']")
	delivery_address_street_and_number_text = (By.XPATH, "//span[@data-testid='street']")
	delivery_address_zip_and_city_text = (By.XPATH, "//span[@data-testid='postCodeAndCityContainer']")

	# Initialization.
	def __init__(self, driver):
		super().__init__(driver)

	# Actions on delivery addresses page.
	def delivery_addresses_remove_all_items(self):
		if self.base_is_visible(self.delivery_address_item, 3):
			while self.base_is_visible(self.delivery_address_first_item_remove_button, 1):
				self.base_click(self.delivery_address_first_item_remove_button)
				self.base_click(self.delivery_address_item_removal_confirmation_button)
				self.base_is_invisible(self.delivery_address_remove_question_dialog)

	def delivery_addresses_add_2_addresses(self):
		for data in TestData.delivery_addresses:
			self.base_click(self.delivery_address_add_new_address_button)
			self.base_send_keys(self.delivery_address_add_dialog_name_surname_input, data["name surname"])
			self.base_send_keys(self.delivery_address_add_dialog_street_input, data["street and number"])
			self.base_send_keys(self.delivery_address_add_dialog_zip_input, data["zip"])
			self.base_send_keys(self.delivery_address_add_dialog_cíty_input, data["city"])
			self.base_click(self.delivery_address_add_dialog_save_button)

	def delivery_addresses_get_number_of_addresses(self):
		number_of_addresses = self.base_get_number_of_elements(self.delivery_address_item)
		return number_of_addresses

	def delivery_addresses_get_addresses_data(self, number_of_addresses):
		delivery_addresses = []
		# Get name and surname, street and number, zip and city for all delivery addresses.
		addresses_names_surnames = self.base_get_multiple_elements_text(self.delivery_address_name_text)
		addresses_street_and_number = self.base_get_multiple_elements_text(self.delivery_address_street_and_number_text)
		addresses_zip_and_city = self.base_get_multiple_elements_text(self.delivery_address_zip_and_city_text)
		# Fill list with dictionary per delivery address with data so that it is similar to the list in TestData and return it.
		for index in range(number_of_addresses):
			address = {}
			delivery_addresses.append(address)
			delivery_addresses[index]["name surname"] = addresses_names_surnames[index]
			delivery_addresses[index]["street and number"] = addresses_street_and_number[index]
			zip_city = addresses_zip_and_city[index]
			zip_city = str(zip_city).split()
			delivery_addresses[index]["zip"] = zip_city[0]
			delivery_addresses[index]["city"] = zip_city[1]
		return delivery_addresses






