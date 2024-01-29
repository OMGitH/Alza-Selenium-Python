from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class TopSection(ElementHandler):

    # Identification of elements in top section of the page.
    login_link = (By.XPATH, "//span[@data-testid='headerContextMenuToggleLogin']")
    alza_main_page_icon = (By.XPATH, "//a[@data-testid='headerLogo']")
    my_profile_link = (By.XPATH, "//a[@data-testid='headerNavigationMyProfile']/span")
    signed_in_user_link = (By.XPATH, "//button[@data-testid='headerContextMenuToggle']")
    logout_link = (By.XPATH, "//span[@data-testid='headerNavigationLogout']/*[name()='svg']")
    alzaplus_image = (By.XPATH, "//img[contains(@src, 'Logo-AlzaPlus')]")
    search_input = (By.XPATH, "//input[@data-testid='searchInput']")
    search_button = (By.XPATH, "//button[@data-testid='button-search']")
    search_suggestion = (By.XPATH, "//div[@data-testid='searchResultsContainer']")
    search_suggestion_1st_item = (By.XPATH, "//div[contains(@data-testid, 'section')][1]/a[@data-testid='suggestion-item'][1]//span[text()]")
    search_suggestion_show_all_results_button = (By.XPATH, "//a[@data-testid='button-showAllResults']")
    basket_icon = (By.XPATH, "//a[@data-testid='headerBasketIcon']")
    basket_icon_item_inside = (By.XPATH, "//a[@data-testid='headerBasketIcon']//span")

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
        if self.element_handler_is_visible(self.logout_link):
            self.element_handler_click(self.logout_link, "'Odhlásit se' link", True)

    def search_provide_value(self, value):
        self.element_handler_clear_input_by_pressing_backspace(self.search_input, "value", "search input field", True)
        self.element_handler_send_keys(self.search_input, value, "search input field", True)
        self.element_handler_is_visible(self.search_suggestion)

    def click_search_button(self):
        self.element_handler_click(self.search_button, "'Hledat' button", True)
        self.element_handler_is_invisible(self.search_suggestion)

    def search_suggestion_click_1st_item(self):
        if self.element_handler_is_visible(self.search_suggestion_1st_item) and self.element_handler_is_visible(self.search_suggestion_show_all_results_button):
            self.element_handler_click(self.search_suggestion_1st_item, "Search suggestion 1st item", True)
        self.element_handler_is_invisible(self.search_suggestion)

    def login_link_is_visible(self):
        flag = self.element_handler_is_visible(self.login_link, handle_timeout_exception=True)
        return flag

    def get_signed_in_user_text(self):
        if self.element_handler_is_visible(self.signed_in_user_link):
            signed_in_user_text = self.element_handler_get_element_text(self.signed_in_user_link)
            return signed_in_user_text

    def click_signed_in_user_link(self):
        self.element_handler_click(self.signed_in_user_link, "Signed in user link", True)
        self.element_handler_is_visible(self.alzaplus_image)

    def click_basket_icon(self):
        self.element_handler_click(self.basket_icon, "Basket icon", True)

    def check_if_basket_is_not_empty(self):
        flag = self.element_handler_is_visible(self.basket_icon_item_inside, 3, True)
        return flag

    def get_number_of_items_at_basket_icon(self):
        if self.check_if_basket_is_not_empty():
            number_of_items = self.element_handler_get_element_text(self.basket_icon_item_inside)
            return int(number_of_items)
        else:
            return "No items"
