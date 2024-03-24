from time import sleep
from selenium.webdriver.common.by import By
from element_handler import ElementHandler
from report_logger import logger
from Tests.test_data import text_once_all_items_removed_from_basket


class Basket(ElementHandler):

    # Identification of elements on basket page.
    item_name_link = {
        "locator": (By.CLASS_NAME, "mainItem"),
        "name": "Item name in basket"
    }
    item_count_text = {
        "locator": (By.CSS_SELECTOR, "div.countEdit input"),
        "name": "Item count in basket"
    }
    item_price_text = {
        "locator": (By.CSS_SELECTOR, "tr[data-code] td.c5"),
        "name": "Item price in basket"
    }
    down_arrow_price_button = {
        "locator": (By.CLASS_NAME, "item-options__trigger"),
        "name": "Down arrow price button"
    }
    down_arrow_price_menu = {
        "locator": (By.CSS_SELECTOR, "div.item-options__container[style='']"),
        "name": "Down arrow price menu"
    }
    down_arrow_price_menu_remove_item = {
        "locator": (By.CSS_SELECTOR, "div.item-options__container[style=''] li.item-options__option--del"),
        "name": "'Odstranit' down arrow price menu item"
    }
    all_items_removed_from_basket_text = {
        "locator": (By.CSS_SELECTOR, "div#blocke span"),
        "name": f"Text when basket is empty '{text_once_all_items_removed_from_basket}'"
    }

    # Actions on basket page.
    def get_item_name(self):
        item_name = self.element_handler_get_element_text(self.item_name_link["locator"], self.item_name_link["name"])
        return item_name

    def get_item_count(self):
        item_count = self.element_handler_get_element_attribute(self.item_count_text["locator"], "value", self.item_count_text["name"])
        return int(item_count)

    def get_item_price(self):
        item_price = self.element_handler_get_element_text(self.item_price_text["locator"], self.item_price_text["name"])
        item_price = item_price.replace(" ", "")
        return item_price

    def get_text_once_all_items_removed(self):
        all_items_removed_message = self.element_handler_get_element_text(self.all_items_removed_from_basket_text["locator"], self.all_items_removed_from_basket_text["name"])
        return all_items_removed_message

    def remove_all_items_from_basket(self, number_of_checks=10, check_wait=0.5):
        removed_items = 0
        while self.element_handler_get_state(self.down_arrow_price_button["locator"], self.all_items_removed_from_basket_text["locator"]) == self.down_arrow_price_button["locator"]:
            number_of_items = self.element_handler_get_number_of_visible_elements(self.down_arrow_price_button["locator"], self.down_arrow_price_button["name"])
            self.element_handler_click(self.down_arrow_price_button["locator"], self.down_arrow_price_button["name"], True)
            self.element_handler_click(self.down_arrow_price_menu_remove_item["locator"], self.down_arrow_price_menu_remove_item["name"], True)
            self.element_handler_is_invisible(self.down_arrow_price_menu["locator"], self.down_arrow_price_menu["name"])
            removed_items += 1
            # It seems Firefox doesn't wait for the basket page to be fully refreshed, following code waits for page to get refreshed.
            if number_of_items != 0:
                for _ in range(number_of_checks):
                    number_of_items_after_removal = self.element_handler_get_number_of_visible_elements(self.down_arrow_price_button["locator"], self.down_arrow_price_button["name"])
                    if number_of_items_after_removal == 0 or number_of_items_after_removal == number_of_items - 1:
                        break
                    sleep(check_wait)
        if removed_items > 0:
            logger.info(f"\t- {removed_items} item(s) removed from basket.")
