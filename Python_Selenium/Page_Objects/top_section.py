from selenium.webdriver.common.by import By
from Page_objects.base_page import BasePage
import time


class TopSection(BasePage):

    # Identification of objects in top section of the page.
    login_link = (By.XPATH, "//span[@data-testid='headerContextMenuToggleLogin']")
    alza_main_page_icon = (By.XPATH, "//a[@data-testid='headerLogo']")
    user_profile_link = (By.ID, "lblUser")
    signed_in_user_link = (By.XPATH, "//span[@data-testid='headerContextMenuToggleTitle']")
    logout_link = (By.XPATH, "//span[@data-testid='headerNavigationLogout']")
    search_input = (By.XPATH, "//input[@data-testid='searchInput']")
    search_button = (By.XPATH, "//button[@data-testid='button-search']")
    search_suggestion = (By.XPATH, "//div[@data-testid='searchResultsContainer']")
    search_suggestion_1st_item = (By.XPATH, "//div[contains(@data-testid, 'section')][1]/a[@data-testid='suggestion-item'][1]")
    basket_icon = (By.XPATH, "//a[@data-testid='headerBasketIcon']")
    basket_icon_item_inside = (By.XPATH, "//a[@data-testid='headerBasketIcon']//span")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions in top section of the page.
    def top_section_click_login_link(self):
        self.base_click(self.login_link)

    def top_section_click_alza_icon(self):
        self.base_click(self.alza_main_page_icon)

    def top_section_click_user_profile_link(self):
        self.base_click(self.user_profile_link)

    def top_section_click_logout_link(self):
        self.base_click(self.logout_link)

    def top_section_search_provide_value(self, value):
        self.base_clear_input_by_pressing_backspace(self.search_input, "value")
        self.base_send_keys(self.search_input, value)
        self.base_is_visible(self.search_suggestion)
        time.sleep(1)

    def top_section_click_search_button(self):
        self.base_click(self.search_button)

    def top_section_search_suggestion_click_1st_item(self):
        self.base_is_visible(self.search_suggestion)
        self.base_click(self.search_suggestion_1st_item)

    def top_section_login_link_is_visible(self):
        flag = self.base_is_visible(self.login_link)
        return flag

    def top_section_get_signed_in_user_text(self):
        if self.base_is_visible(self.signed_in_user_link):
            signed_in_user_text = self.base_get_element_text(self.signed_in_user_link)
            return signed_in_user_text

    def top_section_click_signed_in_user_link(self):
        self.base_click(self.signed_in_user_link)

    def top_section_click_basket_icon(self):
        self.base_click(self.basket_icon)

    def top_section_basket_is_not_empty(self):
        flag = self.base_is_visible(self.basket_icon_item_inside, 2)
        return flag