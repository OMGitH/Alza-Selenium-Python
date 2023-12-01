from selenium.webdriver.common.by import By
from object_handler import ObjectHandler


class LoginPage(ObjectHandler):

    # Identification of objects on login page.
    email_input = (By.XPATH, "//input[@id='userName' and not(@readonly)]")
    password_input = (By.XPATH, "//input[@id='password' and not(@readonly)]")
    sign_in_button_active = (By.XPATH, "//button[@id='btnLogin'][@class='btn btn-login mt-2']")
    sign_in_button_disabled = (By.XPATH, "//button[@id='btnLogin'][@class='btn btn-login mt-2 invalid']")
    login_dialog = (By.CLASS_NAME, "login-body")
    provide_email_text = (By.XPATH, "//label[@for='userName']/parent::div/span")
    provide_password_text = (By.XPATH, "//label[@for='password']/parent::div/span")

    # Initialization.
    def __init__(self, driver):
        super().__init__(driver)

    # Actions on login dialog.
    def provide_email(self, username):
        self.object_handler_clear_input(self.email_input)
        self.object_handler_send_keys(self.email_input, username)

    def provide_password(self, password):
        self.object_handler_clear_input(self.password_input)
        self.object_handler_send_keys(self.password_input, password)

    def click_signin_button(self):
        self.object_handler_click(self.sign_in_button_active)

    def login_dialog_is_visible(self):
        flag = self.object_handler_is_visible(self.login_dialog, handle_TimeoutException=True)
        return flag

    def login_dialog_is_invisible(self):
        flag = self.object_handler_is_invisible(self.login_dialog, handle_TimeoutException=True)
        return flag

    def get_blank_email_text(self):
        if self.object_handler_is_visible(self.provide_email_text):
            email_text = self.object_handler_get_element_text(self.provide_email_text)
            return email_text

    def get_blank_password_text(self):
        if self.object_handler_is_visible(self.provide_password_text):
            password_text = self.object_handler_get_element_text(self.provide_password_text)
            return password_text

    def get_disabled_login_button_text(self):
        if self.object_handler_is_visible(self.sign_in_button_disabled):
            disabled_button_text = self.object_handler_get_element_text(self.sign_in_button_disabled)
            return disabled_button_text

    def successful_login(self, username, password):
        self.provide_email(username)
        self.provide_password(password)
        self.click_signin_button()
