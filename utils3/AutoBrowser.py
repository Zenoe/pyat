#!/usr/bin/env python

# -*- coding: utf-8 -*-

from selenium import webdriver
import configparser
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import time

from Log import MyLog as Log
log = Log.get_log()
logger = log.get_logger()


# 设置chromedriver 环境变量
# chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# os.environ["webdriver.chrome.driver"] = chromedriver
# driver = webdriver.Chrome(chromedriver)


# def getBrowser():
# '''standalone function'''
#     options = webdriver.ChromeOptions()
#     prefs= {
#         "profile.managed_default_content_settings.images":1,
#         "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
#         "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,
#     }

#     options.add_experimental_option('prefs', prefs)
#     options.add_argument('--ignore-certificate-errors')
#     options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
#     browser = webdriver.Chrome(chrome_options=options)
#     browser.maximize_window()
#     return browser

def getConf(conf_file):

    try:
        cf = configparser.ConfigParser()
        cf.read(conf_file, encoding='UTF-8')
        return cf
    except Exception as e:
        print ('parse conf err', e)
        pass

    
def send_keys(el, keys):
    for i in range(len(keys)):
        el.send_keys(keys[i])

#send_keys(el, keys)

class AutoBrowser:
    def __init__(self, url):
        logger.info("browser init")
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        #the flag --disable-features=EnableEphemeralFlashPermission has been removed in Chrome 71
        # options.add_argument("--disable-features=EnableEphemeralFlashPermission");
        # prefs= {
        #     "profile.managed_default_content_settings.images":1,
        #     "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
        #     "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,
        # }

        # options.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.maximize_window()
        self.browser.get(url)
        self.waittime=15
        self.typefuncDict={"xpaths": "find_elements_by_xpath","xpath":"find_element_by_xpath", "name": "find_element_by_name", "id": "find_element_by_id", "selector": "find_element_by_css_selector"}

    def SendKeyByXXX(self, ele_value, ele_type, text):
        targetEle=self.getEleByXXX(ele_value, ele_type)
        targetEle.clear()
        # targetEle.send_keys(text)
        send_keys(targetEle, str(text))

    def switchActive(self):
        self.browser.switch_to_active_element()

    def SelectByText(self, selectname, optiontext):
        tmp=Select(g_browser.find_elements_by_name(selectname)[1]).select_by_visible_text(optiontext)

    def clickEleByLiteralText(self, eletype, text):
        self.clickByXXX("//%s[contains(text(),'%s')]" % (eletype, text), 'xpath')

    def clickButtonByValue(self, text, altertive=None):
        self.clickByXXX("//input[contains(@value,'%s')]" % (text), 'xpath')

    def clickByXXX(self, ele_value, ele_type='xpath'):
        # stale element reference: element is not attached to the page document
        # to avoid the StaleElementReferenceException, it must wait for the element to show
        self.browser.implicitly_wait(self.waittime)
        targetEle=self.getEleByXXX(ele_value, ele_type)
        try:
            targetEle.click()
        except StaleElementReferenceException:
            self.mouseMoveClick(targetEle)

    def clickByText(self, text, ele_type):
        xpath=("//%s[contains(text(),'%s')]" %(ele_type, text))
        self.clickByXXX(xpath, 'xpath')
    # def findbyclass(self, class_name):
    #     return self.browser.find_element_by_xpath("//div[contains(@class, 'dT dialogHeader')]")

    def mouseMoveClick(self, targetele):
        self.browser.implicitly_wait(self.waittime)
        # tmp = self.browser.find_element_by_xpath(xpath)
        # if tmp is None:
        #     logger.error("xpath : %s could not be found" % xpath)
        #     return
        self.browser.actions().mouseMove(targetele).perform();
        self.browser.actions().click().perform();

    def jumptoFrameByIDfromHere(self, frameid):
        # self.browser.implicitly_wait(self.waittime)
        # iframe_handle = self.browser.find_element_by_id(frameid)
        # self.browser.switch_to_frame(iframe_handle)

        # can not find frame by src attribute?
        # frame = self.browser.find_element_by_xpath('//*[@src="/refsystem/res_day/daily_work_view.jhtml"]')
        frame = self.browser.find_elements_by_tag_name("iframe")[0]
        self.browser.switch_to_frame(frame)
        frame = self.browser.find_element_by_xpath('//*[@id="frame1"]')
        self.browser.switch_to_frame(frame)

    def jumptoFrameByID(self, frameid):
        self.browser.implicitly_wait(self.waittime)
        self.backtodef()
        iframe_handle = self.browser.find_element_by_id(frameid)
        self.browser.switch_to_frame(iframe_handle)

    def getEleByXXX(self, ele_value, ele_type):
        self.browser.implicitly_wait(self.waittime)
        targetEle = getattr(self.browser, self.typefuncDict[ele_type])(ele_value)
        if targetEle is None:
            print ("xpath : %s could not be found" % ele_value)
            logger.error("xpath : %s could not be found" % ele_value)
            return
        return targetEle

    def getEleTextByXXX(self, ele_value, ele_type):
        targetEle=self.getEleByXXX(ele_value, ele_type)
        return targetEle.text

    def backtodef(self):
        # self.browser.switch_to.parent_frame()
        self.browser.switch_to.default_content()

    def switch_to_alert(self):
        return self.browser.switch_to_alert()

    def performClick(self, ele_value, ele_type):
        ac = ActionChains(self.browser)
        elem=self.getEleByXXX(ele_value, ele_type)
        # ac.move_to_element(elem).move_by_offset(x_off, y_off).click().perform()
        ac.move_to_element(elem).click().perform()
