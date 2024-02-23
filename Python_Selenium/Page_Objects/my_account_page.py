from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class MyAccount(ElementHandler):

    # Identification of elements on my account page.
    watchdogs_menu_item = (By.XPATH, "//a[@data-testid='menuButton-UserWatchDog']")
    delivery_addresses_menu_item = (By.XPATH, "//a[@data-testid='menuButton-DeliveryAddresses']")

    # Actions on my account page.
    def click_watchdogs_menu_item(self):
        self.element_handler_click(self.watchdogs_menu_item, "'Hlídací psi' menu item", True)

    def click_delivery_addresses_menu_item(self):
        self.element_handler_click(self.delivery_addresses_menu_item, "'Doručovací adresy' menu item", True)
