from selenium.webdriver.common.by import By
from element_handler import ElementHandler
import time


class TopSection(ElementHandler):

    # Identification of elements in top section of the page.
    login_link = (By.XPATH, "//span[@data-testid='headerContextMenuToggleLogin']")
    alza_main_page_icon = (By.XPATH, "//a[@data-testid='headerLogo']")
    my_profile_link = (By.XPATH, "//a[@data-testid='headerNavigationMyProfile']/span")
    signed_in_user_link = (By.XPATH, "//button[@data-testid='headerContextMenuToggle']")
    # signed_in_user_link = (By.XPATH, "//span[@data-testid='headerContextMenuToggleTitle']")
    signed_in_user_dialog = (By.XPATH, "//div[@data-testid='headerContextMenu']")
    logout_link = (By.XPATH, "//span[@data-testid='headerNavigationLogout']/*[name()='svg']")
    search_input = (By.XPATH, "//input[@data-testid='searchInput']")
    search_button = (By.XPATH, "//button[@data-testid='button-search']")
    search_suggestion = (By.XPATH, "//div[@data-testid='searchResultsContainer']")
    search_suggestion_1st_item = (By.XPATH, "//div[contains(@data-testid, 'section')][1]/a[@data-testid='suggestion-item'][1]")
    basket_icon = (By.XPATH, "//a[@data-testid='headerBasketIcon']")
    basket_icon_item_inside = (By.XPATH, "//a[@data-testid='headerBasketIcon']//span")
    basket_icon_empty = (By.XPATH, "//a[@data-testid='headerBasketIcon'][not(span)]")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions in top section of the page.
    def click_login_link(self):
        self.element_handler_click(self.login_link, "'Přihlásit se' link", True)

    def click_alza_icon(self):
        self.element_handler_click(self.alza_main_page_icon, "'alza.cz' icon", True)

    def click_my_profile_link(self):
        self.element_handler_click(self.my_profile_link, "'Můj profil' link", True)

    def click_logout_link(self):
        self.element_handler_click(self.logout_link, "'Odhlásit se' link", True)

    def search_provide_value(self, value):
        self.element_handler_clear_input_by_pressing_backspace(self.search_input, "value", "search input field", True)
        self.element_handler_send_keys(self.search_input, value, "search input field", True)
        self.element_handler_is_visible(self.search_suggestion)
        time.sleep(1)

    def click_search_button(self):
        self.element_handler_click(self.search_button, "'Hledat' button", True)

    def search_suggestion_click_1st_item(self):
        self.element_handler_is_visible(self.search_suggestion)
        self.element_handler_click(self.search_suggestion_1st_item, "Search suggestion 1st item", True)

    def login_link_is_visible(self):
        flag = self.element_handler_is_visible(self.login_link, handle_TimeoutException=True)
        return flag

    def get_signed_in_user_text(self):
        if self.element_handler_is_visible(self.signed_in_user_link):
            signed_in_user_text = self.element_handler_get_element_text(self.signed_in_user_link)
            return signed_in_user_text

    def click_signed_in_user_link(self):
        self.element_handler_click(self.signed_in_user_link, "Signed in user link", True)

    # It seems in Firefox sometimes signed in user link is clicked before page is fully loaded and dialog does not get displayed,
    # therefore method click until appears is used.
    # def click_signed_in_user_link(self):
    #     self.object_handler_click_until_appears(self.signed_in_user_link, self.signed_in_user_dialog)

    def click_basket_icon(self):
        self.element_handler_click(self.basket_icon, "Basket icon", True)

    def check_if_basket_is_not_empty(self):
        flag = self.element_handler_is_visible(self.basket_icon_item_inside, 2, True)
        return flag

    """
    Code below uses get state method that is faster as it doesn't wait for timeout to make sure whether or not there is an item
    identifying a state (if there is a number at basket icon, True is returned, if not, False is returned).
    """
    # def top_section_check_if_basket_not_empty(self):
    #     element_identifier = self.base_get_state(self.basket_icon_item_inside, self.basket_icon_empty)
    #     if element_identifier == self.basket_icon_item_inside:
    #         flag = True
    #     else:
    #         flag = False
    #     return flag

    def get_number_of_items_at_basket_icon(self):
        if self.check_if_basket_is_not_empty():
            number_of_items = self.element_handler_get_element_text(self.basket_icon_item_inside)
            return int(number_of_items)
        else:
            return "No items"

    # def top_section_get_number_of_items_at_basket_icon(self):
    #     number_of_items = self.base_get_element_text(self.basket_icon_item_inside)
    #     return int(number_of_items)
