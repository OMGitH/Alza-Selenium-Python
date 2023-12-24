from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import report_log

# Contains basic methods for handling web page elements that are used at all page object and thus is a parent of all page objects.

timeout_default = 20


class ObjectHandler:

    def __init__(self, driver):
        self.driver = driver

    # Methods:
    def object_handler_click(self, locator, locator_name, report_entry, handle_StaleElementReferenceException=False, timeout=timeout_default):
        if not handle_StaleElementReferenceException:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()
        else:
            end_time = time.monotonic() + timeout
            while time.monotonic() <= end_time:
                try:
                    WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()
                    break
                except StaleElementReferenceException:
                    pass
        if report_entry:
            report_log.logger.info(f"{locator_name} clicked.")


    def object_handler_click_until_appears(self, locator_click, locator_to_appear, number_of_clicks=10, click_wait=0.5):
        for click in range(number_of_clicks):
            self.object_handler_click(locator_click)
            if self.object_handler_is_visible(locator_to_appear, click_wait, True):
                break

    def object_handler_hover_click(self, locator, locator_name, report_entry, timeout=timeout_default):
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        action = ActionChains(self.driver)
        action.move_to_element(element).click().perform()
        if report_entry:
            report_log.logger.info(f"{locator_name} hovered and clicked.")

    def object_handler_send_keys(self, locator, value, locator_name, report_entry, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).send_keys(value)
        if report_entry:
            report_log.logger.info(f"'{value}' entered into {locator_name}.")

    def object_handler_switch_to_frame(self, locator, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.frame_to_be_available_and_switch_to_it(locator))

    def object_handler_switch_back_from_frame(self):
        self.driver.switch_to.default_content()

    def object_handler_is_visible(self, locator, timeout=timeout_default, handle_TimeoutException=False):
        if not handle_TimeoutException:
            element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return element
        else:
            try:
                WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
                return True
            except TimeoutException:
                return False

    def object_handler_is_invisible(self, locator, timeout=timeout_default, handle_TimeoutException=False):
        if not handle_TimeoutException:
            flag = WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            return flag
        else:
            try:
                WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
                return True
            except TimeoutException:
                return False

    def object_handler_get_element_text(self, locator, timeout=timeout_default):
        element_text = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator)).text
        return element_text

    def object_handler_get_multiple_elements_text(self, locator, timeout=timeout_default):
        elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
        elements_text = []
        for element in elements:
            elements_text.append(element.text)
        return elements_text

    def object_handler_get_element_attribute_value(self, locator, attribute, timeout=timeout_default):
        element_attribute_value = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator)).get_attribute(attribute)
        return element_attribute_value

    def object_handler_clear_input(self, locator, locator_name, report_entry, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator)).clear()
        if report_entry:
            report_log.logger.info(f"{locator_name} cleared.")


    def object_handler_element_exists(self, locator, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    """
    Original uploaded code.
    def base_element_exists(self, locator, timeout=timeout_default):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
        except TimeoutException:
            flag = False
            return flag
        flag = True
        return flag
    """

    def object_handler_clear_input_by_pressing_backspace(self, locator, attribute, locator_name, report_entry, timeout=timeout_default):
        element_attribute_value = self.object_handler_get_element_attribute_value(locator, attribute, timeout)
        number_of_hits = len(element_attribute_value)
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).send_keys(number_of_hits * Keys.BACKSPACE)
        if report_entry:
            report_log.logger.info(f"{locator_name} cleared by pressing backspace.")

    def object_handler_get_number_of_visible_elements(self, locator, timeout=2):
        try:
            elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
            number_of_elements = len(elements)
            return number_of_elements
        except TimeoutException:
            number_of_elements = 0
            return number_of_elements

    def object_handler_get_multiple_visible_elements(self, locator, timeout=timeout_default):
        elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
        return elements

    """
    Serves for checking which of multiple possible states is true without having to wait for timeout when checking whether an element is present or not.
    Can be used only if each state has an element that is not present in the other state as the state is identified based on presence of an element.
    In general speeds up process of checking state and adds reliability (for example can be used instead of checking if item is in basket or not
    using visibility_of_element_located with timeout of 2 seconds and if it doesn't appear in 2 seconds, assuming that there is no item in basket).
    """
    def object_handler_get_state(self, *locators, number_of_checks=40, check_wait=0.25):
        for check in range(number_of_checks):
            for locator in locators:
                try:
                    WebDriverWait(self.driver, check_wait).until(EC.visibility_of_element_located(locator))
                    return locator
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
