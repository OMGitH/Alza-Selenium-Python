from Page_Objects.cookies_pane import CookiesPane
from Page_Objects.login_page import LoginPage
from Page_Objects.top_section import TopSection
from Page_Objects.basket_page import Basket
from Page_Objects.my_account_page import MyAccount
from Page_Objects.watchdogs_page import Watchdogs
from Config.test_data import TestData
import mixed_assertions as mixed_assert


class AlzaModule:

	# Initialization.
	def __init__(self, driver):
		self.driver = driver
		self.login_page = LoginPage(self.driver)
		self.cookies_pane = CookiesPane(self.driver)
		self.top_section = TopSection(self.driver)
		self.basket_page = Basket(self.driver)
		self.my_account_page = MyAccount(self.driver)
		self.watchdogs_page = Watchdogs(self.driver)

	# Login and logout:
	def reject_cookies_and_login(self):
		# Reject all cookies.
		self.cookies_pane.cookies_pane_click_reject_all()
		# Log into application:
		# Click login link.
		self.top_section.top_section_click_login_link()
		# Fill in credentials and login.
		self.login_page.login_successful_login(TestData.user_name, TestData.password)

	def logout(self):
		self.top_section.top_section_click_signed_in_user_link()
		self.top_section.top_section_click_logout_link()
		mixed_assert.is_true(self.top_section.top_section_login_link_is_visible(), "Login link is not visible though it shall be.")

	# test_basket_add_remove_item: Empty basket if there are items inside and go back to Alza main page.
	def empty_basket_if_items_inside(self):
		if self.top_section.top_section_check_if_basket_not_empty():
			self.top_section.top_section_click_basket_icon()
			self.basket_page.basket_remove_all_items_from_basket()
			self.top_section.top_section_click_alza_icon()

	# test_watchdog_add_remove_item: Empty watchdog list if there are watched items and go back to Alza main page.
	def empty_watchdog_list_if_watched_items(self):
		self.top_section.top_section_click_signed_in_user_link()
		self.top_section.top_section_click_my_profile_link()
		self.my_account_page.my_account_click_watchdogs_link()
		self.watchdogs_page.watchdogs_remove_all_items_from_watchdogs_list()
		self.top_section.top_section_click_alza_icon()
