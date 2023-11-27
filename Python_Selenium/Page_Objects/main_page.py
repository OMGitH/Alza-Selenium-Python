from selenium.webdriver.common.by import By
from Page_Objects.base_page import BasePage


class MainPage(BasePage):

    # Identification of objects on main page.
    category_section_header = (By.XPATH, "//div[@class='categoryPage']/h1")
    item_detail_page = (By.XPATH, "//div[contains(@class, 'detail-page')]")
    computers_notebooks_menu_item = (By.LINK_TEXT, "Počítače a notebooky")
    computers_tile = (By.LINK_TEXT, "Počítače")
    first_computer_name = (By.XPATH, "//div[contains(@class, 'first firstRow')]//a[contains(@class, 'name')]")
    first_computer_price = (By.XPATH, "//div[contains(@class, 'first firstRow')]//span[@class='price-box__price']")
    first_computer_put_to_basket_button = (By.XPATH, "//div[contains(@class, 'first firstRow')]//a[@class='btnk1']")
    continue_to_basket_button = (By.ID, "varBToBasketButton")
    search_result_header_text = (By.XPATH, "//h1[@itemprop='name']")
    search_result_number_of_items_found = (By.ID, "lblNumberItem")
    pet_supplies_menu_item = (By.LINK_TEXT, "Chovatelské potřeby")
    pet_supply_dialog_agree_button = (By.XPATH, "//button[@data-testid='dialogRestrictedAgeAcceptButton']")
    first_pet_supply_item_link = (By.XPATH, "//div[@data-react-client-component-id='carousel0']//swiper-slide[@class='swiper-slide-active']//a[@data-testid='itemName']")
    first_pet_supply_item_name = (By.XPATH, "//h1[@itemprop='name']")
    watchdog_link = (By.CLASS_NAME, "watchproduct")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions on main page.
    def main_page_hover_click_computers_notebooks_menu_item(self):
        self.base_hover_click(self.computers_notebooks_menu_item)
        self.base_is_visible(self.category_section_header)

    def main_page_hover_click_pet_supplies_menu_item(self):
        self.base_hover_click(self.pet_supplies_menu_item)
        self.base_is_visible(self.category_section_header)

    def main_page_click_computers_tile(self):
        self.base_click(self.computers_tile)

    def main_page_click_first_pet_suppy_item(self):
        self.base_click(self.first_pet_supply_item_link)
        self.base_is_visible(self.item_detail_page)

    def main_page_click_watch_price(self):
        self.base_click(self.watchdog_link)

    def main_page_get_first_computer_name(self):
        if self.base_is_visible(self.first_computer_name):
            first_computer_name = self.base_get_element_text(self.first_computer_name)
            # It may happen there is a note inside () in name. It is needed to remove this note as it is not present in item name inside basket.
            opening_bracket_index = str(first_computer_name).find("(")
            if opening_bracket_index != -1:
                first_computer_name = str(first_computer_name)[:opening_bracket_index]
                first_computer_name = first_computer_name.strip()
            return first_computer_name

    def main_page_get_first_pet_supply_name(self):
        if self.base_is_visible(self.first_pet_supply_item_name):
            first_pet_supply_name = self.base_get_element_text(self.first_pet_supply_item_name)
            return first_pet_supply_name

    def main_page_get_first_computer_price(self):
        if self.base_is_visible(self.first_computer_price):
            price = self.base_get_element_text(self.first_computer_price)
            price = price.replace(" ", "")
            price = price.replace(",-", "Kč")
            return price

    def main_page_click_cont_to_basket_button(self):
        self.base_click(self.continue_to_basket_button)

    def main_page_click_first_computer_put_to_basket_button(self):
        self.base_click(self.first_computer_put_to_basket_button)

    def main_page_get_search_result_header(self):
        if self.base_is_visible(self.search_result_header_text):
            result_header = self.base_get_element_text(self.search_result_header_text)
            return result_header

    def main_page_get_search_result_items_amount(self):
        if self.base_is_visible(self.search_result_number_of_items_found):
            result_items_amount = self.base_get_element_text(self.search_result_number_of_items_found)
            return int(result_items_amount)

    def main_page_pet_supply_close_dialog(self):
        if self.base_is_visible(self.pet_supply_dialog_agree_button, 2, True):
            self.base_click(self.pet_supply_dialog_agree_button)
