from selenium.webdriver.common.by import By
from object_handler import ObjectHandler
import time


class DeliveryAddresses(ObjectHandler):

	# Identification of objects on delivery addresses page.
	delivery_address_item = (By.XPATH, "//div[@data-testid='address']")
	without_delivery_address_items = (By.XPATH, "//div[@data-testid='deliveryAddressesRoot'][not(descendant::div[@data-testid='address'])]")
	delivery_address_remove_button = (By.XPATH, "//button[@data-testid='button-deleteAddress']")
	delivery_address_removal_confirmation_button = (By.XPATH, "//button[contains(@class, 'green')]")
	remove_question_dialog = (By.XPATH, "//div[@role='dialog']")
	name_text = (By.XPATH, "//span[@data-testid='name']")
	street_and_number_text = (By.XPATH, "//span[@data-testid='street']")
	zip_and_city_text = (By.XPATH, "//span[@data-testid='postCodeAndCityContainer']")
	add_new_delivery_address_button = (By.XPATH, "//button[@data-testid='button-addAddress']")

	# Initialization.
	def __init__(self, driver):
		super().__init__(driver)

	# Actions on delivery addresses page.
	def remove_all_addresses_from_delivery_addresses_list(self, number_of_checks=10, check_wait=0.5):
		while self.object_handler_is_visible(self.delivery_address_remove_button, 2, True):
			number_of_addresses = self.object_handler_get_number_of_visible_elements(self.delivery_address_remove_button)
			self.object_handler_click(self.delivery_address_remove_button, True)
			self.object_handler_click(self.delivery_address_removal_confirmation_button)
			self.object_handler_is_invisible(self.remove_question_dialog)
			# It seems delivery addresses page UI is slow and not refreshed fast enough, following code waits for page to get refreshed.
			if number_of_addresses != 0:
				for check in range(number_of_checks):
					number_of_addresses_after_removal = self.object_handler_get_number_of_visible_elements(self.delivery_address_remove_button)
					if number_of_addresses_after_removal == 0 or number_of_addresses_after_removal == number_of_addresses - 1:
						break
					time.sleep(check_wait)

	# def delivery_addresses_remove_all_items_from_delivery_addresses_list(self, number_of_checks=10, check_wait=0.5):
	# 	if self.base_is_visible(self.delivery_address_item, 3, True):
	# 		while self.base_is_visible(self.delivery_address_remove_button, 1, True):
	# 			number_of_items = self.base_get_number_of_visible_elements(self.delivery_address_remove_button)
	# 			self.base_click(self.delivery_address_remove_button, True)
	# 			self.base_click(self.delivery_address_removal_confirmation_button)
	# 			self.base_is_invisible(self.remove_question_dialog)
	# 			# It seems delivery addresses page UI is slow and not refreshed fast enough, following code waits for it to get refreshed.
	# 			if number_of_items != 0:
	# 				for check in range(number_of_checks):
	# 					number_of_items_after_removal = self.base_get_number_of_visible_elements(self.delivery_address_remove_button)
	# 					if number_of_items_after_removal == 0 or number_of_items_after_removal == number_of_items - 1:
	# 						break
	# 					time.sleep(check_wait)

	"""
	Code below uses get state method that is faster as it doesn't wait for timeout to make sure whether or not there is an item
	identifying a state (if there is an address in delivery addresses list, True is returned, if not, False is returned).
	"""
	# def delivery_addresses_remove_all_items_from_delivery_addresses_list(self, number_of_checks=10, check_wait=0.5):
	# 	if self.base_get_state(self.delivery_address_item, self.without_delivery_address_items):
	# 		while self.base_is_visible(self.delivery_address_remove_button, 1):
	# 			number_of_items = self.base_get_number_of_elements(self.delivery_address_remove_button)
	# 			self.base_click(self.delivery_address_remove_button, True)
	# 			self.base_click(self.delivery_address_removal_confirmation_button)
	# 			self.base_is_invisible(self.remove_question_dialog)
	# 			# It seems delivery addresses page UI is slow and not refreshed fast enough, following code waits for it to get refreshed.
	# 			if number_of_items != 0:
	# 				for check in range(number_of_checks):
	# 					number_of_items_after_removal = self.base_get_number_of_elements(self.delivery_address_remove_button)
	# 					if number_of_items_after_removal == 0 or number_of_items_after_removal == number_of_items - 1:
	# 						break
	# 					time.sleep(check_wait)

	def click_add_new_address_button(self):
		self.object_handler_click(self.add_new_delivery_address_button)

	def get_number_of_addresses(self):
		number_of_addresses = self.object_handler_get_number_of_visible_elements(self.delivery_address_item)
		return number_of_addresses

	def get_addresses_data(self, number_of_addresses):
		delivery_addresses = []
		# Get name and surname, street and number, zip and city for all delivery addresses.
		addresses_names_surnames = self.object_handler_get_multiple_elements_text(self.name_text)
		addresses_street_and_number = self.object_handler_get_multiple_elements_text(self.street_and_number_text)
		addresses_zip_and_city = self.object_handler_get_multiple_elements_text(self.zip_and_city_text)
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

	def get_addresses(self):
		addresses = self.object_handler_get_multiple_visible_elements(self.delivery_address_item)
		return addresses

	def click_address_item_as_argument(self, address):
		self.object_handler_click(address)
