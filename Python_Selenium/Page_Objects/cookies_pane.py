from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class CookiesPane(ElementHandler):

    # Identification of elements on cookies pane.
    cookies_pane = (By.CLASS_NAME, "cookies-info__container")
    reject_all_button = (By.CLASS_NAME, "js-cookies-info-reject")

    # Actions on cookies pane.
    def click_reject_all_button(self):
        self.element_handler_click(self.reject_all_button, "'Odmítnout vše' button", True)

    def cookies_pane_is_invisible(self, handle_timeout_exception=False):
        flag = self.element_handler_is_invisible(self.cookies_pane, handle_timeout_exception=handle_timeout_exception)
        return flag
