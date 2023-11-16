from selenium.webdriver.common.by import By
from Config.test_data import TestData
from Page_objects.base_page import BasePage
import time


class DeliveryAddresses(BasePage):
	# Identification of objects on delivery addresses page.
	delivery_address_item = (By.XPATH, "//div[@data-testid='address']")
	delivery_address_without_items = (By.XPATH, "//div[@data-testid='addressesContainer'][not(div)]")
	delivery_address_item_remove_button = (By.XPATH, "//button[@data-testid='button-deleteAddress']")
	delivery_address_item_removal_confirmation_button = (By.XPATH, "//button[contains(@class, 'green')]")
	delivery_address_remove_question_dialog = (By.XPATH, "//div[@role='dialog']")
	delivery_address_name_text = (By.XPATH, "//span[@data-testid='name']")
	delivery_address_street_and_number_text = (By.XPATH, "//span[@data-testid='street']")
	delivery_address_zip_and_city_text = (By.XPATH, "//span[@data-testid='postCodeAndCityContainer']")
	delivery_address_add_new_address_button = (By.XPATH, "//button[@data-testid='button-addAddress']")
	delivery_address_add_dialog_name_surname_input = (By.NAME, "name")
	delivery_address_add_dialog_street_input = (By.NAME, "street")
	delivery_address_add_dialog_zip_input = (By.NAME, "zip")
	delivery_address_add_dialog_cíty_input = (By.NAME, "city")
	delivery_address_add_dialog_save_button = (By.XPATH, "//button[@data-testid='button-submit']")

	# Initialization.
	def __init__(self, driver):
		super().__init__(driver)

	# Actions on delivery addresses page.
	def delivery_addresses_remove_all_items_from_delivery_addresses_list(self, number_of_checks=10, check_wait=0.5):
		if self.base_is_visible(self.delivery_address_item, 3, True):
			while self.base_is_visible(self.delivery_address_item_remove_button, 1, True):
				number_of_items = self.base_get_number_of_visible_elements(self.delivery_address_item_remove_button)
				self.base_click(self.delivery_address_item_remove_button, True)
				self.base_click(self.delivery_address_item_removal_confirmation_button)
				self.base_is_invisible(self.delivery_address_remove_question_dialog)
				# It seems delivery addresses page UI is slow and not refreshed fast enough, following code waits for it to get refreshed.
				if number_of_items != 0:
					for check in range(number_of_checks):
						number_of_items_after_removal = self.base_get_number_of_visible_elements(self.delivery_address_item_remove_button)
						if number_of_items_after_removal == 0 or number_of_items_after_removal == number_of_items - 1:
							break
						time.sleep(check_wait)

	"""
	Code below uses get state method that is faster as it doesn't wait for timeout to make sure whether or not there is an item
	identifying a state (if there is an address in delivery addresses list, True is returned, if not, False is returned).
	"""
	# def delivery_addresses_remove_all_items_from_delivery_addresses_list(self, number_of_checks=10, check_wait=0.5):
	# 	if self.base_get_state(self.delivery_address_item, self.delivery_address_without_items):
	# 		while self.base_is_visible(self.delivery_address_item_remove_button, 1):
	# 			number_of_items = self.base_get_number_of_elements(self.delivery_address_item_remove_button)
	# 			self.base_click(self.delivery_address_item_remove_button, True)
	# 			self.base_click(self.delivery_address_item_removal_confirmation_button)
	# 			self.base_is_invisible(self.delivery_address_remove_question_dialog)
	# 			# It seems delivery addresses page UI is slow and not refreshed fast enough, following code waits for it to get refreshed.
	# 			if number_of_items != 0:
	# 				for check in range(number_of_checks):
	# 					number_of_items_after_removal = self.base_get_number_of_elements(self.delivery_address_item_remove_button)
	# 					if number_of_items_after_removal == 0 or number_of_items_after_removal == number_of_items - 1:
	# 						break
	# 					time.sleep(check_wait)

	def delivery_addresses_add_addresses(self):
		for data in TestData.delivery_addresses_original:
			self.base_click(self.delivery_address_add_new_address_button)
			self.base_send_keys(self.delivery_address_add_dialog_name_surname_input, data["name surname"])
			self.base_send_keys(self.delivery_address_add_dialog_street_input, data["street and number"])
			self.base_send_keys(self.delivery_address_add_dialog_zip_input, data["zip"])
			self.base_send_keys(self.delivery_address_add_dialog_cíty_input, data["city"])
			self.base_click(self.delivery_address_add_dialog_save_button)
			self.base_is_invisible(self.delivery_address_add_dialog_save_button)

	def delivery_addresses_get_number_of_addresses(self):
		number_of_addresses = self.base_get_number_of_visible_elements(self.delivery_address_item)
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

	def delivery_addresses_edit_addresses(self):
		addresses = self.base_get_multiple_visible_elements(self.delivery_address_item)
		for index, address in enumerate(addresses):
			self.base_click(address)
			self.base_clear_input_by_pressing_backspace(self.delivery_address_add_dialog_name_surname_input, "value")
			self.base_send_keys(self.delivery_address_add_dialog_name_surname_input, TestData.delivery_addresses_edited[index]["name surname"])
			self.base_clear_input_by_pressing_backspace(self.delivery_address_add_dialog_street_input, "value")
			self.base_send_keys(self.delivery_address_add_dialog_street_input, TestData.delivery_addresses_edited[index]["street and number"])
			self.base_clear_input_by_pressing_backspace(self.delivery_address_add_dialog_zip_input, "value")
			self.base_send_keys(self.delivery_address_add_dialog_zip_input, TestData.delivery_addresses_edited[index]["zip"])
			self.base_clear_input_by_pressing_backspace(self.delivery_address_add_dialog_cíty_input, "value")
			self.base_send_keys(self.delivery_address_add_dialog_cíty_input, TestData.delivery_addresses_edited[index]["city"])
			self.base_click(self.delivery_address_add_dialog_save_button)
