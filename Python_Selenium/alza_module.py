import mixed_assertions as mixed_assert
from Page_Objects.basket_page import Basket
from Page_Objects.cookies_pane import CookiesPane
from Page_Objects.delivery_addresses_details_dialog import DeliveryAddressesDetails
from Page_Objects.delivery_addresses_page import DeliveryAddresses
from Page_Objects.login_page import LoginPage
from Page_Objects.main_page import MainPage
from Page_Objects.my_account_page import MyAccount
from Page_Objects.top_section import TopSection
from Page_Objects.watchdogs_page import Watchdogs
from Tests.test_data import user_name, password, user_signed_in_text, delivery_addresses_original
from report_logger import logger


class AlzaModule:
	"""Additional layer in which various methods can be defined, for example those used in more tests, that are just preconditions for test
	or which combine more page objects. Can serve also for extraction of complexity from test level.
	"""
	# Initialization.
	def __init__(self, driver):
		self.driver = driver
		self.login_page = LoginPage(self.driver)
		self.cookies_pane = CookiesPane(self.driver)
		self.top_section = TopSection(self.driver)
		self.basket_page = Basket(self.driver)
		self.my_account_page = MyAccount(self.driver)
		self.watchdogs_page = Watchdogs(self.driver)
		self.delivery_addresses_page = DeliveryAddresses(self.driver)
		self.delivery_addresses_details_dialog = DeliveryAddressesDetails(self.driver)
		self.main_page = MainPage(self.driver)

	# Methods:
	# Reject all cookies.
	def reject_all_cookies(self):
		self.cookies_pane.click_reject_all_button()
		self.main_page.main_page_loaded_after_cookies_rejected()

	# Login and logout:
	def reject_all_cookies_and_login(self, driver, report_screenshots_folder, tmp_test_urls_file_path, interrupt_test=False):
		# Reject all cookies.
		self.reject_all_cookies()
		self.cookies_pane.cookies_pane_is_invisible()
		# Log into application:
		# Click login link.
		self.top_section.click_login_link()
		# Fill in credentials and login.
		self.login_page.successful_login(user_name, password)
		# Check successful login.
		mixed_assert.is_true(self.login_page.login_dialog_is_invisible(), "Login dialog is correctly invisible.", "Login dialog is still visible but shall not be.", driver, report_screenshots_folder, tmp_test_urls_file_path, interrupt_test)
		actual_signed_in_text = self.top_section.get_signed_in_user_text()
		mixed_assert.equal(actual_signed_in_text, user_signed_in_text, f"Text in the top section is correct: '{actual_signed_in_text}'.", f"Wrong text in the top section. Actual text is '{actual_signed_in_text}' but shall be '{user_signed_in_text}'. Seems user is not logged in though shall be.", driver, report_screenshots_folder, tmp_test_urls_file_path, interrupt_test)

	def logout(self, driver, report_screenshots_folder, tmp_test_urls_file_path, interrupt_test=False):
		self.top_section.click_signed_in_user_link()
		self.top_section.click_logout_link_icon()
		# Check successful logout.
		mixed_assert.is_true(self.top_section.login_link_is_visible(), "Login link in the top section is correctly visible.", "Login link in the top section is not visible though it shall be.", driver, report_screenshots_folder, tmp_test_urls_file_path, interrupt_test)

	# test_basket_add_remove_item: Empty basket if there are items inside and go back to Alza main page.
	def empty_basket_if_items_inside(self):
		if self.top_section.check_if_basket_is_not_empty():
			self.top_section.click_basket_icon()
			self.basket_page.remove_all_items_from_basket()
			self.top_section.click_alza_icon()
		else:
			logger.info("\t- Nothing removed as there are no items in basket.")

	# test_watchdogs_add_remove_item: Empty watchdogs page if there are watched items and go back to Alza main page.
	def empty_watchdogs_page_if_watched_items(self):
		self.top_section.click_signed_in_user_link()
		self.top_section.click_my_profile_link()
		self.my_account_page.click_watchdogs_menu_item()
		self.watchdogs_page.remove_all_items_from_watchdogs_page()
		self.top_section.click_alza_icon()

	# test_add_remove_delivery_addresses: Add delivery addresses.
	def delivery_addresses_add_addresses(self):
		for data in delivery_addresses_original:
			self.delivery_addresses_page.click_add_new_address_button()
			self.delivery_addresses_details_dialog.fill_in_new_address_details(data)

	# test_add_remove_delivery_addresses: Edit delivery addresses.
	def delivery_addresses_edit_addresses(self):
		delivery_addresses = self.delivery_addresses_page.get_delivery_addresses()
		for index, delivery_address in enumerate(delivery_addresses):
			self.delivery_addresses_page.click_delivery_address_item_as_argument(delivery_address)
			self.delivery_addresses_details_dialog.edit_address_details(index)
