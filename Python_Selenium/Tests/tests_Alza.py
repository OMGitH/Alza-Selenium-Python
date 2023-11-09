import pytest

from Config.test_data import TestData
from Helpers.helpers import Helpers
from Page_objects.basket import Basket
from Page_objects.login_page import LoginPage
from Page_objects.main_page import MainPage
from Page_objects.my_account import MyAccount
from Page_objects.top_section import TopSection
from Page_objects.cookies_pane import CookiesPane
from Page_objects.watchdogs_page import Watchdogs
from Page_objects.watchdog_add_dialog import WatchdogAdd


@pytest.mark.usefixtures("initialize_driver")
class TestsAlza:

    def test_login_logout(self):
        """
        Tests log in functionality. First all cookies are rejected, then login is clicked.
        Credential fields are blank, signin button is clicked and it is checked that login dialog stays open and there are corresponding error messages displayed.
        Then wrong email address is provided with correct password, signin button is clicked and it is checked that login stays displayed and there is correct
        text on signin button.
        Then correct email address is provided with wrong password, signin button is clicked and it is checked that login stays displayed and there is correct
        text on signin button.
        Then both correct email address and correct password are provided, signin button is clicked and it is checked that login disappears and correct
        user email is displayed in upper part of the screen.
        At the end logout link is clicked and it is checked that login link is present.
        """

        self.login_page = LoginPage(self.driver)
        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()
        assert self.cookies_pane.cookies_pane_is_invisible(), "Cookies pane is still visible but shall not be."

        # Click login link.
        self.top_section.top_section_click_login_link()

        # Unsuccessful login:
        # Email and password fields blank.
        self.login_page.login_click_signin_button()
        assert self.login_page.login_dialog_is_visible(), "Login dialog is not visible though it shall be."
        actual_blank_email_text = self.login_page.login_get_blank_email_text()
        assert actual_blank_email_text == TestData.blank_email_text, f"Wrong message for blank e-mail input field. Current message is {actual_blank_email_text} but it shall be {TestData.blank_email_text}."
        actual_blank_password_text = self.login_page.login_get_blank_password_text()
        assert actual_blank_password_text == TestData.blank_password_text, f"Wrong message for blank password input field. Current message is {actual_blank_password_text} but it shall be {TestData.blank_password_text}."

        # Wrong email and correct password provided.
        self.login_page.login_provide_email(TestData.incorrect_user_name)
        self.login_page.login_provide_password(TestData.password)
        self.login_page.login_click_signin_button()
        assert self.login_page.login_dialog_is_visible(), "Login dialog is not visible though it shall be."
        actual_disabled_login_button_text = self.login_page.login_get_disabled_login_button_text()
        assert actual_disabled_login_button_text == TestData.signin_button_incorrect_user_name_password_text, f"Wrong message at signin button when incorrect email provided. Current message is {actual_disabled_login_button_text} but it shall be {TestData.signin_button_incorrect_user_name_password_text}."

        # Correct email and wrong password provided.
        self.login_page.login_provide_email(TestData.user_name)
        self.login_page.login_provide_password(TestData.incorrect_password)
        self.login_page.login_click_signin_button()
        assert self.login_page.login_dialog_is_visible(), "Login dialog is not visible though it shall be."
        actual_disabled_login_button_text = self.login_page.login_get_disabled_login_button_text()
        assert actual_disabled_login_button_text == TestData.signin_button_incorrect_user_name_password_text, f"Wrong message at signin button when incorrect password provided. Current message is {actual_disabled_login_button_text} but it shall be {TestData.signin_button_incorrect_user_name_password_text}."

        # Successful login.
        self.login_page.login_provide_email(TestData.user_name)
        self.login_page.login_provide_password(TestData.password)
        self.login_page.login_click_signin_button()
        assert self.login_page.login_dialog_is_invisible(), "Login dialog is still visible but shall not be."
        actual_signed_in_text = self.top_section.top_section_get_signed_in_user_text()
        assert actual_signed_in_text == TestData.user_signed_in_text, f"Wrong text in the top menu. Current text is {actual_signed_in_text} but shall be {TestData.user_signed_in_text}. User is not logged in though shall be?"

        # Logout.
        self.top_section.top_section_click_signed_in_user_link()
        self.top_section.top_section_click_logout_link()
        assert self.top_section.top_section_login_link_is_visible(), "Login link is not visible, though it shall be."

    def test_basket_add_remove_item(self):
        """
        Tests adding and removing item from basket. First all cookies are rejected then logs in, if there are items in basket they are removed,
        then adds computer to basket, checks number of items at basket icon, goes to basket, checks name of item present, its count and price.
        Then removes item from basket and checks basket is empty.
        At the end logs out.
        """

        self.login_page = LoginPage(self.driver)
        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.main_page = MainPage(self.driver)
        self.basket = Basket(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()

        # Log into application:
        # Click login link.
        self.top_section.top_section_click_login_link()
        # Fill in credentials and login.
        self.login_page.login_successful_login(TestData.user_name, TestData.password)

        # Empty basket if there are items inside.
        if self.top_section.top_section_basket_is_not_empty():
            self.top_section.top_section_click_basket_icon()
            self.basket.basket_remove_all_items_from_basket()
            self.top_section.top_section_click_alza_icon()

        # Putting into basket:
        # Navigate to computers.
        self.main_page.main_page_hover_click_computers_notebooks_menu_item()
        self.main_page.main_page_click_computers_tile()
        # Get first computer name and price and put it into basket and go there.
        first_computer_name = self.main_page.main_page_get_first_computer_name()
        first_computer_price = self.main_page.main_page_get_first_computer_price()
        self.main_page.main_page_click_first_computer_put_to_basket_button()
        # Check there is correct number at basket icon and go to basket.
        actual_number_of_items_at_basket_icon = self.top_section.top_section_get_number_of_items_at_basket_icon()
        assert actual_number_of_items_at_basket_icon == TestData.number_of_items_in_basket, f"Wrong number of items at basket icon. Actual number is {actual_number_of_items_at_basket_icon} but it shall be {TestData.number_of_items_in_basket}."
        self.top_section.top_section_click_basket_icon()

        # On basket page:
        # Check item name, count and price.
        actual_computer_name = self.basket.basket_get_item_name()
        assert first_computer_name in actual_computer_name, f"Wrong name of computer in basket. Actual name is {actual_computer_name} but it shall be {first_computer_name}. Computer that shall be in basket is not?"
        actual_number_of_computers_in_basket = self.basket.basket_get_item_count()
        assert actual_number_of_computers_in_basket == TestData.number_of_items_in_basket, f"Wrong number of computers in basket. There are {actual_number_of_computers_in_basket} computers but there shall be {TestData.number_of_items_in_basket} computer."
        actual_computer_price_in_basket = self.basket.basket_get_item_price()
        assert actual_computer_price_in_basket == first_computer_price, f"Wrong computer price in basket. Price is {actual_computer_price_in_basket} but shall be {first_computer_price}."
        # Remove item from basket and check it is empty.
        self.basket.basket_remove_all_items_from_basket()
        actual_text_once_basket_empty = self.basket.basket_get_text_once_all_items_removed()
        assert actual_text_once_basket_empty == TestData.text_once_all_items_removed_from_basket, f"Wrong text once basket is empty. Text is {actual_text_once_basket_empty} but it shall be {TestData.text_once_all_items_removed_from_basket}. Basket is not empty?"

        # Logout.
        self.top_section.top_section_click_signed_in_user_link()
        self.top_section.top_section_click_logout_link()

    def test_search(self):
        """
        Tests search functionality in 2 ways. First all cookies are rejected then logs in, provides search value, presses search button
        and checks header of result and that amount of items found is bigger than 0.
        Then provides search value, waits for suggestions to appear, clicks first article in suggestions and checks that name of article contains
        looked up word.
        At the end logs out.
        """

        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.login_page = LoginPage(self.driver)
        self.main_page = MainPage(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()

        # Log into application:
        # Click login link.
        self.top_section.top_section_click_login_link()
        # Fill in credentials, login, switch back to page.
        self.login_page.login_successful_login(TestData.user_name, TestData.password)

        # Search for "jízdní kola" and click search button:
        self.top_section.top_section_search_provide_value(TestData.search_value_via_search_button)
        self.top_section.top_section_click_search_button()
        # Check result.
        actual_search_result_title = self.main_page.main_page_get_search_result_header()
        assert actual_search_result_title == TestData.search_result_header_via_search_button, f"Wrong header of looked up section is displayed. Actual header is {actual_search_result_title} but it shall be {TestData.search_result_header_via_search_button}. Wrong section displayed?"
        assert self.main_page.main_page_get_search_result_items_amount() > 0, "No items found, items shall be found."

        # Search for "recenze" and choose from suggestion:
        self.top_section.top_section_search_provide_value(TestData.search_value_via_suggestion)
        self.top_section.top_section_search_suggestion_click_1st_item()
        # Check result.
        actual_search_result_title = self.main_page.main_page_get_search_result_header().lower()
        assert TestData.search_result_word_in_title_via_suggestion in actual_search_result_title, f"Result doesn't contain looked up word in title. Actual article title is {actual_search_result_title}, it does not contain word {TestData.search_result_word_in_title_via_suggestion}."

        # Logout.
        self.top_section.top_section_click_signed_in_user_link()
        self.top_section.top_section_click_logout_link()

    def test_watchdog_add_remove_item(self):
        """
        Tests adding and removing item from watchdog list. First all cookies are rejected then logs in, if there are items in watchdog list they
        are removed. Then adds watchdog to pet supply item, goes to watchdog list, checks name of item present, its price limit and that checkbox
        for alerting when price decreases is checked. Then removes item from watchdog list and checks watchdog list is empty.
        At the end logs out.
        """

        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.login_page = LoginPage(self.driver)
        self.main_page = MainPage(self.driver)
        self.my_account_page = MyAccount(self.driver)
        self.watchdogs_page = Watchdogs(self.driver)
        self.watchdog_add_dialog = WatchdogAdd(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()

        # Log into application:
        # Click login link.
        self.top_section.top_section_click_login_link()
        # Fill in credentials, login, switch back to page.
        self.login_page.login_successful_login(TestData.user_name, TestData.password)

        # Empty watchdog list if there are watched items.
        self.top_section.top_section_click_signed_in_user_link()
        self.top_section.top_section_click_my_profile_link()
        self.my_account_page.my_account_click_watchdogs_link()
        self.watchdogs_page.watchdogs_remove_all_items()
        self.top_section.top_section_click_alza_icon()

        # Navigate to pet supplies, open first pet supply and get its name.
        self.main_page.main_page_hover_click_pet_supplies_menu_item()
        self.main_page.main_page_click_first_pet_suppy_item()
        first_pet_supply_name = self.main_page.main_page_get_first_pet_supply_name()

        # Watchdog dialog:
        self.main_page.main_page_click_watch_price()
        # Check prefilled e-mail address.
        actual_email = self.watchdog_add_dialog.watchdog_add_dialog_get_email()
        assert actual_email == TestData.user_name, f"Incorrect e-mail address prefilled. There is {actual_email} but there should be {TestData.user_name}."
        # Set watch price.
        self.watchdog_add_dialog.watchdog_add_dialog_set_price_limit(TestData.watchdog_price_limit)
        self.watchdog_add_dialog.watchdog_add_dialog_click_confirm_button()

        # Check watchdogs page:
        # Go to watchdogs page.
        self.top_section.top_section_click_signed_in_user_link()
        self.top_section.top_section_click_my_profile_link()
        self.my_account_page.my_account_click_watchdogs_link()
        # Check watched item name and price limit, checkbox alert price is checked.
        actual_pet_supply_name = self.watchdogs_page.watchdogs_get_watchdog_item_name()
        assert first_pet_supply_name in actual_pet_supply_name, f"Wrong name of pet supply in watchdogs. Actual pet supply name in watchdogs is {actual_pet_supply_name} but it shall be {first_pet_supply_name}. Pet supply that shall be in watchdogs is not?"
        actual_price_limit = self.watchdogs_page.watchdogs_get_price_limit_provided()
        assert actual_price_limit == TestData.watchdog_price_limit, f"Wrong price limit displayed in watchdogs. Actual price limit in watchdogs is {actual_price_limit} but it shall be {TestData.watchdog_price_limit}."
        assert self.watchdogs_page.watchdogs_check_alert_price_is_checked(), f"Checkbox for alert when price is lower than {TestData.watchdog_price_limit} shall be checked but it is not."
        # Remove item from watchdog list.
        self.watchdogs_page.watchdogs_remove_all_items()
        actual_text_once_watchdog_list_empty = self.watchdogs_page.watchdogs_get_text_once_all_items_removed()
        assert actual_text_once_watchdog_list_empty == TestData.text_once_all_items_removed_from_watchdog_list, f"Wrong text once watchodg list is empty. Acutal text is {actual_text_once_watchdog_list_empty} but it shall be {TestData.text_once_all_items_removed_from_watchdog_list}. Watchdog list is not empty?"

        # Logout.
        self.top_section.top_section_click_signed_in_user_link()
        self.top_section.top_section_click_logout_link()

    def test_additional_account_changes(self):
        """
        Tests changes of information in user account. First all cookies are rejected then logs in and navigates to user account page.
        Then street, zip and city fields are filled in.
        Then navigates to main page and back to user account page where is checked that fields still have values provided into them.
        After that fields are returned to original state, i.e. cleared.
        At the end logs out.
        """

        self.login_page = LoginPage(self.driver)
        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.my_account_page = MyAccount(self.driver)
        self.helpers = Helpers(self.driver)

        # Reject all cookies.
        self.cookies_pane.cookies_pane_click_reject_all()

        # Log into application:
        # Click login link.
        self.top_section.top_section_click_login_link()
        # Fill in credentials and login.
        self.login_page.login_successful_login(TestData.user_name, TestData.password)
        # Switch from login frame back to page.
        self.login_page.login_switch_back_from_login_frame()

        # Changes to my account:
        # Navigate to my account page.
        self.top_section.top_section_click_my_profile_link()
        self.my_account_page.my_account_click_account_settings_dropdown()
        self.my_account_page.my_account_click_my_account_menu_item()
        # Fill in street, zip, city.
        self.my_account_page.my_account_provide_street()
        self.my_account_page.my_account_provide_zip()
        self.my_account_page.my_account_provide_city()
        # Go back to main page.
        self.top_section.top_section_click_alza_icon()
        # Go back to my account page and check provided values are stored.
        self.top_section.top_section_click_my_profile_link()
        self.my_account_page.my_account_click_account_settings_dropdown()
        self.my_account_page.my_account_click_my_account_menu_item()
        actual_street_and_number = self.my_account_page.my_account_get_street_value()
        assert actual_street_and_number == TestData.street_and_number, f"Wrong street and number. Actual street and number is {actual_street_and_number} but it shall be {TestData.street_and_number}."
        actual_zip = self.my_account_page.my_account_get_zip_value()
        assert actual_zip == TestData.zip, f"Wrong zip. Actual zip is {actual_zip} but it shall be {TestData.zip}."
        actual_city = self.my_account_page.my_account_get_city_value()
        assert actual_city == TestData.city, f"Wrong city. Actual city is {actual_city} but it shall be {TestData.city}."

        # Clear street, zip, city.
        self.my_account_page.my_account_clear_street_input()
        self.my_account_page.my_account_clear_zip_input()
        self.my_account_page.my_account_clear_city_input()
        # Refresh page to refresh values for assertions.
        self.helpers.helpers_refresh_page()
        assert self.my_account_page.my_account_get_street_value() == "", "Street input field is not empty though it shall be."
        assert self.my_account_page.my_account_get_zip_value() == "", "Zip input field is not empty though it shall be."
        assert self.my_account_page.my_account_get_city_value() == "", "City input field is not empty though it shall be."

        # Logout.
        self.top_section.top_section_click_logout_link()