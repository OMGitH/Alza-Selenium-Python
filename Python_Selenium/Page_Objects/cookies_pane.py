from element_handler import ElementHandler
from selenium.webdriver.common.by import By


class CookiesPane(ElementHandler):

    # Identification of elements on cookies pane.
    cookies_pane = (By.XPATH, "//div[@class='cookies-info__container']")
    reject_all_link = (By.XPATH, "//a[@data-action-id-value='0']")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions on cookies pane.
    def click_reject_all_link(self):
        self.element_handler_click(self.reject_all_link, "'Odmítnout vše' link", True)

    def cookies_pane_is_invisible(self):
        flag = self.element_handler_is_invisible(self.cookies_pane, handle_TimeoutException=True)
        return flag
