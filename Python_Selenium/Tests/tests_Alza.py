from test_data import TestData
from Page_Objects.basket_page import Basket
from Page_Objects.login_page import LoginPage
from Page_Objects.main_page import MainPage
from Page_Objects.my_account_page import MyAccount
from Page_Objects.top_section import TopSection
from Page_Objects.cookies_pane import CookiesPane
from Page_Objects.watchdogs_page import Watchdogs
from Page_Objects.watchdog_add_dialog import WatchdogAdd
from Page_Objects.delivery_addresses_page import DeliveryAddresses
from alza_module import AlzaModule
import pytest
import mixed_assertions as mixed_assert


@pytest.mark.usefixtures("initialize_driver")
class TestsAlza:

    def test_login_logout(self):
        """
        Tests log in and log out:
        - Reject all cookies, click login link.
        - Click signin button when credential fields are blank. Check that login dialog stays displayed and there are corresponding error messages displayed.
        - Provide wrong email address and correct password, click signin button. Check that login dialog stays displayed and there is correct
        text on signin button.
        - Provide correct email address and wrong password, click signin button. Check that login dialog stays displayed and there is correct
        text on signin button.
        - Provide correct email address and password, click signin button. Check that login dialog disappears and correct user email is displayed
        in the upper part of the screen.
        - Click logout link, check that login link is displayed.
        """

        self.login_page = LoginPage(self.driver)
        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.alza_module = AlzaModule(self.driver)

        # Reject all cookies.
        self.cookies_pane.click_reject_all_link()
        mixed_assert.is_true(self.cookies_pane.cookies_pane_is_invisible(), "Cookies pane is still visible but shall not be.")

        # Click login link.
        self.top_section.click_login_link()

        # Unsuccessful login:
        # Email and password fields blank.
        self.login_page.click_signin_button()
        mixed_assert.is_true(self.login_page.login_dialog_is_visible(), "Login dialog is not visible though it shall be.", True)
        actual_blank_email_text = self.login_page.get_blank_email_text()
        mixed_assert.equal(actual_blank_email_text, TestData.blank_email_text, f"Wrong message for blank e-mail input field. Actual message is '{actual_blank_email_text}' but it shall be '{TestData.blank_email_text}'.")
        actual_blank_password_text = self.login_page.get_blank_password_text()
        mixed_assert.equal(actual_blank_password_text, TestData.blank_password_text, f"Wrong message for blank password input field. Actual message is '{actual_blank_password_text}' but it shall be '{TestData.blank_password_text}'.")
        # Wrong email and correct password provided.
        self.login_page.provide_email(TestData.incorrect_user_name)
        self.login_page.provide_password(TestData.password)
        self.login_page.click_signin_button()
        mixed_assert.is_true(self.login_page.login_dialog_is_visible(), "Login dialog is not visible though it shall be.", True)
        actual_disabled_login_button_text = self.login_page.get_disabled_login_button_text()
        mixed_assert.equal(actual_disabled_login_button_text, TestData.signin_button_incorrect_user_name_password_text, f"Wrong message at signin button when incorrect e-mail provided. Actual message is '{actual_disabled_login_button_text}' but it shall be '{TestData.signin_button_incorrect_user_name_password_text}'.")
        # Correct email and wrong password provided.
        self.login_page.provide_email(TestData.user_name)
        self.login_page.provide_password(TestData.incorrect_password)
        self.login_page.click_signin_button()
        mixed_assert.is_true(self.login_page.login_dialog_is_visible(), "Login dialog is not visible though it shall be.", True)
        actual_disabled_login_button_text = self.login_page.get_disabled_login_button_text()
        mixed_assert.equal(actual_disabled_login_button_text, TestData.signin_button_incorrect_user_name_password_text, f"Wrong message at signin button when incorrect password provided. Actual message is '{actual_disabled_login_button_text}' but it shall be '{TestData.signin_button_incorrect_user_name_password_text}'.")

        # Successful login.
        self.login_page.provide_email(TestData.user_name)
        self.login_page.provide_password(TestData.password)
        self.login_page.click_signin_button()
        mixed_assert.is_true(self.login_page.login_dialog_is_invisible(), "Login dialog is still visible but shall not be.", True)
        actual_signed_in_text = self.top_section.get_signed_in_user_text()
        mixed_assert.equal(actual_signed_in_text, TestData.user_signed_in_text, f"Wrong text in the top menu. Actual text is '{actual_signed_in_text}' but shall be '{TestData.user_signed_in_text}'. Seems user is not logged in though shall be.", True)

        # Logout.
        self.top_section.click_signed_in_user_link()
        self.top_section.click_logout_link()
        # Check successful logout.
        mixed_assert.is_true(self.top_section.login_link_is_visible(), "Login link is not visible though it shall be.", True)

    def test_basket_add_remove_item(self):
        """
        Tests adding and removing item from basket:
        - Reject all cookies and log in, if there are items in basket, remove them.
        - Add computer to basket and check number of items at basket icon.
        - Go to basket, check name of item present, its count and price.
        - Remove item from basket, check that basket is empty and there is no number at basket icon.
        - Log out.
        """

        self.login_page = LoginPage(self.driver)
        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.main_page = MainPage(self.driver)
        self.basket_page = Basket(self.driver)
        self.alza_module = AlzaModule(self.driver)

        # Reject all cookies and log into application.
        self.alza_module.reject_cookies_and_login()

        # Precondition: Empty basket if there are items inside and go back to Alza main page.
        self.alza_module.empty_basket_if_items_inside()

        # Putting into basket:
        # Navigate to computers.
        self.main_page.hover_click_computers_notebooks_menu_item()
        self.main_page.click_computers_tile()
        # Get first computer name and price, put it into basket and go there.
        first_computer_name = self.main_page.get_first_computer_name()
        first_computer_price = self.main_page.get_first_computer_price()
        self.main_page.click_first_computer_put_to_basket_button()
        # Check there is correct number at basket icon and go to basket.
        actual_number_of_items_at_basket_icon = self.top_section.get_number_of_items_at_basket_icon()
        mixed_assert.equal(actual_number_of_items_at_basket_icon, TestData.number_of_items_in_basket, f"Wrong number of items at basket icon. Actual number is '{actual_number_of_items_at_basket_icon}' but it shall be '{TestData.number_of_items_in_basket}'.")
        self.top_section.click_basket_icon()

        # On basket_page page:
        # Check item name, count and price.
        actual_computer_name = self.basket_page.get_item_name()
        mixed_assert.is_in(first_computer_name, actual_computer_name, f"Wrong name of computer in basket. Actual name is '{actual_computer_name}' but it shall be '{first_computer_name}'. Seems computer that shall be in basket is not.")
        actual_number_of_computers_in_basket = self.basket_page.get_item_count()
        mixed_assert.equal(actual_number_of_computers_in_basket, TestData.number_of_items_in_basket, f"Wrong number of computers in basket. There are '{actual_number_of_computers_in_basket}' computers but there shall be '{TestData.number_of_items_in_basket}' computer.")
        actual_computer_price_in_basket = self.basket_page.get_item_price()
        mixed_assert.equal(actual_computer_price_in_basket, first_computer_price, f"Wrong computer price in basket. Actual price is '{actual_computer_price_in_basket}' but shall be '{first_computer_price}'.")
        # Remove item from basket and check it is empty.
        self.basket_page.remove_all_items_from_basket()
        actual_text_once_basket_empty = self.basket_page.get_text_once_all_items_removed()
        mixed_assert.equal(actual_text_once_basket_empty, TestData.text_once_all_items_removed_from_basket, f"Wrong text once basket is empty. Actual text is '{actual_text_once_basket_empty}' but it shall be '{TestData.text_once_all_items_removed_from_basket}'. Seems basket is not empty.")
        # Check there is no number at basket icon.
        actual_number_of_items_at_basket_icon = self.top_section.get_number_of_items_at_basket_icon()
        mixed_assert.equal(actual_number_of_items_at_basket_icon, "No items", f"Wrong number of items at basket icon. Actual number is '{actual_number_of_items_at_basket_icon}' but there shall be no items.")

        # Logout.
        self.alza_module.logout()

    def test_search(self):
        """
        Tests searching via search button and by clicking suggestion:
        - Reject all cookies and log in.
        - Type "jízdní kola" into search input, press search button. Check that header of result page is "jízdní kola" and that amount of items found
        is bigger than 0.
        - Type "recenze" into search box, wait for suggestions to appear. Click first suggestion in suggestions and check that header of result page contains
        word "recenze".
        - Log out.
        """

        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.login_page = LoginPage(self.driver)
        self.main_page = MainPage(self.driver)
        self.alza_module = AlzaModule(self.driver)

        # Reject all cookies and log into application.
        self.alza_module.reject_cookies_and_login()

        # Search for "jízdní kola" and click search button:
        self.top_section.search_provide_value(TestData.search_value_via_search_button)
        self.top_section.click_search_button()
        # Check result.
        actual_search_result_title = self.main_page.get_search_result_header()
        mixed_assert.equal(actual_search_result_title, TestData.search_result_header_via_search_button, f"Wrong header of looked up section is displayed. Actual header is '{actual_search_result_title}' but it shall be '{TestData.search_result_header_via_search_button}'. Seems wrong section is displayed.")
        mixed_assert.greater(self.main_page.get_search_result_items_amount(), 0, "No items found, items shall be found.")

        # Search for "recenze" and choose from suggestion:
        self.top_section.search_provide_value(TestData.search_value_via_suggestion)
        self.top_section.search_suggestion_click_1st_item()
        # Check result.
        actual_search_result_title = self.main_page.get_search_result_header().lower()
        mixed_assert.is_in(TestData.search_result_word_in_title_via_suggestion, actual_search_result_title, f"Result doesn't contain looked up word in title. Actual title is '{actual_search_result_title}', it does not contain word '{TestData.search_result_word_in_title_via_suggestion}' though it shall.")

        # Logout.
        self.alza_module.logout()

    def test_watchdogs_add_remove_item(self):
        """
        Tests adding and removing item from watchdogs list:
        - Reject all cookies and log in, if there are items in watchdogs list, remove them.
        - Add watchdog to pet supply item, go to watchdogs list. Check name of item present, its price limit and that checkbox for alerting when price
        decreases under price limit is checked.
        - Remove item from watchdogs list, check that watchdogs list is empty.
        - Log out.
        """

        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.login_page = LoginPage(self.driver)
        self.main_page = MainPage(self.driver)
        self.my_account_page = MyAccount(self.driver)
        self.watchdogs_page = Watchdogs(self.driver)
        self.watchdog_add_dialog = WatchdogAdd(self.driver)
        self.alza_module = AlzaModule(self.driver)

        # Reject all cookies and log into application and stop test execution if login failed.
        self.alza_module.reject_cookies_and_login(True)

        # Precondition: Empty watchdogs list if there are watched items and go back to Alza main page.
        self.alza_module.empty_watchdogs_list_if_watched_items()

        # Navigate to pet supplies, open first pet supply, handle dialog if appears and get supply name.
        self.main_page.hover_click_pet_supplies_menu_item()
        self.main_page.click_first_pet_suppy_item()
        self.main_page.pet_supply_close_dialog()
        first_pet_supply_name = self.main_page.get_first_pet_supply_name()

        # Watchdog dialog:
        self.main_page.click_watch_price_link()
        # Check prefilled e-mail address.
        actual_email = self.watchdog_add_dialog.get_email()
        mixed_assert.equal(actual_email, TestData.user_name, f"Incorrect e-mail address prefilled. There is '{actual_email}' but there shall be '{TestData.user_name}'.")
        # Set watch price, confirm and close success popup.
        self.watchdog_add_dialog.set_price_limit(TestData.watchdog_price_limit)
        self.watchdog_add_dialog.click_confirm_button()
        self.watchdogs_page.close_success_popup()

        # Check watchdogs page and remove item:
        # Go to watchdogs page.
        self.top_section.click_signed_in_user_link()
        self.top_section.click_my_profile_link()
        self.my_account_page.click_watchdogs_menu_item()
        # Check watched item name and price limit, checkbox alert price is checked.
        actual_pet_supply_name = self.watchdogs_page.get_watchdog_item_name()
        mixed_assert.is_in(first_pet_supply_name, actual_pet_supply_name, f"Wrong name of pet supply in watchdogs. Actual pet supply name is '{actual_pet_supply_name}' but it shall be '{first_pet_supply_name}'. Seems pet supply that shall be in watchdogs is not.")
        actual_price_limit = self.watchdogs_page.get_price_limit_provided()
        mixed_assert.equal(actual_price_limit, TestData.watchdog_price_limit, f"Wrong price limit displayed in watchdogs. Actual price limit is '{actual_price_limit}' but it shall be '{TestData.watchdog_price_limit}'.")
        mixed_assert.is_true(self.watchdogs_page.check_alert_price_is_checked(), f"Checkbox for alert when price is lower than '{TestData.watchdog_price_limit}' shall be checked but it is not.")
        # Remove item from watchdogs list.
        self.watchdogs_page.remove_all_items_from_watchdogs_list()
        actual_text_once_watchdogs_list_empty = self.watchdogs_page.get_text_once_all_items_removed()
        mixed_assert.equal(actual_text_once_watchdogs_list_empty, TestData.text_once_all_items_removed_from_watchdogs_list, f"Wrong text once watchdogs list is empty. Actual text is '{actual_text_once_watchdogs_list_empty}' but it shall be '{TestData.text_once_all_items_removed_from_watchdogs_list}'. Seems watchdogs list is not empty.")

        # Logout.
        self.alza_module.logout()

    def test_delivery_addresses_add_remove_addresses(self):
        """
        Tests adding and removing addresses from delivery addresses list:
        - Reject all cookies and log in, if there are addresses in delivery addresses list, remove them.
        - Add 2 delivery addresses, go to main page, then back to delivery addresses list. Check number of delivery addresses and that at both all provided
        data is correct.
        - Edit data at both addresses, go to main page, then back to delivery addresses list. Check that at both addresses all edited data is correct.
        - Remove both addresses from delivery addresses list and check that delivery addresses list is empty.
        - Log out.
        Note: Number of addresses can be changed by adding or removing dictionaries from TestData.delivery_addresses_original and TestData.delivery_addresses_edited.
        """

        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.login_page = LoginPage(self.driver)
        self.delivery_addresses_page = DeliveryAddresses(self.driver)
        self.my_account_page = MyAccount(self.driver)
        self.alza_module = AlzaModule(self.driver)

        # Reject all cookies and log into application and stop test execution if login failed.
        self.alza_module.reject_cookies_and_login(True)

        # Adding delivery addresses:
        # Go to delivery addresses page:
        self.top_section.click_signed_in_user_link()
        self.top_section.click_my_profile_link()
        self.my_account_page.click_delivery_addresses_menu_item()
        # Precondition: Empty delivery addresses list if there are addresses.
        self.delivery_addresses_page.remove_all_addresses_from_delivery_addresses_list()
        # Add 2 delivery addresses.
        self.alza_module.delivery_addresses_add_addresses()

        # Go to Alza main page and back to delivery addresses and check added addresses are present with correct data:
        self.top_section.click_alza_icon()
        # Go to delivery addresses page.
        self.top_section.click_signed_in_user_link()
        self.top_section.click_my_profile_link()
        self.my_account_page.click_delivery_addresses_menu_item()
        # Check number of addresses and their data.
        actual_number_of_delivery_addresses = self.delivery_addresses_page.get_number_of_addresses()
        expected_number_of_delivery_addresses = len(TestData.delivery_addresses_original)
        mixed_assert.equal(actual_number_of_delivery_addresses, expected_number_of_delivery_addresses, f"Incorrect number of delivery addresses. Actual number is '{actual_number_of_delivery_addresses}' but it shall be '{expected_number_of_delivery_addresses}'.")
        actual_delivery_addresses_data = self.delivery_addresses_page.get_addresses_data(actual_number_of_delivery_addresses)
        mixed_assert.equal(actual_delivery_addresses_data, TestData.delivery_addresses_original, f"Actual delivery addresses are not the same as provided delivery addresses. Actual delivery addresses are '{actual_delivery_addresses_data}', expected delivery addresses are '{TestData.delivery_addresses_original}'.")

        # Editing delivery addresses:
        self.alza_module.delivery_addresses_edit_addresses()
        # Go to Alza main page.
        self.top_section.click_alza_icon()
        # Go to delivery addresses page.
        self.top_section.click_signed_in_user_link()
        self.top_section.click_my_profile_link()
        self.my_account_page.click_delivery_addresses_menu_item()
        # Check addresses have correct edited data.
        actual_delivery_addresses_data = self.delivery_addresses_page.get_addresses_data(actual_number_of_delivery_addresses)
        mixed_assert.equal(actual_delivery_addresses_data, TestData.delivery_addresses_edited, f"Actual delivery addresses are not the same as updated delivery addresses. Actual delivery addresses are '{actual_delivery_addresses_data}', expected delivery addresses are '{TestData.delivery_addresses_edited}'.")

        # Remove delivery addresses:
        self.delivery_addresses_page.remove_all_addresses_from_delivery_addresses_list()
        # Check there are no addresses.
        actual_number_of_delivery_addresses = self.delivery_addresses_page.get_number_of_addresses()
        mixed_assert.equal(actual_number_of_delivery_addresses, 0, f"There are delivery addresses present though there shall not be any. There are '{actual_number_of_delivery_addresses}' delivery addresses.")

        # Logout.
        self.alza_module.logout()
