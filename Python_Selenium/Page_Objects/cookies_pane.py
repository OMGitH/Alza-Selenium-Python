from object_handler import ObjectHandler
from selenium.webdriver.common.by import By


class CookiesPane(ObjectHandler):

    # Identification of objects on cookies pane.
    cookies_pane = (By.XPATH, "//div[@class='cookies-info__container']")
    reject_all_button = (By.XPATH, "//a[@data-action-id-value='0']")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions on cookies pane.
    def cookies_pane_click_reject_all(self):
        self.object_handler_click(self.reject_all_button)

    def cookies_pane_is_invisible(self):
        flag = self.object_handler_is_invisible(self.cookies_pane, handle_TimeoutException=True)
        return flag
