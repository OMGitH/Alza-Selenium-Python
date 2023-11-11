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