from selenium.webdriver.common.by import By
from Page_objects.base_page import BasePage


class TopSection(BasePage):

    # Identification of objects in top section of the page.
    login_link = (By.XPATH, "//span[@data-testid='headerContextMenuToggleLogin']")
    alza_main_page_icon = (By.XPATH, "//a[@title='Alza']")
    user_profile_link = (By.ID, "lblUser")
    signed_in_user_link = (By.XPATH, "//span[@data-testid='headerContextMenuToggleTitle']")
    logout_link = (By.XPATH, "//span[@data-testid='headerNavigationLogout']")
    search_input = (By.ID, "edtSearch")
    search_button = (By.ID, "btnSearch")
    search_suggestion = (By.XPATH, "//ul[@id='ui-id-1'][not(contains(@style, 'none'))]")
    search_suggestion_1st_article = (By.XPATH, "//li[@class='t6 ui-menu-item'][1]")
    basket_icon = (By.XPATH, "//a[@data-testid='headerBasketIcon']")

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
        self.base_clear_input(self.search_input)
        self.base_send_keys(self.search_input, value)

    def top_section_click_search_button(self):
        self.base_click(self.search_button)

    def top_section_search_suggestion_click_1st_article(self):
        self.base_is_visible(self.search_suggestion)
        self.base_click(self.search_suggestion_1st_article)

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