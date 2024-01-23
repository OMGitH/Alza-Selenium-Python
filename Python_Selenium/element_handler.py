from time import monotonic
from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from report_logger import logger

"""
Contains basic methods for handling web page elements that are used at all page objects and thus is a parent of all page objects.
"""

timeout_default = 20


class ElementHandler:

    def __init__(self, driver):
        self.driver = driver

    # Methods:
    def element_handler_click(self, element_identifier, element_name, report_entry, handle_StaleElementReferenceException=False, timeout=timeout_default):
        if not handle_StaleElementReferenceException:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element_identifier)).click()
        else:
            end_time = monotonic() + timeout
            while monotonic() <= end_time:
                try:
                    WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element_identifier)).click()
                    break
                except StaleElementReferenceException:
                    pass
        if report_entry:
            logger.info(f"{element_name} clicked.")


    def element_handler_click_until_appears(self, locator_click, locator_to_appear, number_of_clicks=10, click_wait=0.5):
        for click in range(number_of_clicks):
            self.element_handler_click(locator_click)
            if self.element_handler_is_visible(locator_to_appear, click_wait, True):
                break

    def element_handler_hover_click(self, element_identifier, element_name, report_entry, timeout=timeout_default):
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(element_identifier))
        action = ActionChains(self.driver)
        action.move_to_element(element).click().perform()
        if report_entry:
            logger.info(f"{element_name} hovered and clicked.")

    def element_handler_send_keys(self, element_identifier, value, element_name, report_entry, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element_identifier)).send_keys(value)
        if report_entry:
            logger.info(f"'{value}' entered into {element_name}.")

    def element_handler_switch_to_frame(self, element_identifier, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.frame_to_be_available_and_switch_to_it(element_identifier))

    def element_handler_switch_back_from_frame(self):
        self.driver.switch_to.default_content()

    def element_handler_is_visible(self, element_identifier, timeout=timeout_default, handle_TimeoutException=False):
        if not handle_TimeoutException:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(element_identifier))
            return element
        else:
            try:
                WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(element_identifier))
                return True
            except TimeoutException:
                return False

    def element_handler_is_invisible(self, element_identifier, timeout=timeout_default, handle_TimeoutException=False):
        if not handle_TimeoutException:
            flag = WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(element_identifier))
            return flag
        else:
            try:
                WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(element_identifier))
                return True
            except TimeoutException:
                return False

    def element_handler_get_element_text(self, element_identifier, timeout=timeout_default):
        element_text = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(element_identifier)).text
        return element_text

    def element_handler_get_multiple_elements_text(self, element_identifier, timeout=timeout_default):
        elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(element_identifier))
        elements_text = [element.text for element in elements]
        return elements_text

    def element_handler_get_element_attribute_value(self, element_identifier, attribute, timeout=timeout_default):
        element_attribute_value = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(element_identifier)).get_attribute(attribute)
        return element_attribute_value

    def element_handler_clear_input(self, element_identifier, element_name, report_entry, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(element_identifier)).clear()
        if report_entry:
            logger.info(f"{element_name} cleared.")


    def element_handler_element_exists(self, element_identifier, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(element_identifier))

    """
    Original uploaded code.
    def base_element_exists(self, element_identifier, timeout=timeout_default):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(element_identifier))
        except TimeoutException:
            flag = False
            return flag
        flag = True
        return flag
    """

    def element_handler_clear_input_by_pressing_backspace(self, element_identifier, attribute, element_name, report_entry, timeout=timeout_default):
        element_attribute_value = self.element_handler_get_element_attribute_value(element_identifier, attribute, timeout)
        number_of_hits = len(element_attribute_value)
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element_identifier)).send_keys(number_of_hits * Keys.BACKSPACE)
        if report_entry:
            logger.info(f"{element_name} cleared by pressing backspace.")

    def element_handler_get_number_of_visible_elements(self, element_identifier, timeout=2):
        try:
            elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(element_identifier))
            number_of_elements = len(elements)
            return number_of_elements
        except TimeoutException:
            number_of_elements = 0
            return number_of_elements

    def element_handler_get_multiple_visible_elements(self, element_identifier, timeout=timeout_default):
        elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(element_identifier))
        return elements

    """
    Serves for checking which of multiple possible states is true without having to wait for timeout when checking whether an element is present or not.
    Can be used only if each state has an element that is not present in the other state as the state is identified based on presence of an element.
    In general speeds up process of checking state and adds reliability (for example can be used instead of checking if item is in basket or not
    using visibility_of_element_located with timeout of 2 seconds and if it doesn't appear in 2 seconds, assuming that there is no item in basket).
    """
    def element_handler_get_state(self, *element_identifiers, number_of_checks=40, check_wait=0.25):
        for check in range(number_of_checks):
            for element_identifier in element_identifiers:
                try:
                    WebDriverWait(self.driver, check_wait).until(EC.visibility_of_element_located(element_identifier))
                    return element_identifier
                except TimeoutException:
                    pass

    """
    Can be used for checking which of 2 possible states is true without having to wait for timeout when checking whether an element is present or not.
    Can be used only if each state has an element that is not present in the other state as the state is identified based on presence of an element.
    """
    # def base_get_state(self, locator_state_1, locator_state_2, number_of_checks=40, check_wait=0.25):
    #     for check in range(number_of_checks):
    #         try:
    #             WebDriverWait(self.driver, 0.1).until(EC.presence_of_element_located(locator_state_1))
    #             return True
    #         except TimeoutException:
    #             pass
    #         try:
    #             WebDriverWait(self.driver, 0.1).until(EC.presence_of_element_located(locator_state_2))
    #             return False
    #         except TimeoutException:
    #             pass
    #         time.sleep(check_wait)
