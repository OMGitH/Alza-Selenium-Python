from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class MainPage(ElementHandler):

    # Identification of elements on main page.
    category_section_header_text = (By.CSS_SELECTOR, "[class='categoryPage'] [itemprop='name']")
    item_detail_page = (By.CSS_SELECTOR, "div.detail-page")
    computers_notebooks_menu_item = (By.CSS_SELECTOR, "[href='/pocitace-a-notebooky']")
    computers_tile = (By.CSS_SELECTOR, "[href*='https://www.alza.cz/pocitace'] span")
    first_computer_name_text = (By.CSS_SELECTOR, "div.first.firstRow a.name")
    first_computer_price_text = (By.CSS_SELECTOR, "div.first.firstRow span.price-box__price")
    first_computer_put_to_basket_button = (By.CSS_SELECTOR, "div.first.firstRow a.btnk1")
    first_computer_added_to_basket_text = (By.CSS_SELECTOR, "div.first.firstRow div[style=''] span.js-count-text")
    search_result_header_text = (By.CSS_SELECTOR, ".categoryPageTitle [itemprop='name']")
    search_result_number_of_items_found_text = (By.ID, "lblNumberItem")
    pet_supplies_menu_item = (By.CSS_SELECTOR, "[href='/pet']")
    pet_supply_restricted_dialog_agree_button = (By.CSS_SELECTOR, "[data-testid='dialogRestrictedAgeAcceptButton']")
    first_pet_supply_item_name_link = (By.CSS_SELECTOR, "div[data-react-client-component-id='carousel0'] swiper-slide.swiper-slide-active [data-testid='itemName']")
    first_pet_supply_item_name_header_text = (By.CSS_SELECTOR, "div.title-share [itemprop='name']")
    watch_price_link = (By.CLASS_NAME, "watchproduct")
    sync_frame = (By.CSS_SELECTOR, "iframe[src*='creativecdn.com']")
    document_body_in_sync_frame = (By.CSS_SELECTOR, "body")
    watchdog_success_add_note_close_button = (By.CSS_SELECTOR, "svg[class*='priceBox'][xmlns]")

    # Actions on main page.
    def hover_click_computers_notebooks_menu_item(self):
        self.element_handler_hover_click(self.computers_notebooks_menu_item, "'Počítače a notebooky' menu item", True)
        self.element_handler_is_visible(self.category_section_header_text)

    def hover_click_pet_supplies_menu_item(self):
        self.element_handler_hover_click(self.pet_supplies_menu_item, "'Chovatelské potřeby' menu item", True)
        self.element_handler_is_visible(self.category_section_header_text)

    def click_computers_tile(self):
        self.element_handler_click(self.computers_tile, "'Počítače' tile", True, 50)

    def click_first_pet_suppy_item(self):
        self.element_handler_click(self.first_pet_supply_item_name_link, "'Chovatelské potřeby' item", True)
        self.element_handler_is_visible(self.item_detail_page)

    def click_watch_price_link(self):
        self.element_handler_click(self.watch_price_link, "'Hlídat cenu' link", True)

    def get_first_computer_name(self):
        if self.element_handler_is_visible(self.first_computer_name_text):
            first_computer_name = self.element_handler_get_element_text(self.first_computer_name_text)
            # It may happen there is a note in name, either inside "()", starting by "-" or with word "záruka" and following text. It is needed to remove such a note
            # as it is not present in item name inside basket.
            unwanted_texts = ["(", "-", "záruka"]
            for text in unwanted_texts:
                text_index = str(first_computer_name).find(text)
                if text_index != -1:
                    first_computer_name = str(first_computer_name)[:text_index]
                    first_computer_name = first_computer_name.strip()
            return first_computer_name

    def get_first_pet_supply_name(self):
        if self.element_handler_is_visible(self.first_pet_supply_item_name_header_text):
            first_pet_supply_name = self.element_handler_get_element_text(self.first_pet_supply_item_name_header_text)
            return first_pet_supply_name

    def get_first_computer_price(self):
        if self.element_handler_is_visible(self.first_computer_price_text):
            price = self.element_handler_get_element_text(self.first_computer_price_text)
            price = price.replace(" ", "")
            price = price.replace(",-", "Kč")
            return price

    def click_first_computer_put_to_basket_button(self):
        self.element_handler_click(self.first_computer_put_to_basket_button, "'Do košíku' button", True)
        self.element_handler_is_visible(self.first_computer_added_to_basket_text)

    def get_search_result_header(self):
        if self.element_handler_is_visible(self.search_result_header_text):
            result_header = self.element_handler_get_element_text(self.search_result_header_text)
            return result_header

    def get_search_result_items_amount(self):
        if self.element_handler_is_visible(self.search_result_number_of_items_found_text):
            result_items_amount = self.element_handler_get_element_text(self.search_result_number_of_items_found_text)
            return int(result_items_amount)

    def pet_supply_close_dialog(self):
        if self.element_handler_is_visible(self.pet_supply_restricted_dialog_agree_button, 2, True):
            self.element_handler_click(self.pet_supply_restricted_dialog_agree_button, "'Souhlasím' button", True)

    def main_page_loaded_after_cookies_rejected(self):
        self.element_handler_switch_to_frame(self.sync_frame)
        self.element_handler_is_visible(self.document_body_in_sync_frame)
        self.element_handler_switch_back_from_frame()

    def close_watchdog_success_add_note(self):
        self.element_handler_click(self.watchdog_success_add_note_close_button, "'X' button at 'Hlídací pes nastaven.' note", True)
        self.element_handler_is_invisible(self.watchdog_success_add_note_close_button)
