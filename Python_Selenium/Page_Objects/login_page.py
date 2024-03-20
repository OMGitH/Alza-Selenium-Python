from selenium.webdriver.common.by import By
from element_handler import ElementHandler


class LoginPage(ElementHandler):

    # Identification of elements on login page.
    email_input = (By.CSS_SELECTOR, "input#userName:not([readonly])")
    password_input = (By.CSS_SELECTOR, "input#password:not([readonly])")
    sign_in_button_active = (By.CSS_SELECTOR, "button#btnLogin:not(.invalid)")
    sign_in_button_disabled = (By.CSS_SELECTOR, "button#btnLogin.invalid")
    login_dialog = (By.CLASS_NAME, "login-body")
    provide_email_error_text = (By.XPATH, "//label[@for='userName']/following-sibling::span")
    provide_password_error_text = (By.XPATH, "//label[@for='password']/following-sibling::span")

    # Actions on login page.
    def provide_email(self, username):
        self.element_handler_clear_input(self.email_input, "'E-mail' input field", True)
        self.element_handler_send_keys(self.email_input, username, "'E-mail' input field", True)

    def provide_password(self, password):
        self.element_handler_clear_input(self.password_input, "'Heslo' input field", True)
        self.element_handler_send_keys(self.password_input, password, "'Heslo' input field", True)

    def click_signin_button(self):
        self.element_handler_click(self.sign_in_button_active, "'Přihlásit se' button", True)

    def login_dialog_is_visible(self):
        flag = self.element_handler_is_visible(self.login_dialog, "Login dialog", handle_timeout_exception=True)
        return flag

    def login_dialog_is_invisible(self):
        flag = self.element_handler_is_invisible(self.login_dialog, "Login dialog", handle_timeout_exception=True)
        return flag

    def get_blank_email_text(self):
        if self.element_handler_is_visible(self.provide_email_error_text, "Error text 'Zadejte e-mailovou adresu'"):
            email_text = self.element_handler_get_element_text(self.provide_email_error_text, "Error text 'Zadejte e-mailovou adresu'")
            return email_text

    def get_blank_password_text(self):
        if self.element_handler_is_visible(self.provide_password_error_text, "Error text 'Zadejte prosím heslo'"):
            password_text = self.element_handler_get_element_text(self.provide_password_error_text, "Error text 'Zadejte prosím heslo'")
            return password_text

    def get_disabled_login_button_text(self):
        if self.element_handler_is_visible(self.sign_in_button_disabled, "Disabled sign in button"):
            disabled_button_text = self.element_handler_get_element_text(self.sign_in_button_disabled, "Disabled sign in button text")
            return disabled_button_text

    def successful_login(self, username, password):
        self.provide_email(username)
        self.provide_password(password)
        self.click_signin_button()
