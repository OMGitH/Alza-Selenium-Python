from selenium.webdriver.common.by import By
from object_handler import ObjectHandler


class MyAccount(ObjectHandler):

    # Identification of objects on my account page.
    account_settings_dropdown = (By.XPATH, "//div[@data-testid='menuSection-MyAccount']")
    my_account_menu_item = (By.XPATH, "//a[@data-testid='menuButton-UserSettings']")
    watchdogs_menu_item = (By.XPATH, "//a[@data-testid='menuButton-UserWatchDog']")
    delivery_addresses_menu_item = (By.XPATH, "//a[@data-testid='menuButton-DeliveryAddresses']")

    data_is_saving_text = (By.XPATH, "//span[@class='saving']/span[@class='text']")
    data_was_saved_text = (By.XPATH, "//span[@class='saved']/span[@class='text']")

    """
    Original uploaded code.
    data_is_saving_text = (By.XPATH, "//span[@class='saving'][contains(@style, 'inline')]/span[@class='text']")
    data_was_saved_text = (By.XPATH, "//span[@class='saved'][contains(@style, 'inline')]/span[@class='text']")
    """

    street_input = (By.NAME, "street")
    street_input_correctly_filled = (By.XPATH, "//input[@name='street'][contains(@class, 'valid')][not(contains(@class, 'empt'))]")
    zip_input = (By.NAME, "zip")
    zip_input_correctly_filled = (By.XPATH, "//input[@name='zip'][contains(@class, 'valid')][not(contains(@class, 'empt'))]")
    city_input = (By.NAME, "city")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions on my account page.
    def click_account_settings_dropdown(self):
        self.object_handler_click(self.account_settings_dropdown)

    def click_my_account_menu_item(self):
        self.object_handler_click(self.my_account_menu_item)
        # Following method helps initialize the page as validations there are dynamic.
        self.object_handler_element_exists(self.data_was_saved_text)

    def click_watchdogs_menu_item(self):
        self.object_handler_click(self.watchdogs_menu_item, "'Hlídací psi' menu item", True)

    def click_delivery_addresses_menu_item(self):
        self.object_handler_click(self.delivery_addresses_menu_item, "'Doručovací adresy' menu item", True)
