import sys
sys.path.append("../util")
import unittest
import time
from datetime import datetime, timedelta
from ui_helper import UIHelper

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait

import logging
logger = logging.getLogger(__name__)

# hide traceback
# __unittest = True

class TestUIItems(unittest.TestCase):
    
    def __init__(self, test_name, instance, **kwargs):
        super().__init__(test_name)
        self.instance = instance
        self.ui = UIHelper(self.instance)
        self.kwargs = kwargs
    
    def test_items(self):
        items = self.kwargs["items"]
        
        self.ui.click_side_menu("Items")
        
        # Add "Items"
        for item in items:
            print(item)
            locator = (By.XPATH, f'.//tbody/tr[contains(@class, "row") and .//a[contains(text(), "{item["name"]}")]]')
            elements = self.instance.find_elements(locator)

            if len(elements) > 0:
#                 logger.info(f"Found: {item['name']}")
                self.instance.scroll_to_element(elements[0])
                self.ui.click_edit(elements[0])
            else:
#                 logger.info(f"Not Found: {item['name']}")
                self.ui.click_add()

            self.ui.enter_text((By.ID, "name"), item["name"])
        #     ui.select_dropdown("Tax", item["tax"])
            self.ui.enter_text((By.ID, "description"), item["description"])
            self.instance.scroll_down()
            self.ui.enter_text((By.ID, "sale_price"), item["sale_price"])
            self.ui.enter_text((By.ID, "purchase_price"), item["purchase_price"])
            self.ui.select_dropdown("Category", item["category"])
            self.ui.select_toggle_button("Enabled", item["enabled"])


            self.ui.click_save()
            self.instance.wait(8)
        
        # Validate items data
        self.__validate_items(items)
   


    def __validate_items(self, items):
         for item in items:
            print(item)
            locator = (By.XPATH, f'.//tbody/tr[contains(@class, "row") and .//a[contains(text(), "{item["name"]}")]]')
            elements = self.instance.find_elements(locator)

            if len(elements) > 0:
#                 logger.info(f"Found: {item['name']}")
                self.instance.scroll_to_element(elements[0])
                self.instance.wait(2)
                self.ui.click_edit(elements[0])
                self.instance.wait(2)
        
            element = self.instance.get_element((By.ID, "name"))
            element.click()
            self.assertEqual(element.get_attribute("value"), item["name"], "Item name is not '{}'".format(item["name"]))

            element = self.instance.get_element((By.ID, "description"))
            element.click()
            self.assertEqual(element.get_attribute("value"), item["description"], "Item description is not '{}'".format(item["description"]))

            self.instance.scroll_down()

            element = self.instance.get_element((By.ID, "sale_price"))
            element.click()
            self.assertEqual(element.get_attribute("value"), str(item["sale_price"]), "Item sales price is not '{}'".format(item["sale_price"]))

            element = self.instance.get_element((By.ID, "purchase_price"))
            element.click()
            self.assertEqual(element.get_attribute("value"), str(item["purchase_price"]), "Item purchase price is not '{}'".format(item["purchase_price"]))

            element = self.instance.get_element((By.XPATH,'//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Category")]]]//input'))
            element.click()
            self.assertEqual(element.get_attribute("placeholder"), item["category"], "Item category is not '{}'".format(item["category"]))

            self.ui.click_save()
            self.instance.wait(5)

            
        
        

  

        
        
        
        

        
        
        
        
        
        
  
        
