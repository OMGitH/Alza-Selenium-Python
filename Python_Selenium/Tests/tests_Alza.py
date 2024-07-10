import pytest
import mixed_assertions as mixed_assert
from Page_Objects.basket_page import Basket
from Page_Objects.cookies_pane import CookiesPane
from Page_Objects.delivery_addresses_page import DeliveryAddresses
from Page_Objects.item_page import ItemPage
from Page_Objects.login_page import LoginPage
from Page_Objects.main_page import MainPage
from Page_Objects.my_account_page import MyAccount
from Page_Objects.top_section import TopSection
from Page_Objects.watchdogs_add_dialog import WatchdogAdd
from Page_Objects.watchdogs_page import Watchdogs
from Tests import test_data
from alza_module import AlzaModule
from report_logger import logger


@pytest.mark.usefixtures("get_report_screenshots_folder_name", "setup_and_teardown", "get_tmp_test_urls_file_path")
class TestsAlza:

    def test_login_logout(self):
        """Tests log in and log out:
        - Reject all cookies, check that cookies pane is invisible, click login link.
        - Click signin button when credential fields are blank. Check that login dialog stays displayed and there are corresponding error messages displayed.
        - Provide wrong e-mail address and correct password, click signin button. Check that login dialog stays displayed and there is correct
        text on signin button.
        - Provide correct e-mail address and wrong password, click signin button. Check that login dialog stays displayed and there is correct
        text on signin button.
        - Provide correct e-mail address and password, click signin button. Check that login dialog disappears and correct user e-mail is displayed
        in the top section of the screen.
        - Click logout link, check that login link is displayed in the top section of the screen.
        """
        self.login_page = LoginPage(self.driver)
        self.cookies_pane = CookiesPane(self.driver)
        self.top_section = TopSection(self.driver)
        self.alza_module = AlzaModule(self.driver)

        # Reject all cookies.
        logger.info("------- REJECT ALL COOKIES -------")
        self.cookies_pane.click_reject_all_button()
        mixed_assert.is_true(self.cookies_pane.cookies_pane_is_invisible(handle_timeout_exception=True), "Cookies pane is correctly invisible.", "Cookies pane is still visible but shall not be.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Unsuccessful login:
        # E-mail and password fields blank.
        logger.info("------- UNSUCCESSFUL LOGIN: E-MAIL AND PASSWORD FIELDS BLANK -------")
        self.top_section.click_login_link()
        self.login_page.click_signin_button()
        mixed_assert.is_true(self.login_page.login_dialog_is_visible(), "Login dialog is correctly visible.", "Login dialog is not visible though it shall be.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path, True)
        actual_blank_email_text = self.login_page.get_blank_email_text()
        mixed_assert.equal(actual_blank_email_text, test_data.blank_email_error_text, f"Message for blank e-mail input field is correct: '{actual_blank_email_text}'.", f"Wrong message for blank e-mail input field. Actual message is '{actual_blank_email_text}' but it shall be '{test_data.blank_email_error_text}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        actual_blank_password_text = self.login_page.get_blank_password_text()
        mixed_assert.equal(actual_blank_password_text, test_data.blank_password_error_text, f"Message for blank password input field is correct: '{actual_blank_password_text}'.", f"Wrong message for blank password input field. Actual message is '{actual_blank_password_text}' but it shall be '{test_data.blank_password_error_text}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        # Wrong e-mail and correct password provided.
        logger.info("------- UNSUCCESSFUL LOGIN: WRONG E-MAIL AND CORRECT PASSWORD PROVIDED -------")
        self.login_page.provide_email(test_data.incorrect_user_name)
        self.login_page.provide_password(test_data.password)
        self.login_page.click_signin_button()
        mixed_assert.is_true(self.login_page.login_dialog_is_visible(), "Login dialog is correctly visible.", "Login dialog is not visible though it shall be.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path, True)
        actual_disabled_signin_button_text = self.login_page.get_disabled_signin_button_text()
        mixed_assert.equal(actual_disabled_signin_button_text, test_data.signin_button_incorrect_user_name_password_error_text, f"Message at signin button when incorrect e-mail provided is as expected: '{actual_disabled_signin_button_text}'.", f"Wrong message at signin button when incorrect e-mail provided. Actual message is '{actual_disabled_signin_button_text}' but it shall be '{test_data.signin_button_incorrect_user_name_password_error_text}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        # Correct e-mail and wrong password provided.
        logger.info("------- UNSUCCESSFUL LOGIN: CORRECT E-MAIL AND WRONG PASSWORD PROVIDED -------")
        self.login_page.provide_email(test_data.user_name)
        self.login_page.provide_password(test_data.incorrect_password)
        self.login_page.click_signin_button()
        mixed_assert.is_true(self.login_page.login_dialog_is_visible(), "Login dialog is correctly visible.", "Login dialog is not visible though it shall be.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path, True)
        actual_disabled_signin_button_text = self.login_page.get_disabled_signin_button_text()
        mixed_assert.equal(actual_disabled_signin_button_text, test_data.signin_button_incorrect_user_name_password_error_text, f"Message at signin button when incorrect password provided is as expected: '{actual_disabled_signin_button_text}'.", f"Wrong message at signin button when incorrect password provided. Actual message is '{actual_disabled_signin_button_text}' but it shall be '{test_data.signin_button_incorrect_user_name_password_error_text}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Successful login.
        logger.info("------- SUCCESSFUL LOGIN -------")
        self.login_page.provide_email(test_data.user_name)
        self.login_page.provide_password(test_data.password)
        self.login_page.click_signin_button()
        mixed_assert.is_true(self.login_page.login_dialog_is_invisible(), "Login dialog is correctly invisible.", "Login dialog is still visible but shall not be.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path, True)
        actual_signed_in_text = self.top_section.get_signed_in_user_text()
        mixed_assert.equal(actual_signed_in_text, test_data.user_signed_in_text, f"Text in the top section is correct: '{actual_signed_in_text}'.", f"Wrong text in the top section. Actual text is '{actual_signed_in_text}' but shall be '{test_data.user_signed_in_text}'. Seems user is not logged in though shall be.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path, True)

        # Logout.
        logger.info("------- LOGOUT -------")
        self.alza_module.logout(self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path, True)

    def test_basket_add_remove_item(self):
        """Tests adding and removing item from basket:
        - Reject all cookies and log in, check that login dialog disappears and correct user e-mail is displayed
        in the top section of the screen. If there are items in basket, remove them.
        - Add computer to basket and check number of items at basket icon.
        - Go to basket, check name of item present, its count and price.
        - Remove item from basket, check that basket is empty and there is no number at basket icon.
        - Log out, check that login link is displayed in the top section of the screen.
        """
        self.top_section = TopSection(self.driver)
        self.main_page = MainPage(self.driver)
        self.basket_page = Basket(self.driver)
        self.alza_module = AlzaModule(self.driver)

        # Reject all cookies and log into application.
        logger.info("------- REJECT ALL COOKIES AND LOG IN -------")
        self.alza_module.reject_all_cookies_and_login(self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Precondition: Empty basket if there are items inside and go back to Alza main page.
        logger.info("------- PRECONDITION: EMPTY BASKET IF THERE ARE ITEMS AND GO BACK TO ALZA MAIN PAGE -------")
        self.alza_module.empty_basket_if_items_inside()

        # Putting into basket:
        # Navigate to computers.
        logger.info("------- GO TO COMPUTERS, PUT FIRST COMPUTER INTO BASKET -------")
        self.main_page.hover_click_computers_notebooks_menu_item()
        self.main_page.click_computers_tile()
        # Get first computer name and price, put computer into basket.
        first_computer_name = self.main_page.get_first_computer_name()
        first_computer_price = self.main_page.get_first_computer_price()
        self.main_page.click_first_computer_put_to_basket_button()
        # Check there is correct number at basket icon and go to basket.
        logger.info("------- CHECK NUMBER OF ITEMS AT BASKET ICON AND GO TO BASKET -------")
        actual_number_of_items_at_basket_icon = self.top_section.get_number_of_items_at_basket_icon()
        mixed_assert.equal(actual_number_of_items_at_basket_icon, test_data.number_of_items_in_basket, f"Number of items at basket icon is correct: '{actual_number_of_items_at_basket_icon}'.", f"Wrong number of items at basket icon. Actual number is '{actual_number_of_items_at_basket_icon}' but it shall be '{test_data.number_of_items_in_basket}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        self.top_section.click_basket_icon()

        # On basket page:
        # Check item name, count and price.
        logger.info("------- BASKET: CHECK CORRECT ITEM IS IN BASKET -------")
        actual_computer_name = self.basket_page.get_item_name()
        mixed_assert.is_in(first_computer_name, actual_computer_name, f"Name of computer in basket is correct: '{actual_computer_name}'.", f"Wrong name of computer in basket. Actual name is '{actual_computer_name}' but it shall be '{first_computer_name}'. Seems computer that shall be in basket is not.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        actual_number_of_computers_in_basket = self.basket_page.get_item_count()
        mixed_assert.equal(actual_number_of_computers_in_basket, test_data.number_of_items_in_basket, f"Number of computers in basket is correct: '{actual_number_of_computers_in_basket}'.", f"Wrong number of computers in basket. There are '{actual_number_of_computers_in_basket}' computers but there shall be '{test_data.number_of_items_in_basket}' computer.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        actual_computer_price_in_basket = self.basket_page.get_item_price()
        mixed_assert.equal(actual_computer_price_in_basket, first_computer_price, f"Computer price in basket is correct: '{actual_computer_price_in_basket}'.", f"Wrong computer price in basket. Actual price is '{actual_computer_price_in_basket}' but shall be '{first_computer_price}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        # Remove item from basket and check it is empty.
        logger.info("------- BASKET: REMOVE ALL ITEMS FROM BASKET AND CHECK THE BASKET IS EMPTY -------")
        self.basket_page.remove_all_items_from_basket()
        actual_text_once_basket_empty = self.basket_page.get_text_once_all_items_removed()
        mixed_assert.equal(actual_text_once_basket_empty, test_data.text_once_all_items_removed_from_basket, f"Text once basket is empty is correct: '{actual_text_once_basket_empty}'.", f"Wrong text once basket is empty. Actual text is '{actual_text_once_basket_empty}' but it shall be '{test_data.text_once_all_items_removed_from_basket}'. Seems basket is not empty.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        # Check there is no number at basket icon.
        actual_number_of_items_at_basket_icon = self.top_section.get_number_of_items_at_basket_icon()
        mixed_assert.equal(actual_number_of_items_at_basket_icon, "No items", "There are correctly no items at basket icon.", f"Wrong number of items at basket icon. Actual number is '{actual_number_of_items_at_basket_icon}' but there shall be no items.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Logout.
        logger.info("------- LOGOUT -------")
        self.alza_module.logout(self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

    def test_search(self):
        """Tests searching via search button and by clicking suggestion:
        - Reject all cookies and log in, check that login dialog disappears and correct user e-mail is displayed
        in the top section of the screen.
        - Type "jízdní kola" into search input, press search button. Check that header of result page is "jízdní kola" and that amount of items found
        is bigger than 0.
        - Type "recenze" into search box, wait for suggestions to appear. Click first suggestion in suggestions and check that header of result page contains
        word "recenze".
        - Log out, check that login link is displayed in the top section of the screen.
        """
        self.top_section = TopSection(self.driver)
        self.main_page = MainPage(self.driver)
        self.alza_module = AlzaModule(self.driver)

        # Reject all cookies and log into application.
        logger.info("------- REJECT ALL COOKIES AND LOG IN -------")
        self.alza_module.reject_all_cookies_and_login(self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Search for "jízdní kola" and click search button:
        logger.info("------- LOOK UP 'JÍZDNÍ KOLA' VIA 'HLEDAT' BUTTON AND CHECK RESULT -------")
        self.top_section.search_provide_value(test_data.search_value_via_search_button)
        self.top_section.click_search_button()
        # Check result.
        actual_search_result_title = self.main_page.get_search_result_header()
        mixed_assert.equal(actual_search_result_title, test_data.search_result_header_via_search_button, f"Displayed header of looked up section is correct: '{actual_search_result_title}'.", f"Wrong header of looked up section is displayed. Actual header is '{actual_search_result_title}' but it shall be '{test_data.search_result_header_via_search_button}'. Seems wrong section is displayed.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        mixed_assert.greater(self.main_page.get_search_result_items_number(), 0, "There are correctly items found.", "No items found, items shall be found.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Search for "recenze" and choose from suggestions:
        logger.info("------- LOOK UP 'RECENZE' VIA FIRST SUGGESTION AND CHECK RESULT -------")
        self.top_section.search_provide_value(test_data.search_value_via_suggestion)
        self.top_section.search_suggestion_click_1st_item()
        # Check result.
        actual_search_result_title = self.main_page.get_search_result_header().lower()
        mixed_assert.is_in(test_data.search_result_word_in_title_via_suggestion, actual_search_result_title, f"Result title: '{actual_search_result_title}' correctly contains looked up word: '{test_data.search_result_word_in_title_via_suggestion}'.", f"Result doesn't contain looked up word in title. Actual title is '{actual_search_result_title}', it does not contain word '{test_data.search_result_word_in_title_via_suggestion}' though it shall.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Logout.
        logger.info("------- LOGOUT -------")
        self.alza_module.logout(self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

    def test_watchdogs_add_remove_item(self):
        """Tests adding and removing item from watchdogs page:
        - Reject all cookies and log in, check that login dialog disappears and correct user e-mail is displayed
        in the top section of the screen. If there are items at watchdogs page, remove them.
        - Add watchdog to pet supply item, go to watchdogs page. Check name of item present, its price limit and that checkbox for alerting when price
        decreases under price limit is checked.
        - Remove item from watchdogs page, check that watchdogs page is empty.
        - Log out, check that login link is displayed in the top section of the screen.
        """
        self.top_section = TopSection(self.driver)
        self.main_page = MainPage(self.driver)
        self.my_account_page = MyAccount(self.driver)
        self.watchdogs_page = Watchdogs(self.driver)
        self.watchdog_add_dialog = WatchdogAdd(self.driver)
        self.item_page = ItemPage(self.driver)
        self.alza_module = AlzaModule(self.driver)

        # Reject all cookies and log into application, stop test execution if login failed.
        logger.info("------- REJECT ALL COOKIES AND LOG IN -------")
        self.alza_module.reject_all_cookies_and_login(self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path, True)

        # Precondition: Empty watchdogs page if there are watched items and go back to Alza main page.
        logger.info("------- PRECONDITION: EMPTY WATCHDOGS PAGE IF THERE ARE ITEMS AND GO BACK TO ALZA MAIN PAGE -------")
        self.alza_module.empty_watchdogs_page_if_watched_items()

        # Navigate to pet supplies, open first pet supply, handle restricted dialog if appears and get supply name.
        logger.info("------- GO TO PET SUPPLIES, AT FIRST PET SUPPLY SET WATCHDOG -------")
        self.main_page.hover_click_pet_supplies_menu_item()
        self.main_page.click_first_pet_supply_item()
        self.item_page.close_pet_supply_restricted_dialog_if_present()
        first_pet_supply_name = self.item_page.get_pet_supply_name()

        # Watchdog dialog:
        self.item_page.click_watch_price_link()
        # Check prefilled e-mail address.
        actual_email = self.watchdog_add_dialog.get_email()
        mixed_assert.equal(actual_email, test_data.user_name, f"Prefilled e-mail address is correct: '{actual_email}'.", f"Incorrect e-mail address prefilled. There is '{actual_email}' but there shall be '{test_data.user_name}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        # Set watch price, confirm and close success popup.
        self.watchdog_add_dialog.set_price_limit(test_data.watchdog_price_limit)
        self.watchdog_add_dialog.click_confirm_button()
        self.item_page.close_watchdog_success_add_note()

        # Check watchdogs page and remove item:
        # Go to watchdogs page.
        logger.info("------- GO TO WATCHDOGS PAGE AND CHECK THERE IS CORRECT ITEM WITH CORRECT WATCHDOG DATA -------")
        self.top_section.click_signed_in_user_link()
        self.top_section.click_my_profile_link()
        self.my_account_page.click_watchdogs_menu_item()
        # Check watched item name and price limit, checkbox alert price is checked.
        actual_pet_supply_name = self.watchdogs_page.get_watchdog_item_name()
        mixed_assert.is_in(first_pet_supply_name, actual_pet_supply_name, f"Name of pet supply in watchdogs is correct: '{actual_pet_supply_name}'.", f"Wrong name of pet supply in watchdogs. Actual pet supply name is '{actual_pet_supply_name}' but it shall be '{first_pet_supply_name}'. Seems pet supply that shall be in watchdogs is not.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        actual_price_limit = self.watchdogs_page.get_price_limit_provided()
        mixed_assert.equal(actual_price_limit, test_data.watchdog_price_limit, f"Price limit in watchdogs is correct: '{actual_price_limit}'.", f"Wrong price limit displayed in watchdogs. Actual price limit is '{actual_price_limit}' but it shall be '{test_data.watchdog_price_limit}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        mixed_assert.is_true(self.watchdogs_page.check_alert_price_is_checked(), f"Checkbox for alert when price is lower than '{test_data.watchdog_price_limit}' is correctly checked.", f"Checkbox for alert when price is lower than '{test_data.watchdog_price_limit}' shall be checked but it is not.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        # Remove item from watchdogs page.
        logger.info("------- WATCHDOGS PAGE: REMOVE ALL ITEMS FROM WATCHDOGS PAGE AND CHECK IT IS EMPTY -------")
        self.watchdogs_page.remove_all_items_from_watchdogs_page()
        actual_text_once_watchdogs_page_empty = self.watchdogs_page.get_text_once_all_items_removed()
        mixed_assert.equal(actual_text_once_watchdogs_page_empty, test_data.text_once_all_items_removed_from_watchdogs_page, f"Text once watchdogs page is empty is correct: '{actual_text_once_watchdogs_page_empty}'.", f"Wrong text once watchdogs page is empty. Actual text is '{actual_text_once_watchdogs_page_empty}' but it shall be '{test_data.text_once_all_items_removed_from_watchdogs_page}'. Seems watchdogs page is not empty.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Logout.
        logger.info("------- LOGOUT -------")
        self.alza_module.logout(self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

    def test_delivery_addresses_add_remove_addresses(self):
        """Tests adding and removing addresses from delivery addresses page:
        - Reject all cookies and log in, check that login dialog disappears and correct user e-mail is displayed
        in the top section of the screen. If there are addresses at delivery addresses page, remove them.
        - Add 2 delivery addresses, go to main page, then back to delivery addresses page. Check number of delivery addresses and that at both all provided
        data is correct.
        - Edit data at both addresses, go to main page, then back to delivery addresses page. Check that at both addresses all edited data is correct.
        - Remove both addresses from delivery addresses page and check that delivery addresses page is empty.
        - Log out, check that login link is displayed in the top section of the screen.
        Note: Number of addresses can be changed by adding or removing dictionaries from delivery_addresses_original and delivery_addresses_edited in test_data.py.
        """
        self.top_section = TopSection(self.driver)
        self.delivery_addresses_page = DeliveryAddresses(self.driver)
        self.my_account_page = MyAccount(self.driver)
        self.alza_module = AlzaModule(self.driver)

        # Reject all cookies and log into application, stop test execution if login failed.
        logger.info("------- REJECT ALL COOKIES AND LOG IN -------")
        self.alza_module.reject_all_cookies_and_login(self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path, True)

        # Adding delivery addresses:
        # Go to delivery addresses page:
        logger.info("------- GO TO DELIVERY ADDRESSES PAGE -------")
        self.top_section.click_signed_in_user_link()
        self.top_section.click_my_profile_link()
        self.my_account_page.click_delivery_addresses_menu_item()
        # Precondition: Empty delivery addresses page if there are addresses.
        logger.info("------- PRECONDITION: EMPTY DELIVERY ADDRESSES PAGE IF THERE ARE ADDRESSES -------")
        self.delivery_addresses_page.remove_all_addresses_from_delivery_addresses_page()
        # Add 2 delivery addresses.
        logger.info("------- DELIVERY ADDRESSES PAGE: ADD 2 ADDRESSES -------")
        self.alza_module.delivery_addresses_add_addresses()

        # Go to Alza main page and back to delivery addresses and check added addresses are present with correct data:
        logger.info("------- GO TO ALZA MAIN PAGE, BACK TO DELIVERY ADDRESSES PAGE AND CHECK THERE ARE ADDED ADDRESSES WITH CORRECT DATA -------")
        self.top_section.click_alza_icon()
        # Go to delivery addresses page.
        self.top_section.click_signed_in_user_link()
        self.top_section.click_my_profile_link()
        self.my_account_page.click_delivery_addresses_menu_item()
        # Check number of addresses and their data.
        actual_number_of_delivery_addresses = self.delivery_addresses_page.get_number_of_addresses()
        expected_number_of_delivery_addresses = len(test_data.delivery_addresses_original)
        mixed_assert.equal(actual_number_of_delivery_addresses, expected_number_of_delivery_addresses, f"Number of delivery addresses is correct: '{actual_number_of_delivery_addresses}'.", f"Incorrect number of delivery addresses. Actual number is '{actual_number_of_delivery_addresses}' but it shall be '{expected_number_of_delivery_addresses}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
        actual_delivery_addresses_data = self.delivery_addresses_page.get_addresses_data(actual_number_of_delivery_addresses)
        mixed_assert.equal(actual_delivery_addresses_data, test_data.delivery_addresses_original, f"Actual delivery addresses are correctly the same as provided delivery addresses: '{actual_delivery_addresses_data}'.", f"Actual delivery addresses are not the same as provided delivery addresses. Actual delivery addresses are '{actual_delivery_addresses_data}', expected delivery addresses are '{test_data.delivery_addresses_original}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Editing delivery addresses:
        logger.info("------- EDIT ADDRESSES, GO TO ALZA MAIN PAGE, BACK TO DELIVERY ADDRESSES PAGE AND CHECK THERE ARE ADDRESSES WITH CORRECT EDITED DATA -------")
        self.alza_module.delivery_addresses_edit_addresses()
        # Go to Alza main page.
        self.top_section.click_alza_icon()
        # Go to delivery addresses page.
        self.top_section.click_signed_in_user_link()
        self.top_section.click_my_profile_link()
        self.my_account_page.click_delivery_addresses_menu_item()
        # Check addresses have correct edited data.
        actual_delivery_addresses_data = self.delivery_addresses_page.get_addresses_data(actual_number_of_delivery_addresses)
        mixed_assert.equal(actual_delivery_addresses_data, test_data.delivery_addresses_edited, f"Actual delivery addresses are correctly the same as updated delivery addresses: '{actual_delivery_addresses_data}'.", f"Actual delivery addresses are not the same as updated delivery addresses. Actual delivery addresses are '{actual_delivery_addresses_data}', expected delivery addresses are '{test_data.delivery_addresses_edited}'.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Remove delivery addresses:
        logger.info("------- DELIVERY ADDRESSES PAGE: REMOVE ALL ADDRESSES FROM DELIVERY ADDRESSES PAGE AND CHECK IT IS EMPTY -------")
        self.delivery_addresses_page.remove_all_addresses_from_delivery_addresses_page()
        # Check there are no addresses.
        actual_number_of_delivery_addresses = self.delivery_addresses_page.get_number_of_addresses()
        mixed_assert.equal(actual_number_of_delivery_addresses, 0, f"There are correctly no delivery addresses present.", f"There are delivery addresses present though there shall not be any. There are '{actual_number_of_delivery_addresses}' delivery addresses.", self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)

        # Logout.
        logger.info("------- LOGOUT -------")
        self.alza_module.logout(self.driver, self.report_screenshots_folder, self.tmp_test_urls_file_path)
