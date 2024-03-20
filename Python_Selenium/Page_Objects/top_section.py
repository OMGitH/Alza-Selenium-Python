from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class TopSection(ElementHandler):

    # Identification of elements in top section of the page.
    login_link = (By.CSS_SELECTOR, "[data-testid='headerContextMenuToggleLogin']")
    alza_main_page_icon = (By.CSS_SELECTOR, "[data-testid='headerLogo']")
    my_profile_link = (By.CSS_SELECTOR, "[data-testid='headerNavigationMyProfile'] span")
    signed_in_user_link = (By.CSS_SELECTOR, "[data-testid='headerContextMenuToggle']")
    logout_link_icon = (By.CSS_SELECTOR, "[data-testid='headerNavigationLogout'] svg")
    alzaplus_image = (By.CSS_SELECTOR, "img[src*='Logo-AlzaPlus']")
    search_input = (By.CSS_SELECTOR, "input[data-testid='searchInput']")
    search_button = (By.CSS_SELECTOR, "[data-testid='button-search']")
    search_suggestions = (By.CSS_SELECTOR, "[data-testid='searchResultsContainer']")
    search_suggestions_1st_item = (By.XPATH, "(//a[@data-testid='suggestion-item']//span[text()])[1]")
    search_suggestions_show_all_results_button = (By.CSS_SELECTOR, "[data-testid='button-showAllResults']")
    basket_icon = (By.CSS_SELECTOR, "[data-testid='headerBasketIcon']")
    basket_icon_item_inside = (By.CSS_SELECTOR, "[data-testid='headerBasketIcon'] span")

    # Actions in top section of the page.
    def click_login_link(self):
        self.element_handler_click(self.login_link, "'Přihlásit se' link", True)

    def click_alza_icon(self):
        self.element_handler_click(self.alza_main_page_icon, "'alza.cz' icon", True)

    def click_my_profile_link(self):
        self.element_handler_click(self.my_profile_link, "'Můj profil' link", True)

    def click_logout_link_icon(self):
        if self.element_handler_is_visible(self.logout_link_icon, "'Odhlásit se' link icon"):
            self.element_handler_click(self.logout_link_icon, "'Odhlásit se' link icon", True)

    def search_provide_value(self, value):
        self.element_handler_clear_input_by_pressing_backspace(self.search_input, "value", "Search input field", True)
        self.element_handler_send_keys(self.search_input, value, "Search input field", True)
        self.element_handler_is_visible(self.search_suggestions, "Search suggestions")

    def click_search_button(self):
        self.element_handler_click(self.search_button, "'Hledat' button", True)
        self.element_handler_is_invisible(self.search_suggestions, "Search suggestions")

    def search_suggestion_click_1st_item(self):
        if self.element_handler_is_visible(self.search_suggestions_1st_item, "Search suggestions 1st item") and self.element_handler_is_visible(self.search_suggestions_show_all_results_button, "'Zobrazit všechny výsledky' button"):
            self.element_handler_click(self.search_suggestions_1st_item, "Search suggestions 1st item", True)
        self.element_handler_is_invisible(self.search_suggestions, "Search suggestions")

    def login_link_is_visible(self):
        flag = self.element_handler_is_visible(self.login_link, "'Přihlásit se' link", handle_timeout_exception=True)
        return flag

    def get_signed_in_user_text(self):
        if self.element_handler_is_visible(self.signed_in_user_link, "Signed in user link"):
            signed_in_user_text = self.element_handler_get_element_text(self.signed_in_user_link, "Signed in user link text")
            return signed_in_user_text

    def click_signed_in_user_link(self):
        self.element_handler_click(self.signed_in_user_link, "Signed in user link", True)
        self.element_handler_is_visible(self.alzaplus_image, "Alzaplus image")

    def click_basket_icon(self):
        self.element_handler_click(self.basket_icon, "Basket icon", True)

    def check_if_basket_is_not_empty(self):
        flag = self.element_handler_is_visible(self.basket_icon_item_inside, "Number of items at basket icon", 3, True)
        return flag

    def get_number_of_items_at_basket_icon(self):
        if self.check_if_basket_is_not_empty():
            number_of_items = self.element_handler_get_element_text(self.basket_icon_item_inside, "Number of items at basket icon")
            return int(number_of_items)
        else:
            return "No items"
