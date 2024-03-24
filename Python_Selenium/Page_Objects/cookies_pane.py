from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class CookiesPane(ElementHandler):

    # Identification of elements on cookies pane.
    cookies_pane = {
        "locator": (By.CLASS_NAME, "cookies-info__container"),
        "name": "Cookies pane"
    }
    reject_all_button = {
        "locator": (By.CLASS_NAME, "js-cookies-info-reject"),
        "name": "'Odmítnout vše' button"
    }

    # Actions on cookies pane.
    def click_reject_all_button(self):
        self.element_handler_click(self.reject_all_button["locator"], self.reject_all_button["name"], True)

    def cookies_pane_is_invisible(self, handle_timeout_exception=False):
        flag = self.element_handler_is_invisible(self.cookies_pane["locator"], self.cookies_pane["name"], handle_timeout_exception=handle_timeout_exception)
        return flag
