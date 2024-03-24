from selenium.webdriver.common.by import By
from element_handler import ElementHandler
from Tests.test_data import blank_email_error_text, blank_password_error_text, signin_button_incorrect_user_name_password_error_text


class LoginPage(ElementHandler):

    # Identification of elements on login page.
    email_input = {
        "locator": (By.CSS_SELECTOR, "input#userName:not([readonly])"),
        "name": "'E-mail' input field"
    }
    password_input = {
        "locator": (By.CSS_SELECTOR, "input#password:not([readonly])"),
        "name": "'Heslo' input field"
    }
    signin_button_active = {
        "locator": (By.CSS_SELECTOR, "button#btnLogin:not(.invalid)"),
        "name": "'Přihlásit se' button"
    }
    signin_button_disabled = {
        "locator": (By.CSS_SELECTOR, "button#btnLogin.invalid"),
        "name": "Disabled signin button"
    }
    login_dialog = {
        "locator": (By.CLASS_NAME, "login-body"),
        "name": "Login dialog"
    }
    provide_email_error_text = {
        "locator": (By.XPATH, "//label[@for='userName']/following-sibling::span"),
        "name": f"Blank e-mail error text '{blank_email_error_text}'"
    }
    provide_password_error_text = {
        "locator": (By.XPATH, "//label[@for='password']/following-sibling::span"),
        "name": f"Blank password error text '{blank_password_error_text}'"
    }

    # Actions on login page.
    def provide_email(self, username):
        self.element_handler_clear_input(self.email_input["locator"], self.email_input["name"], True)
        self.element_handler_send_keys(self.email_input["locator"], username, self.email_input["name"], True)

    def provide_password(self, password):
        self.element_handler_clear_input(self.password_input["locator"], self.password_input["name"], True)
        self.element_handler_send_keys(self.password_input["locator"], password, self.password_input["name"], True)

    def click_signin_button(self):
        self.element_handler_click(self.signin_button_active["locator"], self.signin_button_active["name"], True)

    def login_dialog_is_visible(self):
        flag = self.element_handler_is_visible(self.login_dialog["locator"], self.login_dialog["name"], handle_timeout_exception=True)
        return flag

    def login_dialog_is_invisible(self):
        flag = self.element_handler_is_invisible(self.login_dialog["locator"], self.login_dialog["name"], handle_timeout_exception=True)
        return flag

    def get_blank_email_text(self):
        email_error_text = self.element_handler_get_element_text(self.provide_email_error_text["locator"], self.provide_email_error_text["name"])
        return email_error_text

    def get_blank_password_text(self):
        password_error_text = self.element_handler_get_element_text(self.provide_password_error_text["locator"], self.provide_password_error_text["name"])
        return password_error_text

    def get_disabled_signin_button_text(self):
        disabled_button_text = self.element_handler_get_element_text(self.signin_button_disabled["locator"], f"{self.signin_button_disabled["name"]} text '{signin_button_incorrect_user_name_password_error_text}'")
        return disabled_button_text

    def successful_login(self, username, password):
        self.provide_email(username)
        self.provide_password(password)
        self.click_signin_button()
