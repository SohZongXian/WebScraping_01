from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from bs4 import BeautifulSoup
import unicodedata

import time
import logging
# Set the threshold for selenium to WARNING
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
seleniumLogger.setLevel(logging.WARNING)
# Set the threshold for urllib3 to WARNING
from urllib3.connectionpool import log as urllibLogger
urllibLogger.setLevel(logging.WARNING)

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

logger = logging.getLogger(__name__)

class WebDriver():
    
    TIMEOUT = 10
    MAX_RETRY = 3
    TIME_SLEEP = 5
    
    def __init__(self, mode, timeout, driver_path=None):
        # Create web driver options
        options = webdriver.ChromeOptions()
        #Disable image
        prefs = {
            "profile.managed_default_content_settings.images": 2, 
            "disk-cache-size": 4096,
            "profile.default_content_setting_values.notifications": 1 # 1: allow, 2: block
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")

        if mode == "linux":
            if driver_path is None:
                driver_path = "/usr/bin/chromedriver"
            options.add_argument("--headless")
        elif mode == "mac":
            if driver_path is None:
                driver_path = "../../drivers/chrome/mac/chromedriver.exe"
        else:
            if driver_path is None:
                driver_path = "../../drivers/chrome/win/chromedriver.exe"
        
        driver = webdriver.Chrome(driver_path, options=options)
        
        self.__timeout = timeout
        
        print("WebDriver created!")
        print("Mode: {}".format(mode))
        print("Driver Path: {}".format(driver_path))
        print("Timeout: {}".format(self.__timeout))
        self.__driver = driver
        
    def get_driver(self):
        return self.__driver
        
    def close(self):
         self.__driver.quit()

    @staticmethod
    def validate_result(test_result):
        if (test_result.wasSuccessful()):
            logger.info("Test was executed successfully ...")
        else:
            if ((len(test_result.errors) > 0)):
                raise Exception(test_result.errors)
            if ((len(test_result.failures) > 0)):
                raise Exception(test_result.failures) 
            
    def __get_element(self, locator, condition, parent=None, max_retry=None, time_sleep=None):
        if parent is None:
            parent = self.__driver
        if max_retry is None:
            max_retry = self.MAX_RETRY
        if time_sleep is None:
            time_sleep = self.TIME_SLEEP
            
        retry = 0
        while retry < max_retry:
            try:
                element = (WebDriverWait(parent, self.TIMEOUT)
                            .until(condition(locator)))
                if element is not None:
                    break
            except TimeoutException:
                retry += 1
                if retry >= max_retry:
                    raise
                time.sleep(time_sleep)
        return element

    def find_element(self, locator, parent=None):
        if parent is None:
            parent = self.__driver
        return parent.find_element(locator[0], locator[1])
    
    def find_elements(self, locator, parent=None):
        if parent is None:
            parent = self.__driver
        return parent.find_elements(locator[0], locator[1])
    
    def get_element(self, locator, parent=None, max_retry=None, time_sleep=None):
        return self.__get_element(locator, expected_conditions.visibility_of_element_located, parent, max_retry, time_sleep)

    def enter_text(self, locator, text, parent=None, max_retry=None, time_sleep=None):
        element = self.get_element(locator, parent, max_retry, time_sleep)
        element.send_keys(Keys.CONTROL + "a") # select existing text in the textbox
        element.send_keys(text)        
    
    def select_dropdown(self, locator, value):
        select_element = Select(self.find_element(locator))
        select_element.select_by_value(value)
    
    def click_element(self, locator, parent=None, max_retry=None, time_sleep=None):
        element = self.__get_element(locator, expected_conditions.element_to_be_clickable, parent, max_retry, time_sleep)
        element.click()
    
    def get_attribute(self, element, attribute="innerHTML"):
        if attribute == "innerHTML":
            value = element.get_attribute("innerHTML")
            value = BeautifulSoup(value, "html.parser").text
            value = unicodedata.normalize("NFKD", value)
        else:
            value = element.get_attribute(attribute)
        value = value.strip()
        return value
    
    def wait(self, seconds):
        time.sleep(seconds)

    def crawl_metadata(self, metadatas, element_id, parent=None):
        fields = {}
        if parent is None:
            parent = self.__driver
        
        for metadata in metadatas:
            xpath = metadata["xpath"].format(element_id=element_id)
            attribute = metadata["attribute"]
            element = parent.find_element_by_xpath(xpath)
            fields[metadata["field"]] = f"{self.get_attribute(element, attribute)}"
        return fields
        
    def move_to(self, element):
        action = ActionChains(self.get_driver())
        action.move_to_element(element).perform()
        self.get_driver().execute_script("arguments[0].click();", element)
        
    def scroll_to_element(self, element):
        coordinates = element.location_once_scrolled_into_view
        x_pixel = coordinates["x"]
        y_pixel = coordinates["y"]
        self.get_driver().execute_script('window.scrollBy({}, {})'.format(x_pixel, y_pixel))
    
    def scroll_by(self, x_pixel, y_pixel):
        self.get_driver().execute_script('window.scrollBy({}, {})'.format(x_pixel, y_pixel))
    
    def scroll_down(self):
        self.get_driver().execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    def get_screenshot(self, path):
        # path = path/imageName
        self.get_driver().save_screenshot(path)
        
    def get_current_url(self):
        current_url = self.get_driver().current_url
        return current_url
    
    def find_elements_by_xpath(self, xpath):
        elements = self.get_driver().find_elements_by_xpath(xpath)
        return elements
    
    def find_elements_by_tag_name(self, tag):
        elements = self.get_driver().find_elements_by_tag_name(tag)
        return elements
    
