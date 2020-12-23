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

class TestUISettings(unittest.TestCase):
    
    def __init__(self, test_name, instance, **kwargs):
        super().__init__(test_name)
        self.instance = instance
        self.ui = UIHelper(self.instance)
        self.kwargs = kwargs
    
    def test_company(self):
        company = self.kwargs["company"]
        
        self.ui.click_side_menu("Settings")
        # Select Company Settings
        self.__click_settings_option("Company")
        
        # edit "Company"
        self.ui.enter_text((By.ID, "name"), company["name"])
        self.ui.enter_text((By.ID, "email"),  company["email_address"])
        self.ui.enter_text((By.ID, "tax_number"),  company["tax_number"])
        self.ui.enter_text((By.ID, "phone"),  company["phone"])
        self.ui.enter_text((By.ID, "address"),  company["address"])
        self.instance.scroll_down()
        self.ui.click_save()
        
        # Re-Select Company Settings after Save
        self.__click_settings_option("Company")
        # Validate company data
        self.__validate_company(company)
        
    def test_localisation(self):
        localisation = self.kwargs["localisation"]
        
        self.ui.click_side_menu("Settings")
        # Select Localisation Settings
        self.__click_settings_option("Localisation")
        
        # edit "Localisation"
        self.ui.select_date_picker("Financial Year Start", localisation["financial_year_start"])
        self.ui.select_dropdown("Time Zone", localisation["time_zone"])
        self.ui.select_dropdown("Date Format", localisation["date_format"])
        self.ui.select_dropdown("Date Separator", localisation["date_separator"])
        self.ui.select_dropdown("Percent (%) Position", localisation["percent_position"])
        self.ui.select_dropdown("Discount Location", localisation["discount_location"])
        self.ui.click_save()
        
        # Re-Select Localisation Settings after Save
        self.__click_settings_option("Localisation")
        # Validate localisation data
        self.__validate_localisation(localisation)
        
    def test_currencies(self):
        currencies = self.kwargs["currencies"]
        
        self.ui.click_side_menu("Settings")
        # Select Currencies Settings
        self.__click_settings_option("Currencies")
        
        for currency in currencies:
            self.instance.scroll_down()
            locator = (By.XPATH, f'.//tbody/tr[contains(@class, "row") and ./td[3 and text()="{currency["code"]}"]]')
            elements = self.instance.find_elements(locator)

            if len(elements) > 0:
                logger.info(f"Found: {currency['code']}")
                self.ui.click_edit(elements[0])
            else:
                logger.info(f"Not Found: {currency['code']}")
                self.ui.click_add()

            self.ui.enter_text((By.ID, "name"), currency["name"])
            self.ui.select_dropdown("Code", currency["code"])
            self.ui.enter_text((By.ID, "rate"), str(currency["rate"]))
            self.ui.select_dropdown("Precision", currency["precision"])
            self.ui.enter_text((By.ID, "decimal_mark"), str(currency["decimal_mark"]))
            self.ui.enter_text((By.ID, "thousands_separator"), str(currency["thousands_separator"]))
            self.instance.scroll_down()
            self.ui.select_toggle_button("Enabled", currency["enabled"])
            self.ui.select_toggle_button("Default Currency", currency["default"])
            self.ui.click_save()
            self.instance.wait(2)
        
        self.ui.click_side_menu("Settings")
        # Re-Select Currencies Settings after Save
        self.__click_settings_option("Currencies")
        # Validate Currencies data
        self.__validate_currencies(currencies)
        
    def test_taxes(self):
        taxes = self.kwargs["taxes"]
        
        self.ui.click_side_menu("Settings")
        # Select Taxes Settings
        self.__click_settings_option("Taxes")
        
        for tax in taxes:
            self.instance.scroll_down()
            locator = (By.XPATH, f'.//tbody/tr[contains(@class, "row") and //*[text()[contains(., "{tax["name"]}")]]]')
            elements = self.instance.find_elements(locator)
            if len(elements) > 0:
                logger.info(f"Found: {tax['name']}")
                self.ui.click_edit(elements[0])
            else:
                logger.info(f"Not Found: {tax['name']}")
                self.ui.click_add()

            self.ui.enter_text((By.ID, "name"), tax["name"])
            self.ui.enter_text((By.ID, "rate"), str(tax["rate_%"]))
            self.ui.select_dropdown("Type", tax["type"])
            self.ui.click_save()
            self.instance.wait(2)

        self.ui.click_side_menu("Settings")
        # Re-Select Taxes Settings after Save
        self.__click_settings_option("Taxes")
        # Validate Taxes data
        self.__validate_taxes(taxes)
    
    def test_categories(self):
        categories = self.kwargs["categories"]
        
        self.ui.click_side_menu("Settings")
        # Select Categories Settings
        self.__click_settings_option("Categories")
        
        for category in categories:
            locator = (By.XPATH, f'.//tbody/tr[contains(@class, "row") and ./td[2] and .//a[text()[contains(., "{category["name"]}")]]]')
            elements = self.instance.find_elements(locator)
            if len(elements) > 0:
                logger.info(f"Found: {category['name']}")
                self.instance.scroll_to_element(elements[0])
                self.ui.click_edit(elements[0])

            else:
                logger.info(f"Not Found: {category['name']}")
                self.ui.click_add()

            self.ui.enter_text((By.ID, "name"), category["name"])
            self.instance.wait(2)
            self.ui.select_dropdown("Type", category["type"])
            self.ui.enter_text((By.ID, "color"), category["colour"])
            self.ui.select_toggle_button("Enabled", category["enabled"])
            self.ui.click_save()
            self.instance.wait(8)

        self.ui.click_side_menu("Settings")
        # Re-Select Categories Settings after Save
        self.__click_settings_option("Categories")
        # Validate Categories data
        self.__validate_categories(categories)
        
    def test_offline_payments(self):
        offline_payments = self.kwargs["offline_payments"]
        
        self.ui.click_side_menu("Settings")
        # Select Offline Payments Settings
        self.instance.scroll_down()
        self.__click_settings_option("Offline Payments")
        
        for payment in offline_payments:
            locator = (By.XPATH, f'.//tbody/tr[contains(@class, "row") and ./td[1 and text()="{payment["name"]}"]]')
            elements = self.instance.find_elements(locator)
            if len(elements) > 0:
                logger.info(f"Found: {payment['name']}")
                self.ui.click_edit(elements[0])
            else:
                logger.info(f"Not Found: {payment['name']}")

            self.ui.enter_text((By.ID, "name"), payment["name"])
            self.ui.enter_text((By.ID, "code"),  payment["code"])
            self.ui.select_toggle_button("Show to Customer", payment["show_to_customer"])
            self.instance.scroll_down()
            self.ui.enter_text((By.ID, "order"), payment["order"])
            self.ui.click_save()
            self.instance.wait(5)

        self.ui.click_side_menu("Settings")
        # Re-Select Offline Payments Settings after Save
        self.instance.scroll_down()
        self.__click_settings_option("Offline Payments")
        # Validate Offline Payments data
        self.__validate_offline_payments(offline_payments)
        
    def test_invoice(self):
        invoice = self.kwargs["invoice"]
        
        self.ui.click_side_menu("Settings")
        # Select invoice Settings
        self.__click_settings_option("Invoice")
        
        # edit "invoice"
        self.ui.enter_text((By.ID, "number_prefix"), invoice["number_prefix"])
        self.ui.enter_text((By.ID, "number_digit"), invoice["number_digit"])
        self.ui.enter_text((By.ID, "number_next"), invoice["next_number"])
        self.ui.select_dropdown("Payment Terms", invoice["payment_terms"])
        self.instance.scroll_down()

        self.ui.click_save()
        
        # Re-Select invoice Settings after Save
        self.__click_settings_option("Invoice")
        # Validate invoice data
        self.__validate_invoice(invoice)
        
    def test_debit_note(self):
        debit_note = self.kwargs["debit_note"]
        
        self.ui.click_side_menu("Settings")
        # Select Debit Note Settings
        self.__click_settings_option("Debit Note")
        
        # edit "Debit Note"
        self.ui.enter_text((By.ID, "number_prefix"), debit_note["number_prefix"])
        self.ui.enter_text((By.ID, "number_digit"), debit_note["number_digit"])
        self.ui.enter_text((By.ID, "number_next"), debit_note["next_number"])
 
        self.ui.click_save()
        
        # Re-Select Debit Note Settings after Save
        self.__click_settings_option("Debit Note")
        # Validate Debit Note data
        self.__validate_debit_note(debit_note)
        
    def test_credit_note(self):
        credit_note = self.kwargs["credit_note"]
        
        self.ui.click_side_menu("Settings")
        # Select Credit Note Settings
        self.__click_settings_option("Credit Note")
        
        # edit "Debit Note"
        self.ui.enter_text((By.ID, "number_prefix"), credit_note["number_prefix"])
        self.ui.enter_text((By.ID, "number_digit"), credit_note["number_digit"])
        self.ui.enter_text((By.ID, "number_next"), credit_note["next_number"])
        self.instance.scroll_down()

        self.ui.click_save()
        
        # Re-Select Credit Note Settings after Save
        self.__click_settings_option("Credit Note")
        # Validate Credit Note data
        self.__validate_credit_note(credit_note)
        
    def test_payroll(self):
        run_payroll_advanced = self.kwargs["payroll"]["Run Payroll Advanced"]
        
        self.ui.click_side_menu("Settings")
        # Select Payroll Settings
        self.instance.scroll_down()
        self.__click_settings_option("Payroll")
        
        # select Run Payroll Advanced tab
        locator = (By.XPATH, '//div[@class="row"]//*[text()="Run Payroll Advanced"]')
        self.instance.click_element(locator)

        self.ui.enter_text((By.ID, "run_payroll_prefix"), run_payroll_advanced["number_prefix"])
        self.ui.enter_text((By.ID, "run_payroll_digit"), run_payroll_advanced["number_digit"])
        self.ui.enter_text((By.ID, "run_payroll_next"), run_payroll_advanced["next_number"])
        self.ui.select_dropdown("Account", run_payroll_advanced["account"])
        self.instance.scroll_down()
        self.ui.select_dropdown("Category", run_payroll_advanced["category"])
        self.ui.select_dropdown("Payment Method", run_payroll_advanced["payment_method"])

        self.ui.click_save()
        
        self.ui.click_side_menu("Settings")
        # Re-Select Payroll Settings after Save
        self.instance.scroll_down()
        self.__click_settings_option("Payroll")
        # Validate Payroll data
        self.instance.wait(3)
        self.__validate_payroll(run_payroll_advanced)
        
    def __click_settings_option(self, key):
        locator = (By.XPATH, f'//div[@class="card-body"]//*[text()="{key}"]')
        self.instance.click_element(locator)
        
    def __validate_company(self, company):
        element = self.instance.get_element((By.ID, "name"))
        self.assertEqual(element.get_attribute("value"), company["name"], "Company name is not '{}'".format(company["name"]))
        
        element = self.instance.get_element((By.ID, "email"))
        self.assertEqual(element.get_attribute("value"), company["email_address"], "Company email address is not '{}'".format(company["email_address"]))
        
        element = self.instance.get_element((By.ID, "tax_number"))
        self.assertEqual(element.get_attribute("value"), company["tax_number"], "Company tax number is not '{}'".format(company["tax_number"]))
        
        element = self.instance.get_element((By.ID, "phone"))
        self.assertEqual(element.get_attribute("value"), company["phone"], "Company phone is not '{}'".format(company["phone"]))
        
        element = self.instance.get_element((By.ID, "address"))
        self.assertEqual(element.get_attribute("value"), company["address"], "Company address is not '{}'".format(company["address"]))

    def __validate_localisation(self, localisation):
    
