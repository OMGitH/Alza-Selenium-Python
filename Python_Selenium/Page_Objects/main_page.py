from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class MainPage(ElementHandler):

    # Identification of elements on main page.
    category_section_header_text = {
        "locator": (By.CSS_SELECTOR, "[class='categoryPage'] [itemprop='name']"),
        "computers notebooks name": "'Počítače a notebooky' section header",
        "pet supplies name": "'Chovatelské potřeby' section header"
    }
    computers_notebooks_menu_item = {
        "locator": (By.CSS_SELECTOR, "[href='/pocitace-a-notebooky']"),
        "name": "'Počítače a notebooky' menu item"
    }
    computers_tile = {
        "locator": (By.CSS_SELECTOR, "[href*='https://www.alza.cz/pocitace'] span"),
        "name": "'Počítače' tile"
    }
    first_computer_name_text = {
        "locator": (By.CSS_SELECTOR, "div.first.firstRow a.name"),
        "name": "First computer name"
    }
    first_computer_price_text = {
        "locator": (By.CSS_SELECTOR, "div.first.firstRow span.price-box__price"),
        "name": "First computer price"
    }
    first_computer_put_to_basket_button = {
        "locator": (By.CSS_SELECTOR, "div.first.firstRow a.btnk1"),
        "name": "'Do košíku' button at first computer"
    }
    first_computer_added_to_basket_text = {
        "locator": (By.CSS_SELECTOR, "div.first.firstRow div[style=''] span.js-count-text"),
        "name": "Text 'Přidáno do košíku' at first computer"
    }
    search_result_header_text = {
        "locator": (By.CSS_SELECTOR, ".categoryPageTitle [itemprop='name']"),
        "name": "Search result header"
    }
    search_result_number_of_items_found_text = {
        "locator": (By.ID, "lblNumberItem"),
        "name": "Number of items found"
    }
    pet_supplies_menu_item = {
        "locator": (By.CSS_SELECTOR, "[href='/pet']"),
        "name": "'Chovatelské potřeby' menu item"
    }
    first_pet_supply_item_name_link = {
        "locator": (By.CSS_SELECTOR, "div[data-react-client-component-id='carousel0'] swiper-slide.swiper-slide-active [data-testid='itemName']"),
        "name": "First pet supply item name link"
    }

    # Actions on main page.
    def hover_click_computers_notebooks_menu_item(self):
        self.element_handler_hover_click(self.computers_notebooks_menu_item["locator"], self.computers_notebooks_menu_item["name"], True)
        self.element_handler_is_visible(self.category_section_header_text["locator"], self.category_section_header_text["computers notebooks name"])

    def hover_click_pet_supplies_menu_item(self):
        self.element_handler_hover_click(self.pet_supplies_menu_item["locator"], self.pet_supplies_menu_item["name"], True)
        self.element_handler_is_visible(self.category_section_header_text["locator"], self.category_section_header_text["pet supplies name"])

    def click_computers_tile(self):
        self.element_handler_click(self.computers_tile["locator"], self.computers_tile["name"], True, 50)

    def click_first_pet_supply_item(self):
        self.element_handler_click(self.first_pet_supply_item_name_link["locator"], self.first_pet_supply_item_name_link["name"], True)

    def get_first_computer_name(self):
        first_computer_name = self.element_handler_get_element_text(self.first_computer_name_text["locator"], self.first_computer_name_text["name"])
        # It may happen there is a note in name, either inside "()", starting by "-" or with word "záruka" and following text. It is needed to remove such a note
        # as it is not present in item name inside basket.
        unwanted_texts = ["(", "-", "záruka"]
        for text in unwanted_texts:
            text_index = str(first_computer_name).find(text)
            if text_index != -1:
                first_computer_name = str(first_computer_name)[:text_index]
                first_computer_name = first_computer_name.strip()
        return first_computer_name

    def get_first_computer_price(self):
        first_computer_price = self.element_handler_get_element_text(self.first_computer_price_text["locator"], self.first_computer_price_text["name"])
        first_computer_price = first_computer_price.replace(" ", "")
        first_computer_price = first_computer_price.replace(",-", "Kč")
        return first_computer_price

    def click_first_computer_put_to_basket_button(self):
        self.element_handler_click(self.first_computer_put_to_basket_button["locator"], self.first_computer_put_to_basket_button["name"], True)
        self.element_handler_is_visible(self.first_computer_added_to_basket_text["locator"], self.first_computer_added_to_basket_text["name"])

    def get_search_result_header(self):
        result_header = self.element_handler_get_element_text(self.search_result_header_text["locator"], self.search_result_header_text["name"])
        return result_header

    def get_search_result_items_number(self):
        result_items_number = self.element_handler_get_element_text(self.search_result_number_of_items_found_text["locator"], self.search_result_number_of_items_found_text["name"])
        return int(result_items_number)
