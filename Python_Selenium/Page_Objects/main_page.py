from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class MainPage(ElementHandler):

    # Identification of elements on main page.
    category_section_header_text = (By.CSS_SELECTOR, "[class='categoryPage'] [itemprop='name']")
    computers_notebooks_menu_item = (By.CSS_SELECTOR, "[href='/pocitace-a-notebooky']")
    computers_tile = (By.CSS_SELECTOR, "[href*='https://www.alza.cz/pocitace'] span")
    first_computer_name_text = (By.CSS_SELECTOR, "div.first.firstRow a.name")
    first_computer_price_text = (By.CSS_SELECTOR, "div.first.firstRow span.price-box__price")
    first_computer_put_to_basket_button = (By.CSS_SELECTOR, "div.first.firstRow a.btnk1")
    first_computer_added_to_basket_text = (By.CSS_SELECTOR, "div.first.firstRow div[style=''] span.js-count-text")
    search_result_header_text = (By.CSS_SELECTOR, ".categoryPageTitle [itemprop='name']")
    search_result_number_of_items_found_text = (By.ID, "lblNumberItem")
    pet_supplies_menu_item = (By.CSS_SELECTOR, "[href='/pet']")
    first_pet_supply_item_name_link = (By.CSS_SELECTOR, "div[data-react-client-component-id='carousel0'] swiper-slide.swiper-slide-active [data-testid='itemName']")
    sync_frame = (By.CSS_SELECTOR, "iframe[src*='creativecdn.com']")
    document_body_in_sync_frame = (By.CSS_SELECTOR, "body")

    # Actions on main page.
    def hover_click_computers_notebooks_menu_item(self):
        self.element_handler_hover_click(self.computers_notebooks_menu_item, "'Počítače a notebooky' menu item", True)
        self.element_handler_is_visible(self.category_section_header_text, "'Počítače a notebooky' section header")

    def hover_click_pet_supplies_menu_item(self):
        self.element_handler_hover_click(self.pet_supplies_menu_item, "'Chovatelské potřeby' menu item", True)
        self.element_handler_is_visible(self.category_section_header_text, "'Chovatelské potřeby' section header")

    def click_computers_tile(self):
        self.element_handler_click(self.computers_tile, "'Počítače' tile", True, 50)

    def click_first_pet_supply_item(self):
        self.element_handler_click(self.first_pet_supply_item_name_link, "First pet supply item name link", True)

    def get_first_computer_name(self):
        first_computer_name = self.element_handler_get_element_text(self.first_computer_name_text, "First computer name")
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
        first_computer_price = self.element_handler_get_element_text(self.first_computer_price_text, "First computer price")
        first_computer_price = first_computer_price.replace(" ", "")
        first_computer_price = first_computer_price.replace(",-", "Kč")
        return first_computer_price

    def click_first_computer_put_to_basket_button(self):
        self.element_handler_click(self.first_computer_put_to_basket_button, "'Do košíku' button at first computer", True)
        self.element_handler_is_visible(self.first_computer_added_to_basket_text, "Text 'Přidáno do košíku' at first computer")

    def get_search_result_header(self):
        result_header = self.element_handler_get_element_text(self.search_result_header_text, "Search result header")
        return result_header

    def get_search_result_items_number(self):
        result_items_number = self.element_handler_get_element_text(self.search_result_number_of_items_found_text, "Number of items found")
        return int(result_items_number)

    def main_page_loaded_after_cookies_rejected(self):
        self.element_handler_switch_to_frame(self.sync_frame)
        self.element_handler_is_visible(self.document_body_in_sync_frame, "Document body in sync frame")
        self.element_handler_switch_back_to_default_content()
