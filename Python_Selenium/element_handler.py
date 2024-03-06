from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from report_logger import logger
from Config.config import timeout_default


class ElementHandler:
    """Contains basic methods for handling web page elements that are used at all page objects and thus is a parent of all page objects."""
    # Initialization.
    def __init__(self, driver):
        self.driver = driver

    # Methods:
    def element_handler_click(self, element_identifier, element_name, report_entry, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(element_identifier)).click()
        if report_entry:
            logger.info(f"{element_name} clicked.")

    def element_handler_hover_click(self, element_identifier, element_name, report_entry, timeout=timeout_default):
        element_hover_click = self.element_handler_is_visible(element_identifier, timeout=timeout)
        action = ActionChains(self.driver)
        action.move_to_element(element_hover_click).click().perform()
        if report_entry:
            logger.info(f"{element_name} hovered and clicked.")

    def element_handler_send_keys(self, element_identifier, value, element_name, report_entry, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(element_identifier)).send_keys(value)
        if report_entry:
            logger.info(f"'{value}' entered into {element_name}.")

    def element_handler_switch_to_frame(self, element_identifier, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(ec.frame_to_be_available_and_switch_to_it(element_identifier))

    def element_handler_switch_back_from_frame(self):
        self.driver.switch_to.default_content()

    def element_handler_is_visible(self, element_identifier, timeout=timeout_default, handle_timeout_exception=False):
        if not handle_timeout_exception:
            element = WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(element_identifier))
            return element
        else:
            try:
                WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(element_identifier))
                flag = True
            except TimeoutException:
                flag = False
        return flag

    def element_handler_is_invisible(self, element_identifier, timeout=timeout_default, handle_timeout_exception=False):
        if not handle_timeout_exception:
            flag = WebDriverWait(self.driver, timeout).until(ec.invisibility_of_element_located(element_identifier))
        else:
            try:
                WebDriverWait(self.driver, timeout).until(ec.invisibility_of_element_located(element_identifier))
                flag = True
            except TimeoutException:
                flag = False
        return flag

    def element_handler_get_element_text(self, element_identifier, timeout=timeout_default):
        element_text = WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(element_identifier)).text
        return element_text

    def element_handler_get_multiple_elements_text(self, element_identifier, timeout=timeout_default):
        elements = WebDriverWait(self.driver, timeout).until(ec.visibility_of_all_elements_located(element_identifier))
        elements_text = [element.text for element in elements]
        return elements_text

    def element_handler_get_element_attribute_value(self, element_identifier, attribute, timeout=timeout_default):
        element_attribute_value = WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(element_identifier)).get_attribute(attribute)
        return element_attribute_value

    def element_handler_clear_input(self, element_identifier, element_name, report_entry, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(element_identifier)).clear()
        if report_entry:
            logger.info(f"{element_name} cleared.")

    def element_handler_clear_input_by_pressing_backspace(self, element_identifier, attribute, element_name, report_entry, timeout=timeout_default):
        element_attribute_value = self.element_handler_get_element_attribute_value(element_identifier, attribute, timeout)
        number_of_hits = len(element_attribute_value)
        WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(element_identifier)).send_keys(number_of_hits * Keys.BACKSPACE)
        if report_entry:
            logger.info(f"{element_name} cleared by pressing backspace.")

    def element_handler_get_number_of_visible_elements(self, element_identifier, timeout=2):
        try:
            elements = WebDriverWait(self.driver, timeout).until(ec.visibility_of_all_elements_located(element_identifier))
            number_of_elements = len(elements)
        except TimeoutException:
            number_of_elements = 0
        return number_of_elements

    def element_handler_get_multiple_visible_elements(self, element_identifier, timeout=timeout_default):
        elements = WebDriverWait(self.driver, timeout).until(ec.visibility_of_all_elements_located(element_identifier))
        return elements

    def element_handler_get_state(self, *elements_identifiers, number_of_checks=40, check_wait=0.25):
        """Serves for checking which of multiple possible states is true without having to wait for timeout when checking whether an element
        is present or not. Can be used only if each state has an element that is not present in the other state as the state is identified
        based on presence of an element. In general speeds up process of checking state and adds reliability.
        """
        for _ in range(number_of_checks):
            for element_identifier in elements_identifiers:
                try:
                    WebDriverWait(self.driver, check_wait).until(ec.visibility_of_element_located(element_identifier))
                    return element_identifier
                except TimeoutException:
                    pass
