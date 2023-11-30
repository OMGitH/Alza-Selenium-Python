from selenium.webdriver.common.by import By
from object_handler import ObjectHandler


class Basket(ObjectHandler):

    # Identification of objects on basket page.
    item = (By.CLASS_NAME, "mainItem")
    item_count_text = (By.XPATH, "//div[@class='countInput']//input")
    item_price_text = (By.XPATH, "//span[contains(@class, 'item-options') and not(text())]//ancestor::tr/td[@class='c5']")
    down_arrow_price_button = (By.XPATH, "//span[contains(@class, 'item-options') and not(text())]")
    down_arrow_price_remove_menu_item = (By.XPATH, "//div[@style='']//li[contains(@class, '-del')]")
    text_all_items_removed_from_basket = (By.XPATH, "//div[@id='blocke'][not(contains(@style, 'none'))]//span")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions on basket page.
    def basket_get_item_name(self):
        if self.object_handler_is_visible(self.item):
            item_name = self.object_handler_get_element_text(self.item)
            return item_name

    def basket_get_item_count(self):
        if self.object_handler_is_visible(self.item_count_text):
            item_count = self.object_handler_get_element_attribute_value(self.item_count_text, "value")
            return int(item_count)

    def basket_get_item_price(self):
        if self.object_handler_is_visible(self.item_price_text):
            item_price = self.object_handler_get_element_text(self.item_price_text)
            item_price = item_price.replace(" ", "")
            return item_price

    def basket_click_down_arrow_price(self):
        self.object_handler_click(self.down_arrow_price_button)

    def basket_click_down_arrow_price_remove(self):
        self.object_handler_click(self.down_arrow_price_remove_menu_item)

    def basket_get_text_once_all_items_removed(self):
        if self.object_handler_is_visible(self.text_all_items_removed_from_basket):
            all_items_removed_message = self.object_handler_get_element_text(self.text_all_items_removed_from_basket)
            return all_items_removed_message

    def basket_remove_all_items_from_basket(self):
        while self.object_handler_get_state(self.down_arrow_price_button, self.text_all_items_removed_from_basket) == self.down_arrow_price_button:
            self.object_handler_click(self.down_arrow_price_button)
            self.object_handler_click(self.down_arrow_price_remove_menu_item)

    # def basket_remove_all_items_from_basket(self):
    #     while self.base_is_visible(self.down_arrow_price_button, 1, True):
    #         self.base_click(self.down_arrow_price_button)
    #         self.base_click(self.down_arrow_price_remove_menu_item)
