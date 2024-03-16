from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class ItemPage(ElementHandler):

    # Identification of elements on item page.
    pet_supply_restricted_dialog_agree_button = (By.CSS_SELECTOR, "[data-testid='dialogRestrictedAgeAcceptButton']")
    pet_supply_item_name_header_text = (By.CSS_SELECTOR, "div.title-share [itemprop='name']")
    watch_price_link = (By.CLASS_NAME, "watchproduct")
    watchdog_success_add_note_close_button = (By.CSS_SELECTOR, "svg[class*='priceBox'][xmlns]")

    # Actions on item page.
    def close_pet_supply_restricted_dialog(self):
        if self.element_handler_is_visible(self.pet_supply_restricted_dialog_agree_button, 2, True):
            self.element_handler_click(self.pet_supply_restricted_dialog_agree_button, "'Souhlasím' button", True)

    def get_pet_supply_name(self):
        if self.element_handler_is_visible(self.pet_supply_item_name_header_text):
            pet_supply_name = self.element_handler_get_element_text(self.pet_supply_item_name_header_text)
            return pet_supply_name

    def click_watch_price_link(self):
        self.element_handler_click(self.watch_price_link, "'Hlídat cenu' link", True)

    def close_watchdog_success_add_note(self):
        self.element_handler_click(self.watchdog_success_add_note_close_button, "'X' button at 'Hlídací pes nastaven.' note", True)
        self.element_handler_is_invisible(self.watchdog_success_add_note_close_button)
