from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class ItemPage(ElementHandler):

    # Identification of elements on item page.
    pet_supply_restricted_dialog_agree_button = {
        "locator": (By.CSS_SELECTOR, "[data-testid='dialogRestrictedAgeAcceptButton']"),
        "name": "'Souhlasím' button at restricted dialog"
    }
    pet_supply_item_name_header_text = {
        "locator": (By.CSS_SELECTOR, "div.title-share [itemprop='name']"),
        "name": "Pet supply item header"
    }
    watch_price_link = {
        "locator": (By.CLASS_NAME, "watchproduct"),
        "name": "'Hlídat cenu' link"
    }
    watchdog_success_add_note_close_button = {
        "locator": (By.CSS_SELECTOR, "svg[class*='priceBox'][xmlns]"),
        "name": "'X' button at 'Hlídací pes nastaven.' note"
    }

    # Actions on item page.
    def close_pet_supply_restricted_dialog_if_present(self):
        if self.element_handler_is_visible(self.pet_supply_restricted_dialog_agree_button["locator"], self.pet_supply_restricted_dialog_agree_button["name"], 2, True):
            self.element_handler_click(self.pet_supply_restricted_dialog_agree_button["locator"], self.pet_supply_restricted_dialog_agree_button["name"], True)

    def get_pet_supply_name(self):
        pet_supply_item_name = self.element_handler_get_element_text(self.pet_supply_item_name_header_text["locator"], self.pet_supply_item_name_header_text["name"])
        return pet_supply_item_name

    def click_watch_price_link(self):
        self.element_handler_click(self.watch_price_link["locator"], self.watch_price_link["name"], True)

    def close_watchdog_success_add_note(self):
        self.element_handler_click(self.watchdog_success_add_note_close_button["locator"], self.watchdog_success_add_note_close_button["name"], True)
        self.element_handler_is_invisible(self.watchdog_success_add_note_close_button["locator"], self.watchdog_success_add_note_close_button["name"])
