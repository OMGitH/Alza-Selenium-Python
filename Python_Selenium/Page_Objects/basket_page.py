from time import sleep
from selenium.webdriver.common.by import By
from element_handler import ElementHandler
from report_logger import logger
from Tests.test_data import text_once_all_items_removed_from_basket


class Basket(ElementHandler):

    # Identification of elements on basket page.
    item = (By.CLASS_NAME, "mainItem")
    item_count_text = (By.CSS_SELECTOR, "div.countEdit input")
    item_price_text = (By.CSS_SELECTOR, "tr[data-code] td.c5")
    down_arrow_price_button = (By.CLASS_NAME, "item-options__trigger")
    down_arrow_price_menu = (By.CSS_SELECTOR, "div.item-options__container[style='']")
    down_arrow_price_menu_remove_item = (By.CSS_SELECTOR, "div.item-options__container[style=''] li.item-options__option--del")
    all_items_removed_from_basket_text = (By.CSS_SELECTOR, "div#blocke span")

    # Actions on basket page.
    def get_item_name(self):
        item_name = self.element_handler_get_element_text(self.item, "Item name in basket")
        return item_name

    def get_item_count(self):
        item_count = self.element_handler_get_element_attribute(self.item_count_text, "value", "Item count in basket")
        return int(item_count)

    def get_item_price(self):
        item_price = self.element_handler_get_element_text(self.item_price_text, "Item price in basket")
        item_price = item_price.replace(" ", "")
        return item_price

    def get_text_once_all_items_removed(self):
        all_items_removed_message = self.element_handler_get_element_text(self.all_items_removed_from_basket_text, f"Text when basket is empty '{text_once_all_items_removed_from_basket}'")
        return all_items_removed_message

    def remove_all_items_from_basket(self, number_of_checks=10, check_wait=0.5):
        removed_items = 0
        while self.element_handler_get_state(self.down_arrow_price_button, self.all_items_removed_from_basket_text) == self.down_arrow_price_button:
            number_of_items = self.element_handler_get_number_of_visible_elements(self.down_arrow_price_button, "Down arrow price button")
            self.element_handler_click(self.down_arrow_price_button, "Down arrow price button", True)
            self.element_handler_click(self.down_arrow_price_menu_remove_item, "'Odstranit' down arrow price menu item", True)
            self.element_handler_is_invisible(self.down_arrow_price_menu, "Down arrow price menu")
            removed_items += 1
            # It seems Firefox doesn't wait for the basket page to be fully refreshed, following code waits for page to get refreshed.
            if number_of_items != 0:
                for _ in range(number_of_checks):
                    number_of_items_after_removal = self.element_handler_get_number_of_visible_elements(self.down_arrow_price_button, "Down arrow price button")
                    if number_of_items_after_removal == 0 or number_of_items_after_removal == number_of_items - 1:
                        break
                    sleep(check_wait)
        if removed_items > 0:
            logger.info(f"\t- {removed_items} item(s) removed from basket.")
