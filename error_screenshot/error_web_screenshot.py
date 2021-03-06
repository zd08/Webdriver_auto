from selenium.webdriver.remote.webdriver import WebDriver
import os
import time
from log.Log import info

class Screenshoot_web:
    def __init__(self,webdriver):
        self.webdriver:WebDriver = webdriver
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.path_screenshoot = os.path.join(self.path,"screenshot_view",str(time.strftime('%Y_%m_%d_%H_%M_%S' , time.localtime()))+'.png')
    def screenshoot(self):
        '''错误截图'''
        try:
            self.webdriver.get_screenshot_as_file(self.path_screenshoot)
            return self.path_screenshoot
        except:
            info('截图失败')

if __name__ == "__main__":
    Screenshoot_web(1)