#         element = self.instance.get_element((By.XPATH,'//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Time Zone")]]]//input'))
#         element.click()
#         self.assertEqual(element.get_attribute("placeholder"), localisation["time_zone"], "Time Zone is not '{}'".format(localisation["time_zone"]))
        
        element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Date Format")]]]//input'))
        element.click()
        self.assertEqual(element.get_attribute("placeholder"), localisation["date_format"], "Date format is not '{}'".format(localisation["date_format"]))
        
        element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Date Separator")]]]//input'))
        element.click()
        self.assertEqual(element.get_attribute("placeholder"), localisation["date_separator"], "Date separator is not '{}'".format(localisation["date_separator"]))
        
        element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Percent (%) Position")]]]//input'))
        element.click()
        self.assertEqual(element.get_attribute("placeholder"), localisation["percent_position"], "Percent Position is not '{}'".format(localisation["percent_position"]))
        
        element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Discount Location")]]]//input'))
        element.click()
        self.assertEqual(element.get_attribute("placeholder"), localisation["discount_location"], "Discount location is not '{}'".format(localisation["discount_location"]))
        
    def __validate_currencies(self, currencies):
        
        for currency in currencies:
            self.instance.scroll_down()
            locator = (By.XPATH, f'.//tbody/tr[contains(@class, "row") and ./td[3 and text()="{currency["code"]}"]]')
            elements = self.instance.find_elements(locator)
            
            self.assertEqual(len(elements), 1, "Currency '{}' does not exists".format(currency["code"]))
            logger.info(f"Exists: {currency['code']}")
            self.instance.scroll_to_element(elements[0])
            self.ui.click_edit(elements[0])
        
            element = self.instance.get_element((By.ID, "name"))
            self.assertEqual(element.get_attribute("value"), currency["name"], "Currency name is not '{}'".format(currency["name"]))

            element = self.instance.get_element((By.XPATH,'//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Code")]]]//input'))
            element.click()
            self.assertEqual(element.get_attribute("placeholder"), currency["code"], "Currency code is not '{}'".format(currency["code"]))

            element = self.instance.get_element((By.ID, "rate"))
            self.assertEqual(element.get_attribute("value"), str(currency["rate"]), "Currency rate is not '{}'".format(str(currency["rate"])))

            element = self.instance.get_element((By.XPATH,'//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Precision")]]]//input'))
            element.click()
            self.assertEqual(element.get_attribute("placeholder"), str(currency["precision"]), "Currency precision is not '{}'".format(str(currency["precision"])))

            element = self.instance.get_element((By.ID, "decimal_mark"))
            self.assertEqual(element.get_attribute("value"), str(currency["decimal_mark"]), "Currency decimal mark is not '{}'".format(str(currency["decimal_mark"])))

            element = self.instance.get_element((By.ID, "thousands_separator"))
            self.assertEqual(element.get_attribute("value"), str(currency["thousands_separator"]), "Currency thousands separator is not '{}'".format(str(currency["thousands_separator"])))

            self.instance.scroll_down()

            element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Enabled")]]]//label[contains(@class, "active")]'))
            self.assertEqual(element.text, currency["enabled"], "Currency enabled status is not '{}'".format(currency["enabled"]))

            element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Default Currency")]]]//label[contains(@class, "active")]'))
            self.assertEqual(element.text, currency["default"], "Currency default status is not '{}'".format(currency["default"]))
            
            self.ui.click_cancel()
            self.instance.wait(3)
            
    def __validate_taxes(self, taxes):
        
        for tax in taxes:
            locator = (By.XPATH, f'.//tbody/tr[contains(@class, "row") and //*[text()[contains(., "{tax["name"]}")]]]')
            elements = self.instance.find_elements(locator)

            self.assertEqual(len(elements), 1, "Tax '{}' does not exists".format(tax["name"]))
            logger.info(f"Exists: {tax['name']}")
            self.ui.click_edit(elements[0])

            element = self.instance.get_element((By.ID, "name"))
            self.assertEqual(element.get_attribute("value"), tax["name"], "Tax name is not '{}'".format(tax["name"]))

            element = self.instance.get_element((By.ID, "rate"))
            self.assertEqual(element.get_attribute("value"), str(tax["rate_%"]), "Tax rate is not '{}'".format(str(tax["rate_%"])))

            element = self.instance.get_element((By.XPATH,'//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Type")]]]//input'))
            element.click()
            self.assertEqual(element.get_attribute("placeholder"), tax["type"], "Tax type is not '{}'".format(tax["type"]))    

            self.ui.click_cancel()
            self.instance.wait(3)
            
    def __validate_categories(self, categories):
        
        for category in categories:
            locator = (By.XPATH, f'.//tbody/tr[contains(@class, "row") and ./td[2] and .//a[text()[contains(., "{category["name"]}")]]]')
            elements = self.instance.find_elements(locator)
            
            self.assertEqual(len(elements), 1, "Category '{}' does not exists".format(category["name"]))
            logger.info(f"Exists: {category['name']}")
            self.instance.scroll_to_element(elements[0])
            self.ui.click_edit(elements[0])
            
            element = self.instance.get_element((By.ID, "name"))
            self.assertEqual(element.get_attribute("value"), category["name"], "Category name is not '{}'".format(category["name"]))
            
            element = self.instance.get_element((By.XPATH,'//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Type")]]]//input'))
            element.click()
            self.assertEqual(element.get_attribute("placeholder"), category["type"], "Category type is not '{}'".format(category["type"]))    
            
            element = self.instance.get_element((By.ID, "color"))
            self.assertEqual(element.get_attribute("value"), category["colour"], "Category colour is not '{}'".format(category["colour"]))
            
            element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Enabled")]]]//label[contains(@class, "active")]'))
            self.assertEqual(element.text, category["enabled"], "Category enabled status is not '{}'".format(category["enabled"]))
                       
            self.ui.click_cancel()
            self.instance.wait(3)
            
    def __validate_offline_payments(self, offline_payments):
        
        for payment in offline_payments:
            locator = (By.XPATH, f'.//tbody/tr[contains(@class, "row") and ./td[1 and text()="{payment["name"]}"]]')
            elements = self.instance.find_elements(locator)
            
            self.assertEqual(len(elements), 1, "Offline Payment '{}' does not exists".format(payment["name"]))
            logger.info(f"Exists: {payment['name']}")
            self.ui.click_edit(elements[0])
            self.instance.wait(3)
            
            payment_code = elements[0].text.split(" ")[-2].split(".")[1]
            self.assertEqual(payment_code, payment["code"], "Payment code is not '{}'".format(payment["code"]))
        
            payment_order = elements[0].text.split(" ")[-1]
            self.assertEqual(payment_order, str(payment["order"]), "Payment order is not '{}'".format(str(payment["order"])))
            
            element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Show to Customer")]]]//label[contains(@class, "active")]'))
            print(element.text)
            self.assertEqual(element.text, payment["show_to_customer"], "Category show to customer is not '{}'".format(payment["show_to_customer"]))

            self.instance.wait(3)
            
    def __validate_invoice(self, invoice):
        
        element = self.instance.get_element((By.ID, "number_prefix"))
        self.assertEqual(element.get_attribute("value"), invoice["number_prefix"], "Number prefix is not '{}'".format(invoice["number_prefix"]))
        
        element = self.instance.get_element((By.ID, "number_digit"))
        self.assertEqual(element.get_attribute("value"), str(invoice["number_digit"]), "Number digit is not '{}'".format(str(invoice["number_digit"])))
        
        element = self.instance.get_element((By.ID, "number_next"))
        self.assertEqual(element.get_attribute("value"), str(invoice["next_number"]), "Number next is not '{}'".format(str(invoice["next_number"])))
    
        element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Payment Terms")]]]//input'))
        element.click()
        self.assertEqual(element.get_attribute("placeholder"), invoice["payment_terms"], "Payment Terms is not '{}'".format(invoice["payment_terms"]))
        
        self.instance.scroll_down()
        self.ui.click_cancel()
        
    def __validate_debit_note(self, debit_note):
        
        element = self.instance.get_element((By.ID, "number_prefix"))
        self.assertEqual(element.get_attribute("value"), debit_note["number_prefix"], "Number prefix is not '{}'".format(debit_note["number_prefix"]))
        
        element = self.instance.get_element((By.ID, "number_digit"))
        self.assertEqual(element.get_attribute("value"), str(debit_note["number_digit"]), "Number digit is not '{}'".format(str(debit_note["number_digit"])))
        
        element = self.instance.get_element((By.ID, "number_next"))
        self.assertEqual(element.get_attribute("value"), str(debit_note["next_number"]), "Number next is not '{}'".format(str(debit_note["next_number"])))
        
        self.ui.click_cancel()
        
    def __validate_credit_note(self, credit_note):
        
        element = self.instance.get_element((By.ID, "number_prefix"))
        self.assertEqual(element.get_attribute("value"), credit_note["number_prefix"], "Number prefix is not '{}'".format(credit_note["number_prefix"]))
        
        element = self.instance.get_element((By.ID, "number_digit"))
        self.assertEqual(element.get_attribute("value"), str(credit_note["number_digit"]), "Number digit is not '{}'".format(str(credit_note["number_digit"])))
        
        element = self.instance.get_element((By.ID, "number_next"))
        self.assertEqual(element.get_attribute("value"), str(credit_note["next_number"]), "Number next is not '{}'".format(str(credit_note["next_number"])))
        
        self.instance.scroll_down()
        self.ui.click_cancel()
        
    def __validate_payroll(self, run_payroll_advanced):
        
        element = self.instance.get_element((By.ID, "run_payroll_prefix"))
        self.assertEqual(element.get_attribute("value"), run_payroll_advanced["number_prefix"], "Number prefix is not '{}'".format(run_payroll_advanced["number_prefix"]))
        
        element = self.instance.get_element((By.ID, "run_payroll_digit"))
        self.assertEqual(element.get_attribute("value"), str(run_payroll_advanced["number_digit"]), "Number digit is not '{}'".format(str(run_payroll_advanced["number_digit"])))
        
        element = self.instance.get_element((By.ID, "run_payroll_next"))
        self.assertEqual(element.get_attribute("value"), str(run_payroll_advanced["next_number"]), "Number next is not '{}'".format(str(run_payroll_advanced["next_number"])))
        
        element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Account")]]]//input'))
        element.click()
        self.assertEqual(element.get_attribute("placeholder"), run_payroll_advanced["account"], "Account is not '{}'".format(run_payroll_advanced["account"]))
        print("yes")
        self.instance.scroll_down()
        
        element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Category")]]]//input'))
        element.click()
        self.assertEqual(element.get_attribute("placeholder"), run_payroll_advanced["category"], "Category is not '{}'".format(run_payroll_advanced["category"]))
        print("yes")
        element = self.instance.get_element((By.XPATH, '//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "Payment Method")]]]//input'))
        element.click()
        self.assertEqual(element.get_attribute("placeholder"), run_payroll_advanced["payment_method"], "Payment Method is not '{}'".format(run_payroll_advanced["payment_method"]))
        print("yes")