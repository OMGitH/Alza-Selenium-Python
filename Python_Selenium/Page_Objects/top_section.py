from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class TopSection(ElementHandler):

    # Identification of elements in top section of the page.
    login_link = {
        "locator": (By.CSS_SELECTOR, "[data-testid='headerContextMenuToggleLogin']"),
        "name": "'Přihlásit se' link"
    }
    alza_main_page_icon = {
        "locator": (By.CSS_SELECTOR, "[data-testid='headerLogo']"),
        "name": "'alza.cz' icon"
    }
    my_profile_link = {
        "locator": (By.CSS_SELECTOR, "[data-testid='headerNavigationMyProfile'] span"),
        "name": "'Můj profil' link"
    }
    signed_in_user_link = {
        "locator": (By.CSS_SELECTOR, "[data-testid='headerContextMenuToggle']"),
        "name": "Signed in user link"
    }
    logout_link_icon = {
        "locator": (By.CSS_SELECTOR, "[data-testid='headerNavigationLogout'] svg"),
        "name": "'Odhlásit se' link icon"
    }
    alzaplus_image = {
        "locator": (By.CSS_SELECTOR, "img[src*='Logo-AlzaPlus']"),
        "name": "Alzaplus image"
    }
    search_input = {
        "locator": (By.CSS_SELECTOR, "input[data-testid='searchInput']"),
        "name": "Search input field"
    }
    search_button = {
        "locator": (By.CSS_SELECTOR, "[data-testid='button-search']"),
        "name": "'Hledat' button"
    }
    search_suggestions = {
        "locator": (By.CSS_SELECTOR, "[data-testid='searchResultsContainer']"),
        "name": "Search suggestions"
    }
    search_suggestions_1st_item = {
        "locator": (By.XPATH, "(//a[@data-testid='suggestion-item']//span[text()])[1]"),
        "name": "Search suggestions 1st item"
    }
    search_suggestions_show_all_results_button = {
        "locator": (By.CSS_SELECTOR, "[data-testid='button-showAllResults']"),
        "name": "'Zobrazit všechny výsledky' button"
    }
    basket_icon = {
        "locator": (By.CSS_SELECTOR, "[data-testid='headerBasketIcon']"),
        "name": "Basket icon"
    }
    number_of_items_basket_icon = {
        "locator": (By.CSS_SELECTOR, "[data-testid='headerBasketIcon'] span"),
        "name": "Number of items at basket icon"
    }

    # Actions in top section of the page.
    def click_login_link(self):
        self.element_handler_click(self.login_link["locator"], self.login_link["name"], True)

    def click_alza_icon(self):
        self.element_handler_click(self.alza_main_page_icon["locator"], self.alza_main_page_icon["name"], True)

    def click_my_profile_link(self):
        self.element_handler_click(self.my_profile_link["locator"], self.my_profile_link["name"], True)

    def click_logout_link_icon(self):
        self.element_handler_click(self.logout_link_icon["locator"], self.logout_link_icon["name"], True)

    def search_provide_value(self, value):
        self.element_handler_clear_input_by_pressing_backspace(self.search_input["locator"], "value", self.search_input["name"], True)
        self.element_handler_send_keys(self.search_input["locator"], value, self.search_input["name"], True)
        self.element_handler_is_visible(self.search_suggestions["locator"], self.search_suggestions["name"])

    def click_search_button(self):
        self.element_handler_click(self.search_button["locator"], self.search_button["name"], True)
        self.element_handler_is_invisible(self.search_suggestions["locator"], self.search_suggestions["name"])

    def search_suggestion_click_1st_item(self):
        if self.element_handler_is_visible(self.search_suggestions_1st_item["locator"], self.search_suggestions_1st_item["name"]) and self.element_handler_is_visible(self.search_suggestions_show_all_results_button["locator"], self.search_suggestions_show_all_results_button["name"]):
            self.element_handler_click(self.search_suggestions_1st_item["locator"], self.search_suggestions_1st_item["name"], True)
        self.element_handler_is_invisible(self.search_suggestions["locator"], self.search_suggestions["name"])

    def login_link_is_visible(self):
        flag = self.element_handler_is_visible(self.login_link["locator"], self.login_link["name"], handle_timeout_exception=True)
        return flag

    def get_signed_in_user_text(self):
        signed_in_user_text = self.element_handler_get_element_text(self.signed_in_user_link["locator"], f"Text of {self.signed_in_user_link["name"]}")
        return signed_in_user_text

    def click_signed_in_user_link(self):
        self.element_handler_click(self.signed_in_user_link["locator"], self.signed_in_user_link["name"], True)
        self.element_handler_is_visible(self.alzaplus_image["locator"], self.alzaplus_image["name"])

    def click_basket_icon(self):
        self.element_handler_click(self.basket_icon["locator"], self.basket_icon["name"], True)

    def check_if_basket_is_not_empty(self):
        flag = self.element_handler_is_visible(self.number_of_items_basket_icon["locator"], self.number_of_items_basket_icon["name"], 3, True)
        return flag

    def get_number_of_items_at_basket_icon(self):
        if self.check_if_basket_is_not_empty():
            number_of_items = self.element_handler_get_element_text(self.number_of_items_basket_icon["locator"], self.number_of_items_basket_icon["name"])
            return int(number_of_items)
        else:
            return "No items"
