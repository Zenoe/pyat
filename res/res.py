# -*- coding: utf-8 -*-

import selenium
import time
import os
import random
import getopt, sys
import datetime

print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

sys.path.append('../utils3')
import readConfig as readConfig
from AutoBrowser import *
from utils import *

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "res.conf")

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

def input_data_frame(frameid):
    g_browser.backtodef()
    # g_browser.jumptoFrameByIDfromHere('newFrame')
    g_browser.jumptoFrameByIDfromHere(frameid)
    jobname=g_conf.get(frameid, 'jobname')
    print ("jobname" + jobname)
    g_browser.SendKeyByXXX('taskNameSelect', 'id', jobname)

    # idlist= [ 'resourceForDivisionId', 'datagrid-row-r3-2-3',]
    idlist= [ 'resourceForDivisionId']
    for idele in idlist:
        print (idele)
        g_browser.clickByXXX(idele,'id')


    # DCN
    # g_browser.clickByXXX('//*[@id="datagrid-row-r2-2-3"]/td[1]/div/div')
    # yjy ping tai
    g_browser.clickByXXX('//*[@id="datagrid-row-r2-2-5"]/td[1]/div/div')

    subtypename=g_conf.get(frameid, 'subtype')
    g_browser.SendKeyByXXX('workClassId', 'id', subtypename)
    g_browser.clickByXXX('workClassId', 'id')
    g_browser.clickByXXX('//*[@id="datagrid-row-r3-2-1"]/td[1]/div')
    # wait_until(g_browser.clickByXXX, ['//*[@id="datagrid-row-r4-2-0"]/td[1]/div/div'])
    # g_browser.clickByXXX('datagrid-row-r4-2-0', 'id')

    # 任务分类
    # jobtype=g_conf.get(frameid, 'jobtype')
    # g_browser.SendKeyByXXX('taskClassId', 'id', jobtype)
    # g_browser.clickByXXX('taskClassId', 'id')

    project=g_conf.get(frameid, 'project')
    print ("project:", project)
    g_browser.clickByXXX('projectId', 'id')
    time.sleep(.8)
    g_browser.SendKeyByXXX('projectId', 'id', project)
    time.sleep(.8)
    g_browser.clickByXXX('projectId', 'id')
    #time.sleep(0.8)
    # g_browser.clickByXXX('datagrid-row-r6-2-0', 'id')
    g_browser.clickByXXX('//*[@id="datagrid-row-r4-2-0"]/td[1]/div/div')

    ## modify for "5GNR12.0PJ1"
    #g_browser.clickByXXX('datagrid-row-r6-2-1', 'id')

    # 工作包
    workpack=g_conf.get(frameid, 'workpack')
    print ("workpack:", workpack)
    if workpack:
        print ('workpack is not none')
        g_browser.SendKeyByXXX('projectId', 'id', workpack)
        
        g_browser.clickByXXX('workPackId', 'id')
        # g_browser.clickByXXX('datagrid-row-r7-2-0', 'id')
        g_browser.clickByXXX('//*[@id="datagrid-row-r5-2-0"]/td[1]/div/div')


    phase=g_conf.get(frameid, 'phase')
    print ("phase:", phase)
    g_browser.SendKeyByXXX('stageId', 'id', phase)
    g_browser.clickByXXX('stageId', 'id')
    time.sleep(.8)
    g_browser.clickByXXX('//*[@id="datagrid-row-r5-2-0"]/td[2]/div')
    # textXpath = "//*[text()[contains(.,'%s')]]" % phase
    # targetEle = g_browser.getEleByXXX(textXpath, 'xpath')
    # g_browser.clickByXXX(textXpath)


    activity=g_conf.get(frameid, 'activity')
    g_browser.SendKeyByXXX('activityId', 'id', activity)
    g_browser.clickByXXX('activityId', 'id')
    time.sleep(.8)
    # g_browser.clickByXXX('datagrid-row-r10-2-0', 'id')
    g_browser.clickByXXX('//*[@id="datagrid-row-r6-2-0"]/td[1]/div')
    # lineCount=random.random()
    # print (lineCount)
    # if(float(lineCount) > 0.5):
    #     lineCount = (float(lineCount)- 0.4)
    # print (lineCount)
    lineCount = 1
    lineCount="{0:.1f}".format(lineCount)
    g_browser.SendKeyByXXX('_easyui_textbox_input1', 'id', lineCount)

    g_browser.SendKeyByXXX('_easyui_textbox_input7', 'id', '8')
    extra_time=random.randint(0,2)
    g_browser.SendKeyByXXX('_easyui_textbox_input8', 'id', extra_time)

    finishpercent=g_conf.get(frameid, "finishpercent")
    g_browser.SendKeyByXXX('_easyui_textbox_input9', 'id', finishpercent)

    g_browser.clickByText('保存', 'span')

# def getTime(keytext):
#     ttext=g_browser.find_element_by_xpath("//b[contains(text(), keytext)]").text
#     return ttext[-5:-3]

# def input_res():
#     g_browser.implicitly_wait(5)
#     g_browser.find_element_by_xpath("//a[contains(text(),'编辑')]").click()
#     g_browser.implicitly_wait(5)

#     plan_time=getTime('计 划')
#     actual_time=getTime('总 结')
#     input_data('添加计划', 'plan')
#     tmp = g_browser.find_elements_by_name("plan_planTime")[1]
#     tmp.clear();
#     tmp.send_keys(plan_time)

#     input_data('添加总结', 'summary')
#     tmp = g_browser.find_elements_by_name("summary_workTime")[1]
#     tmp.clear();
#     tmp.send_keys(actual_time)

# def input_data(content, flag):
#     g_browser.implicitly_wait(5)
#     btnxpath=("//span[contains(text(),'%s')]" % (content))
#     g_browser.find_element_by_xpath(btnxpath).click()
#     tmp=g_browser.find_elements_by_name(flag+"_taskName")[1]
#     tmp.click();
#     g_browser.implicitly_wait(5)
#     plan_name=g_conf.get("res", flag+"_name")
#     tmp.send_keys(plan_name)

#     resSelectdict=OrderedDict([(flag+"_resourceForDivisionId", ("无线",0)),
#                                (flag+"_workClassId", ("软件-平台升级/竞争/补齐类/各种临时项目", 0)),
#                                (flag+"_projectId", ("RG-iData_3.00", 1)),
#                                (flag+"_workPackId", ("一键网优", 1)),
#                                (flag+"_taskClassId", ("内部测试支持", 1))])

#     for key,value in resSelectdict.items():
#         print (key)
#         clickSelect(key, value[0], value[1])


def open_res():
    urladdr=g_conf.get("site", "url")
    username=g_conf.get("user", "usr")
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
    input_data_frame('frame1')
    # input_data_frame('frame2')
if __name__ == '__main__':
    # resSelectdict=OrderedDict([("plan_resourceForDivisionId", ("无线",0)),
    #                ("plan_workClassId", ("软件-平台升级/竞争/补齐类/各种临时项目", 0)),
    #                ("plan_projectId", ("RG-iData_3.00", 1)),
    #                ("plan_workPackId", ("一键网优", 1))])
    # for key,value in resSelectdict.items():
    #     print key
    #     print value[0]
    #     print value[1]
    main()
    
    
