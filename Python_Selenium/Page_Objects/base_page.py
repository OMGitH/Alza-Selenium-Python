from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# This is a base page class that contains methods that can be used at any page and thus is a parent of all pages.

timeout_default = 20


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def base_click(self, locator, handle_StaleElementReferenceException=False, timeout=timeout_default):
        if handle_StaleElementReferenceException == False:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()
        else:
            end_time = time.monotonic() + timeout
            while time.monotonic() <= end_time:
                try:
                    WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()
                    break
                except StaleElementReferenceException:
                    pass

    def base_hover_click(self, locator, timeout=timeout_default):
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        action = ActionChains(self.driver)
        action.move_to_element(element).click().perform()

    def base_send_keys(self, locator, value, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).send_keys(value)

    def base_switch_to_frame(self, locator, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.frame_to_be_available_and_switch_to_it(locator))

    def base_switch_back_from_frame(self):
        self.driver.switch_to.default_content()

    def base_is_visible(self, locator, timeout=timeout_default):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def base_is_invisible(self, locator, timeout=timeout_default):
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            return True
        except:
            return False

    def base_get_element_text(self, locator, timeout=timeout_default):
        element_text = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator)).text
        return element_text

    def base_get_multiple_elements_text(self, locator, timeout=timeout_default):
        elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
        elements_text = []
        for element in elements:
            elements_text.append(element.text)
        return elements_text

    def base_get_element_attribute_value(self, locator, attribute, timeout=timeout_default):
        element_attribute_value = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator)).get_attribute(attribute)
        return element_attribute_value

    def base_clear_input(self, locator, timeout=timeout_default):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator)).clear()

    def base_element_exists(self, locator, timeout=timeout_default):
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

    def base_clear_input_by_pressing_backspace(self, locator, attribute, timeout=timeout_default):
        element_attribute_value = self.base_get_element_attribute_value(locator, attribute, timeout)
        number_of_hits = len(element_attribute_value)
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).send_keys(number_of_hits * Keys.BACKSPACE)

    def base_get_number_of_elements(self, locator, timeout=2):
        try:
            number_of_elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
            return len(number_of_elements)
        except TimeoutException:
            return 0

    def base_get_multiple_elements(self, locator, timeout=timeout_default):
        elements = WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))
        return elements

    """
    Can be used for checking which of 2 possible states is actual without having to wait for timeout when checking whether an element is present or not.
    Can be used only if each state has an element that is not present in the other state as the state is identified based on presence of an element.
    """
    def base_get_state(self, locator1, locator2, number_of_checks=40, check_wait=0.25):
        for check in range(number_of_checks):
            try:
                WebDriverWait(self.driver, 0.1).until(EC.visibility_of_element_located(locator1))
                return True
            except:
                pass
            try:
                WebDriverWait(self.driver, 0.1).until(EC.visibility_of_element_located(locator2))
                return False
            except:
                pass
            time.sleep(check_wait)