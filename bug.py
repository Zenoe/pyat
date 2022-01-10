# -*- coding: utf-8 -*-
# python bug.py -a CLOSED-ByDevelopment -i 516796
# python bug.py -a RESOLVED -i 557913

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import configparser
import getopt, sys
sys.path.append('./utils3')
import readConfig as readConfig

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "bug.conf")

g_conf = readConfig.ReadConfig(configPath).get_conf()
if(not g_conf):
    print ("null configparser")
    exit
# 设置chromedriver 环境变量
# chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# os.environ["webdriver.chrome.driver"] = chromedriver
# driver = webdriver.Chrome(chromedriver)

def getBrowser():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    browser = webdriver.Chrome(chrome_options=options)
    browser.maximize_window()
    return browser

# def getConf():
#     try:
#         cf = configparser.ConfigParser()
#         cf.read("bug.conf")
#         return cf
#     except Exception as e:
#         print ('parse conf err', e)
#         pass

g_browser = getBrowser()

g_submit=False
g_analysis=''
g_solution=''

def search_bugid(in_browser, in_bugid, p_action):
    search_bugid.try_count = 1
    while(1):
        try:
            search_bugid.try_count += 1
            in_browser.find_element_by_id("inputBugId").send_keys(in_bugid)
            in_browser.find_element_by_id("ext-gen30").click()
            in_browser.implicitly_wait(10)
            break
        except:
            if search_bugid.try_count > 10:
                print ('try more than 10 times')
                break

    iframe_handle = in_browser.find_element_by_xpath("//div[@id='tab_id']//div[@id='tab_bugid_%s']//iframe[@name='iframe_tab_bugid_%s']"%(in_bugid, in_bugid))
    in_browser.switch_to_frame(iframe_handle)

    try:
        tmp = in_browser.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//span[text()='Bug状态']/parent::*/following-sibling::div//div//img")
        tmp.click()
        # tmp3 = in_browser.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//div[text()='RESOLVED']")
        tmp3 = in_browser.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//div[text()='%s']" % p_action)
        tmp3.click()
        al = in_browser.switch_to_alert()
        al.accept()
    except Exception as e:
        print (e)

    if (p_action == "RESOLVED"):
        resolve(in_browser)
    elif(p_action == "CLOSED-ByDevelopment"):
        closeBD(in_browser)

def closeBD(in_browser):
    conf_revision=g_conf.get("bug", "revision")
    ele=in_browser.find_element_by_name("bugInfo.resolvedVersion")
    ele.clear()
    ele.send_keys( conf_revision)

    in_browser.find_element_by_xpath("//button[contains(text(), '提交')]").click()

def resolve(in_browser):
    print ("click checker")
    conf_checker=g_conf.get("bug", "checker")
    click_dropdown(in_browser, '审核人:', conf_checker)

    # check_audit()
    # return

    print ("select work package")
    conf_package=g_conf.get("bug", "package")
    click_dropdown(in_browser, '工作包', conf_package)
    try:
        phase=g_conf.get("bug", "discoverphase")
        # select_bug_discover_phase ( 'bugInfo.discoveryPhase.id', '集成测试')
        print ('select discoverphase')
        select_bug_discover_phase ( 'bugInfo.discoveryPhase.id', phase)
    except Exception as e:
        print (e)

    select_bug_type('bugInfo.bugCategory.id')

    print ('select bug happen time')
    bughappentime=g_conf.get("bug", "bughappentime")
    click_dropdown(in_browser, 'Bug引入的状态', bughappentime)

    resolveway=g_conf.get("bug", "resolveway")
    click_dropdown(in_browser, '解决方式', resolveway)

    isifbug=g_conf.get("bug", "isifbug")
    click_dropdown_span(in_browser, '是否用户接口修订并通过三方评审', isifbug)

    legacybug=g_conf.get("bug", "legacybug")
    click_dropdown(in_browser, '遗留Bug', legacybug)

    # 修订影响面
    fix_effect=g_conf.get("bug", "fix_effect")
    in_browser.find_element_by_name("bugInfo.repairInfluence").send_keys(fix_effect)

    #测试验证点
    testverify=g_conf.get("bug", "testverify")
    in_browser.find_element_by_name("bugInfo.testVerification").send_keys(testverify)

    # 修订量
    print ('modifycount')
    modifycount=g_conf.get("bug", "modifycount")
    in_browser.find_element_by_name("bugInfo.repairOrder").send_keys(modifycount)

    # 是否使用一键收集信息
    print ('onekeycollect')
    onekeycollect=g_conf.get("bug", "onekeycollect")
    click_dropdown(in_browser, '是否使用一键收集信息', onekeycollect)

    #发现bug的组件:
    print ('bugcomponent')
    bugcomponent=g_conf.get("bug", 'bugcomponent')
    in_browser.find_element_by_xpath("//label[contains(text(), '发现bug的组件:')]/..//input").send_keys(bugcomponent)
    # bugcomponent=g_conf.get("bug", "bugcomponent")
    # click_dropdown(in_browser, '发现bug的组件:', bugcomponent)

    resolvedVerification=g_conf.get("bug", "resolvedVerification")
    in_browser.find_element_by_name("bugInfoExp.resolvedVerification").send_keys(resolvedVerification)

    resolvedModuleAffect=g_conf.get("bug", "resolvedModuleAffect")
    in_browser.find_element_by_name("bugInfoExp.resolvedModuleAffect").send_keys(resolvedModuleAffect)

    resolvedProductAffect=g_conf.get("bug", "resolvedProductAffect")
    in_browser.find_element_by_name("bugInfoExp.resolvedProductAffect").send_keys(resolvedProductAffect)

    resolvedAnalyse=g_conf.get("bug", "resolvedAnalyse")
    # bug.conf 文件为utf8编码时要decode
    # in_browser.find_element_by_name("bugInfoExp.resolvedAnalyse").send_keys(resolvedAnalyse.decode('utf-8'))
    # bug.conf 文件为ansi编码了
    in_browser.find_element_by_name("bugInfoExp.resolvedAnalyse").send_keys(resolvedAnalyse)

    resolvedSolution=g_conf.get("bug", "resolvedSolution")
    in_browser.find_element_by_name("bugInfoExp.resolvedSolution").send_keys(resolvedSolution)

