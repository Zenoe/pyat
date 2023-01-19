# -*- coding: utf-8 -*-

import selenium
import time
import os
import random
import getopt, sys
import datetime
import re
from selenium.webdriver.common.keys import Keys
print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))


sys.path.append('../utils3')
from Log import MyLog as Log
log = Log.get_logger_instance('./log')
logger = log.get_logger()

sys.path.append('../utils3')
import readConfig as readConfig
from AutoBrowser import *
from utils import *

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "getRouterVer.conf")

g_conf = readConfig.ReadConfig(configPath).get_conf()
g_submit = False


def handle_alert(in_browser):
    if hasattr(handle_alert, "count"):
        pass
    else:
        pass

    handle_alert.count = 1
    if hasattr(handle_alert, "count"):
        pass

    while(1):
        try:
            handle_alert.count += 1
            a = in_browser.switch_to_alert()
            a.accept()   #driver.execute("acceptAlert")
            break
        except ( selenium.common.exceptions.NoAlertPresentException ):
            if ( handle_alert.count > 10 ):
                print (('wait too long'))
                break
            time.sleep(0.1)
            print ('sleep ', handle_alert.count)

def clickSelect(selectname, optiontext, closeFlag):
    g_browser.implicitly_wait(3)
    tmp=Select(g_browser.find_elements_by_name(selectname)[1]).select_by_visible_text(optiontext)
    if closeFlag == 0:
        return
    tmp=g_browser.find_element_by_id("filterSelectClose")

    try:
        if tmp is not None:
            print ("click close btn")
            tmp.click()
            print ("click close btn")
    except selenium.common.exceptions.ElementNotVisibleException:
        print ("element not interactable")
        pass

def get_data():
    g_browser.backtodef()
    confSecName='osinfo'
    branch=g_conf.get(confSecName, 'branch')
    print ("branch" + branch)

    product=g_conf.get(confSecName, 'product')
    print ("product" + product)

    # ttext=g_browser.getEleByXXX("//*[contains(text(),'" +product+ "')]", 'xpaths')
    elements=g_browser.getEleByXXX("//td[(text()='" +product+ "')]", 'xpaths')
    bfound = False
    osDownloadUrl = None
    passRate = ''
    testDate = ''

    date_regex = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$')
    for ele in elements:
        if bfound is True:
            break
        parentElement = ele.find_element_by_xpath('./..')
        cells = parentElement.find_elements_by_tag_name('td')
        for cell in cells:
            text = cell.text
            if(text == branch):
                bfound = True
            if(text.startswith('http')):
                osDownloadUrl = cell
            if(text.endswith('%')):
                passRate = text
            if(date_regex.search(text)):
                testDate = text


    logger.warning('passRate: ' + passRate)
    logger.info('passRate: ' + passRate)
    logger.info('testDate: ' + testDate)

    if passRate != '100%':
        logger.warning('testDate: ' + testDate)
        return
    hrefEle = osDownloadUrl.find_elements_by_tag_name('a')
    hrefEle[0].click()
    time.sleep(0.2)

    g_browser.switchWindow()
    installBinHref = g_browser.getEleByXXX("//a[contains(text(), 'install.bin')]", 'xpath')
    print(installBinHref.get_attribute("href"))

    import datetime
    # The programme is executed after midnight, so here we need to go back two days
    twodaysb4 = datetime.datetime.now() - datetime.timedelta(days=2)
    formattedTwodaysb4 = twodaysb4.strftime("%Y-%m-%d")
    print('wanted date', formattedTwodaysb4)

    trEle = installBinHref.find_element_by_xpath('../..')
    cells = trEle.find_elements_by_tag_name('td')
    for cell in cells:
        text = cell.text
        if(text.startswith(formattedTwodaysb4)):
            print('')
    print(trEle.text)
    # osDownloadUrl.click()
    # osDownloadUrl.send_keys(Keys.ENTER)
# def getTime(keytext):
#     ttext=g_browser.find_element_by_xpath("//b[contains(text(), keytext)]").text
#     return ttext[-5:-3]


def open_res():
    urladdr=g_conf.get("site", "url")
    username=g_conf.get("user", "usr")
    print('user' + username)
    password=g_conf.get("user", "pwd")

    global g_browser
    g_browser=AutoBrowser(urladdr)
    browser = g_browser
    nameXpath = "//input[@name='username']"
    passXpath = "//input[@type='password']"
    browser.SendKeyByXXX(nameXpath, 'xpath', username)
    browser.SendKeyByXXX(passXpath, 'xpath', password)
    submitXpath ="//button[@type='submit']"
    browser.clickByXXX(submitXpath, 'xpath')

    handle_alert(browser)

    # g_browser.jumptoFrameByIDfromHere('newFrame')
    # browser.clickEleByLiteralText('div', '日报')

def usage():
    print ("i: idata_url; a: action; s: autosubmit")

def main():
    idata_url=0
    action=''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:i:hs", ["help"])
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-i":
            idata_url=a
        if o == "-p":
            port=a
        if o in ("-h", "--help"):
            usage()
        if o in ("-s"):
            global g_submit
            g_submit=True


    open_res()
    get_data()
if __name__ == '__main__':
    main()
