from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from log.Log import info
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class Flow_element():
    '''元素数据操作'''
    def __init__(self, driver):
        self.driver: WebDriver = driver
        self.locat_method_dict = {
            "xpath":By.XPATH,
            "id":By.ID,
            "css":By.CSS_SELECTOR,
            "class":By.CLASS_NAME,
            "name":By.NAME
        }

    def location(self, location_method=None, locaton_element=None):
        '''定位操作'''
        # print(location_method,locaton_element

        if location_method != None and locaton_element != None:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((self.locat_method_dict[location_method],locaton_element)))
            self.locat = self.driver.find_element(self.locat_method_dict[location_method], locaton_element)
        else:
            info('定位错误：%s %s' % (location_method, locaton_element))

    def page_operation(self, send_operation=None, data=None, clear_data=None):
        '''数据操作'''
        # self.driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", self.locat,
        # "background:green;border:2px solid red;")
        time.sleep(0.3)

        if send_operation == 'send_keys':
            if clear_data != 'N':
                self.locat.send_keys(Keys.CONTROL + 'a')
                self.locat.send_keys(Keys.BACKSPACE)
            # print(data)
            if data != None:
                self.locat.send_keys(data)
        elif send_operation == 'click':
            # print(self.driver.page_source)
            self.locat.click()
            time.sleep(1)
        elif send_operation == "backspace":  # 清空输入框
            self.locat.send_keys(Keys.CONTROL + 'a')
            self.locat.send_keys(Keys.BACKSPACE)
        elif send_operation == "actionchains":  # 鼠标悬停
            ActionChains(self.driver).move_to_element(self.locat).perform()
        elif send_operation == "text":
            data_text = self.locat.text
            return [data_text]
        elif send_operation == 'value':
            # print(self.driver.page_source)
            return [self.locat.get_attribute('value')]
        elif send_operation == 'is_selected':
            return [str(self.locat.is_selected())]



    def js_operation(self,js_oper):
        self.driver.execute_script(js_oper,self.locat)#"js操作","元素定位"

    def web_operation(self,send_operation):
        if send_operation == "refresh":
            self.driver.refresh()
            time.sleep(1)

    def return_driver(self):
        return self.driver