def click_dropdown(in_driver, label_text, div_text):
    g_browser.implicitly_wait(2)
    tmp = in_driver.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//label[contains(text(), '%s')]/parent::*/div//img"%(label_text))
    print ('click ', label_text)
    tmp.click()

    # tmp3 = in_driver.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//div[text()='%s']"%(div_text))
    tmp3 = in_driver.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//div[contains(text(), '%s')]"%(div_text))
    tmp3.click()

def check_audit():
    tmp = g_browser.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//label[contains(text(), '%s')]/parent::*/div//input[@type='text']"%('审核人:'))
    # tmp.click()
    tmp.send_keys(Keys.TAB)

    print ('finish sending tab')
    tmp = g_browser.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//label[contains(text(), '%s')]/parent::*/div//input[@name='bugInfo.checked']"%('审核人:'))
    tmp.send_keys(Keys.TAB)
    tmp.click()
    print ('check audit')

def click_hint_dropdown(in_driver, name_id):
    tmp = in_driver.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//Input[contains(@name, '%s')]/parent::*/img"%(name_id))
    tmp.click()

def click_dropdown_span (in_driver, name_id, div_text):
    # click_hint_dropdown(in_driver, name_id)
    # //span[contains(text(), '是否用户接口修订并通过三方评审')]/../..//img
    tmp = in_driver.find_element_by_xpath("//span[contains(text(), '%s')]/../..//img"%(name_id))
    tmp.click()
    select_drop_div(in_driver, div_text)
    print ('click', div_text)

def select_bug_discover_phase(name_id, span_text):
    click_hint_dropdown(g_browser, name_id)
    g_browser.implicitly_wait(1)
    # ( g_browser.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']/div[13]/div/div/div/div/div/ul/div/li[3]/div/a/span[contains(text(), '%s')]"%(span_text)) ).click()
    clickspan_byname(span_text)
    # ( g_browser.find_element_by_xpath("//span[contains(text(), '%s')]"%(span_text)) ).click()
    g_browser.implicitly_wait(1)

def clickspan_byname(name):
    ( g_browser.find_element_by_xpath("//span[contains(text(), '%s')]"%(name)) ).click()
    g_browser.implicitly_wait(1)

def clickplus_byname(name):
    ( g_browser.find_element_by_xpath("//span[contains(text(), '%s')]/../../img"%(name)) ).click()
    g_browser.implicitly_wait(1)

def select_bug_type(name_id):
    print ('select bug type')
    g_browser.implicitly_wait(2)
    click_hint_dropdown(g_browser, name_id)
    # 编码阶段
    waittime=0.5
    bugtype=g_conf.get("bug", "bugtype")
    bugsubtype=g_conf.get("bug", "bugsubtype")
    bugsubsubtype=g_conf.get("bug", "bugsubsubtype")
    clickplus_byname(bugtype)
    # it won't click the disired item if it does not wait for a centain time
    time.sleep(waittime)
    clickplus_byname(bugsubtype)
    time.sleep(waittime)
    clickspan_byname(bugsubsubtype)

def select_drop_div(in_driver, div_text):
    ( in_driver.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//div[contains(text(), '%s')]"%(div_text)) ).click()

def select_product(product_name):
    tmp = g_browser.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//div[1]//div[contains(text(), '%s')]/preceding-sibling::img"%(product_name))
    print ('select product',tmp)
    tmp.click()
    # ( g_browser.find_element_by_xpath("//body[@class='ext-webkit ext-chrome x-border-layout-ct']//div[1]/div[contains(text(), '%s')]"%(product_name)) ).click()

def handle_alert(in_browser):
    if hasattr(handle_alert , "count"):
        pass
    else:
        pass

    handle_alert.count = 1
    if hasattr(handle_alert , "count"):
        pass

    while(1):
        try:
            handle_alert.count += 1
            a = in_browser.switch_to_alert()
            a.accept()   #driver.execute("acceptAlert")
            break
        except ( selenium.common.exceptions.NoAlertPresentException ):
            if ( handle_alert.count > 10 ):
                print ('wait too long')
                break
            time.sleep(0.1)
            print ('sleep ', handle_alert.count)

def open_bug(p_bugid, p_action):
    browser = g_browser
    bugsite=g_conf.get("site", "url")
    username=g_conf.get("user", "usr")
    password=g_conf.get("user", "pwd")

    browser.get(bugsite)
    browser.find_element_by_id("username").send_keys(username)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_name("submit").click()

    handle_alert(browser)

    search_bugid(browser, p_bugid, p_action)

    if g_submit==True:
        print ("auto submit")
    else:
        print ("exit")

def usage():
    print ("i: bugid; a: action; s: autosubmit")

def main():
    bugid=0
    action=''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:i:hs", ["help", "action="])
    except getopt.GetoptError:
        # print (help information and exit:)
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-i":
            bugid=a
        if o in ("-a", "--action"):
            action=a
        if o in ("-h", "--help"):
            usage()
        if o in ("-s"):
            global g_submit
            g_submit=True

    open_bug(bugid, action)

if __name__ == '__main__':
    main()
