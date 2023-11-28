from Page_Objects.cookies_pane import CookiesPane
from Page_Objects.login_page import LoginPage
from Page_Objects.top_section import TopSection
from Config.test_data import TestData
import mixed_assertions as mixed_assert


class AlzaModule:

	# Initialization.
	def __init__(self, driver):
		self.driver = driver
		self.login_page = LoginPage(self.driver)
		self.cookies_pane = CookiesPane(self.driver)
		self.top_section = TopSection(self.driver)

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
