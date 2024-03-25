from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class MyAccount(ElementHandler):

    # Identification of elements on my account page.
    watchdogs_menu_item = {
        "locator": (By.CSS_SELECTOR, "[data-testid='menuButton-UserWatchDog']"),
        "name": "'Hlídací psi' menu item"
    }
    delivery_addresses_menu_item = {
        "locator": (By.CSS_SELECTOR, "[data-testid='menuButton-DeliveryAddresses']"),
        "name": "'Doručovací adresy' menu item"
    }
    sync_element = {
        "locator": (By.ID, "facebook-jssdk"),
        "name": "Sync element signaling page is loaded"
    }

    # Actions on my account page.
    def click_watchdogs_menu_item(self):
        self.element_handler_click(self.watchdogs_menu_item["locator"], self.watchdogs_menu_item["name"], True)

    def click_delivery_addresses_menu_item(self):
        self.element_handler_click(self.delivery_addresses_menu_item["locator"], self.delivery_addresses_menu_item["name"], True)
        self.element_handler_is_present(self.sync_element["locator"], self.sync_element["name"])
