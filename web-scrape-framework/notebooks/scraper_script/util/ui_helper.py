from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
import json

class UIHelper():
    def __init__(self, instance, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
    
    def login(self, user_name, password):
#         user_name = self.kwargs["user_name"]
#         password = self.kwargs["password"]
        
        # enter email
        locator = (By.NAME, "email")
        self.instance.enter_text(locator, user_name)

        # enter password
        locator = (By.NAME, "password")
        self.instance.enter_text(locator, password)

        # click login button
        locator = (By.XPATH, './/button[contains(@type, "submit")]')
        self.instance.click_element(locator)

    # side menu functions
    def switch_company(self, company_short_name):
        # click dropdown on side bar
        locator = (By.XPATH, '//div[contains(@class, "sidenav-header")]//a[@class="nav-link"]')
        self.instance.click_element(locator)
        # select company
        locator = (By.XPATH, f'//div[contains(@class, "sidenav-header")]//a[@class="dropdown-item"]//*[text()[contains(., "{company_short_name}")]]')
        self.instance.click_element(locator)
    
    def click_side_menu(self, menu, submenu="None"):
        locator = (By.XPATH, f'//a[contains(@class, "nav-link")]//*[text()[contains(., "{menu}")]]')
        self.instance.click_element(locator)
        if submenu!="None":
            locator = (By.XPATH, f'//a[@class="nav-link"]//*[text()[contains(., "{submenu}")]]')
            self.instance.click_element(locator)
            
    # user profile settings
    def click_user_settings(self, option):
        locator = (By.XPATH, './/div[@id="navbarSupportedContent"]//img[@class="user-img"]')
        self.instance.click_element(locator)
        # click on option
        locator = (By.XPATH, f'.//div[@class="dropdown-menu dropdown-menu-right show"]//*[text()[contains(., "{option}")]]')
        self.instance.click_element(locator)

    # buttons functions
    def click_save(self):
        locator = (By.XPATH, './/button[contains(@type, "submit")]')
        self.instance.click_element(locator)

    def click_add(self):
        locator = (By.XPATH, '//div[@id="header"]//a[//*[text()[contains(., "Add New")]]]')
        self.instance.click_element(locator)
        
    def click_import(self):
        locator = (By.XPATH, '//div[@id="header"]//a[text()[contains(., "Import")]]')
        self.instance.click_element(locator)
        
    def click_export(self):
        locator = (By.XPATH, '//div[@id="header"]//a[text()[contains(., "Export")]]')
        self.instance.click_element(locator)
    
    def click_cancel(self):
        locator = (By.XPATH, './/div[@class="card-footer"]//a')
        self.instance.click_element(locator)

    def __get_actions_dropdown(self, row):
        locator = (By.XPATH, './/div[contains(@class, "dropdown")]')
        dropdown = self.instance.find_element(locator, parent=row)
        if "show" not in dropdown.get_attribute("class"):
            dropdown.click()
        return dropdown

    def click_edit(self, row):
        dropdown = self.__get_actions_dropdown(row)

        locator = (By.XPATH, './/*[text()[contains(., "Edit")]]')
        element = self.instance.find_element(locator, parent=dropdown)
        element.click()
        
    def click_delete(self, row):
        dropdown = self.__get_actions_dropdown(row)

        locator = (By.XPATH, './/button[text()[contains(., "Delete")]]')
        element = self.instance.find_element(locator, parent=dropdown)
        element.click()
        
        # confirm delete
        locator = (By.XPATH, f'//div[@class="modal-content"]//button[.//*[text()[contains(., "Delete")]]]')
        self.instance.click_element(locator)
        locator = (By.XPATH, f'//div[@class="modal-content"]')
        WebDriverWait(self.instance.get_driver(), 15).until(expected_conditions.invisibility_of_element_located(locator))
        
    # control functions
    def enter_text(self, locator, value):
        self.instance.enter_text(locator, value)

    def select_date_picker(self, key, date, wait=1):
        # click dropdown
        locator = (By.XPATH, f'//div[@class="row"]//div[contains(@class, "form-group") and .//*[text()[contains(., "{key}")]]]')
        self.instance.click_element(locator)
        self.instance.wait(wait)
        
        year = date[0:4]
        month = str(int(date[5:7]) - 1)
        day = str(int(date[8:10]))

        self.instance.enter_text((By.XPATH, './/input[@class="numInput cur-year"]'), year)
        self.instance.select_dropdown((By.XPATH, './/select[@class="flatpickr-monthDropdown-months"]'), month)
        locator = (By.XPATH, f'.//div[@class="dayContainer"]//*[text()="{day}" and (@class="flatpickr-day " or @class="flatpickr-day selected")]')
        self.instance.click_element(locator)
        self.instance.wait(wait)

    def select_dropdown(self, key, value, wait=1):
        # click dropdown
        locator = (By.XPATH, f'//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "{key}")]]]')
        self.instance.click_element(locator)
        self.instance.wait(wait)
        # click option
        locator = (By.XPATH, f'//div[@class="el-select-dropdown el-popper" and not(contains(@style, "display: none"))]//li[.//*[text()="{value}"]]') 
        self.instance.click_element(locator)
        self.instance.wait(wait)
        
    def select_dropdown_multiple(self, key, values, wait=1):
        # click dropdown
        locator = (By.XPATH, f'//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "{key}")]]]')
        self.instance.click_element(locator)
        self.instance.wait(wait)
        # click multiple options
        for value in values:
            locator = (By.XPATH, f'//div[@class="el-select-dropdown el-popper is-multiple" and not(contains(@style, "display: none"))]//li[.//*[text()="{value}"]]') 
            self.instance.click_element(locator)
        self.instance.wait(wait)

    def select_toggle_button(self, key, value, wait=1):
        locator = (By.XPATH, f'//div[@class="card-body"]//div[contains(@class, "form-group") and .//*[text()[contains(., "{key}")]]]//label[contains(text(), "{value}")]')
        self.instance.click_element(locator)
    
    def load_data(self, data_path):
        with open(data_path, "r") as file:
            data = file.read()
            data = json.loads(data)
        return data
    
    def import_file(self, file_path):
        # example file_path = "C://Users/putri.wijaya/Downloads/customers.xlsx"
        self.instance.find_element((By.ID, 'projectCoverUploads')).send_keys(file_path)
        # click Import Button
        locator = (By.XPATH, '//div[@class="card-footer"]//button[text()[contains(., "Import")]]')
        self.instance.click_element(locator)
    
    def shortcut(self, wait=1):
        locator = (By.XPATH, '//ul[@class="navbar-nav align-items-center ml-md-auto"]//li[@class="nav-item dropdown"]//i[@class="fas fa-plus"]')
        self.instance.click_element(locator)
        self.instance.wait(wait)
        
        
        