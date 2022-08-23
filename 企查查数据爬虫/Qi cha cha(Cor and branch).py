# 一*-coding : utf-8 -*-
# author: Canden Cao time: 2021/10/12
# from selenium.webdriver import chrome
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import csv
from lxml import etree, html
import re
from msedge.selenium_tools import EdgeOptions, Edge  # Edge效果同selenium中的Edge
from selenium import webdriver


# 对外投资信息
def Basic_invest(html_source):
    # 通过lxml.html将源码解析成一个DOM树（https://www.yuanrenxue.com/crawler/python-lxml-usage.html），返回一个对象
    Html = html.fromstring(html_source)
    # 通过xpath获取网页中的表格数据'//*[@id="touzilist"]/div[2]/table'
    try:
        table = Html.xpath('//*[@id="touzilist"]/div[4]/table')[0]  # 由于table是一个包着table对象的列表，因此取第一个元素
    except:
        table = Html.xpath('//*[@id="touzilist"]/div[2]/table')[0]
    # print(html.tostring(table).decode("utf-8"))  #查看源码转化后的网页格式
    trs = table.xpath("./tr")[1:]  # 不要第一行，取表格内容
    for tr in trs:
        Inve = tr.xpath('./td')[1].xpath('./div/span[2]/span/a/text()')[0]  # 网页中存在着伪元素(
        # ::before、：：after)，无法精准定位，只能胡子眉毛一把抓
        Date = tr.xpath('./td')[6].xpath('./span/text()')[0]
        Inve_Pro = tr.xpath('./td')[4].xpath('./span/text()')[0]
        Station = tr.xpath('./td')[7].xpath('./span/span/text()')[0]
        data1 = (Inve, Date, Inve_Pro, Station)
        basic_invest.append(data1)
        # print(Inve, Date, Inve_Pro, Amount, Station)


def Basic_holding(html_source):
    # 通过lxml.html将源码解析成一个DOM树（https://www.yuanrenxue.com/crawler/python-lxml-usage.html），返回一个对象
    Html = html.fromstring(html_source)
    # 通过xpath获取网页中的表格数据
    table = Html.xpath('//*[@id="ipocgkglist"]/div[2]/table')[0]  # 由于table是一个包着table对象的列表，因此取第一个元素
    # print(html.tostring(table).decode("utf-8"))  #查看源码转化后的网页格式
    trs = table.xpath("./tr")[1:]  # 不要第一行，取表格内容
    for tr in trs:
        try:
            Inve = tr.xpath('./td')[1].xpath('./div/span[2]/span/a/text()')[0]
        except:
            Inve = tr.xpath('./td')[1].xpath('./div/span[2]/span/span/text()')[0]
        Rela = tr.xpath('./td')[2].xpath('./span/text()')[0]
        Inve_Pro = tr.xpath('./td')[4].xpath('./span/text()')[0]
        data1 = (Inve, Rela, Inve_Pro)
        basic_holding.append(data1)
        # print(Inve, Date, Inve_Pro, Amount, Station)


def Basic_branch(html_source):
    Html = html.fromstring(html_source)
    # 通过xpath获取网页中的表格数据
    table = Html.xpath('//*[@id="branchelist"]/div[2]/table')[0]  # 由于table是一个包着table对象的列表，因此取第一个元素
    # print(html.tostring(table).decode("utf-8"))  #查看源码转化后的网页格式
    trs = table.xpath('./tr')[1:]  # 不要第一行，取表格内容
    for tr in trs:
        Name = tr.xpath('./td')[1].xpath('./div/span[2]/span/a/text()')[0].strip()  # 网页中存在着伪元素(
        # ::before、：：after)，无法精准定位，只能胡子眉毛一把抓
        Station = tr.xpath('./td')[3].xpath('./span/span/text()')[0]
        data2 = (Name, Station)
        basic_branch.append(data2)
        # print(Name, Station)


def MotherCor(html_source):
    Html = html.fromstring(html_source)
    try:
        station = Html.xpath('//*[@id="cominfo"]/div[2]/table/tr[2]/td[4]/text()')[0].strip()
        start = Html.xpath('//*[@id="cominfo"]/div[2]/table/tr[2]/td[6]/text()')[0].strip()
        end = Html.xpath('//*[@id="cominfo"]/div[2]/table/tr[3]/td[6]/text()')[0].strip()
        with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(['--------------------------------------------------------'])
            writer.writerow((j, Query, station, start, end))
        print('--------------------------------------------------------')
        print(j, Query, station, start, end)
    except:
        with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
            writer = csv.writer(fp)
            writer.writerow(['--------------------------------------------------------'])
            writer.writerow((j, Query, '无'))
        print('--------------------------------------------------------')
        print(j, Query, '无')


if __name__ == '__main__':
    # 将公司一列变成列表
    data = pd.read_excel('D:\Desktop\城市连锁网络\城市连连锁网络所需公司.xlsx', 'Sheet3', header=0)['公司'].values.tolist()
    # 从中断处继续查询
    data = data[data.index('江苏兴荣髙新科技股份有限公司'):data.index('大连船舶重工集团有限公司')]  #列表并不会遍历最后一个元素
    data01 = ['金红叶纸业集团有限公司 ']
        # 使用已经打开的浏览器进行模拟
    edgeoptions = EdgeOptions()
    edgeoptions.use_chromium = True
    edgeoptions.add_experimental_option('debuggerAddress', '127.0.0.1:9222')  # 127.0.01是本机的IP地址,9222是指定的端口号
    web = Edge(r"D:\Python\msedgedriver.exe", options=edgeoptions)
    time.sleep(0.5)

    for j in data:
        # 转移到第一个窗口
        web.switch_to.window(web.window_handles[0])
        # 清空搜索框
        web.find_element_by_xpath('//*[@id="searchKey"]').clear()
        # 输入公司
        web.find_element_by_xpath('//*[@id="searchKey"]') \
            .send_keys(j, Keys.ENTER)
        time.sleep(0.5)
        HTML = html.fromstring(web.page_source)
        try:
            try:
                # 使用string提出父目录(即xpath(.))下面全部子孙文本 /html/body/div[1]/div[2]/div[2]/div[4]/div/div[2]/div/table/tr[1]/td[3]/div/a[1]/span
                Query = (
                    HTML.xpath('/html/body/div[1]/div[2]/div[2]/div[3]/div/div[2]/div/table/tr[1]/td[3]/div/a[1]/span')[0].xpath('string(.)'))
                click_button = web.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[2]/div[3]/div/div[2]/div/table/tr[1]/td[3]/div/a[1]/span/em[1]")
                web.execute_script("arguments[0].click();", click_button)
            except:
                Query = (
                    HTML.xpath('/html/body/div[1]/div[2]/div[2]/div[5]/div/div[2]/div/table/tr[1]/td[3]/div/a[1]/span')[
                        0].xpath('string(.)'))
                click_button = web.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[2]/div[5]/div/div[2]/div/table/tr[1]/td[3]/div/a[1]/span/em[1]")
                web.execute_script("arguments[0].click();", click_button)  # 使用当模拟点击失灵时,使用脚本来进行模拟
        except:
            Query = (
                HTML.xpath('/html/body/div[1]/div[2]/div[2]/div[4]/div/div[2]/div/table/tr[1]/td[3]/div/a[1]/span')[0]
                    .xpath('string(.)'))
            click_button = web.find_element_by_xpath(
                "/html/body/div[1]/div[2]/div[2]/div[4]/div/div[2]/div/table/tr[1]/td[3]/div/a[1]/span/em[1]")
            web.execute_script("arguments[0].click();", click_button)
        # # 获取全部浏览器窗口，返回窗口列表
        # windows = web.window_handles
        # 将窗口定位至最后一个窗口
        web.switch_to.window(web.window_handles[-1])
        time.sleep(0.5)
        # 采取公司相关信息
        # 既有分支机构也有对外投资信息上市信息：/html/body/div[1]/div[2]/div[3]/div/div/div[1]/a[1]/h2；基本信息：/html/body/div[1]/div[2]/div[3]/div/div/div[1]/a[2]/h2
        try:
            button = web.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/a/h2[contains(text(),"基本信息")]')
        except:
            button = web.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/a/h2[contains(text(),"上市信息")]')
        web.execute_script("arguments[0].click();", button)
        time.sleep(1)
        Source_M = web.page_source
        MotherCor(Source_M)
        try:
            # 分支机构数
            num = web.find_element_by_xpath('//*[@id="branchelist"]/div[1]/span[1]').text
            with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                writer = csv.writer(fp)
                writer.writerow(('分支机构真实数', num))
            print('分支机构真实数', num)
            Page_all = int(num) // 10
            # 采集分支机构信息
            basic_branch = [('公司', '状态'), (j, Query + '(' + num + ')')]
            # 返回窗口的网页源码
            Source = web.page_source
            Basic_branch(Source)
            for i in range(Page_all):
                # 点击下一页
                try:
                    click_button = web.find_element_by_xpath(f'//*[@id="branchelist"]/div[2]/nav/ul/li/a[text()={i}+2]')
                except:
                    break
                web.execute_script("arguments[0].click();", click_button)  # 由于标签重复，左右无法点击，所以需要通过这点代码来解决问题
                time.sleep(0.8)
                Source = web.page_source
                Basic_branch(Source)
            # 消除重复行
            basic_branch01 = pd.DataFrame(basic_branch[1:], columns=basic_branch[0])
            basic_branch02 = basic_branch01.drop_duplicates()
            basic_branch = basic_branch02.values
            get_sum = len(basic_branch)-1
            if get_sum != int(num):
                click_button = web.find_element_by_xpath(f'//*[@id="branchelist"]/div[2]/nav/ul/li/a[text()={Page_all}+1]')
                web.execute_script("arguments[0].click();", click_button)
                Source = web.page_source
                Basic_branch(Source)
            # print(basic_branch)
            with open("D:/Desktop/分支机构表1.csv", "a", encoding="utf-8", newline='') as fp:
                writer = csv.writer(fp)
                writer.writerow(['--------------------------------------------------------'])
                writer.writerows(basic_branch)
            with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                writer = csv.writer(fp)
                writer.writerow(('分支机构获取数', get_sum))
            print('分支机构获取数', get_sum)

            try:
                # 查询对外对外参股控股信息
                try:
                    button = web.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div/div/a/h2[contains(text(),"上市信息")]')
                except:
                    button = web.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div/div/a/h2[contains(text(),"基本信息")]')
                web.execute_script("arguments[0].click();", button)
                time.sleep(1)
                num3 = web.find_element_by_xpath('//*[@id="ipocgkglist"]/div[1]/span[1]').text
                with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                    writer = csv.writer(fp)
                    writer.writerow(('对外参股控股真实数', num3))
                print('对外参股控股真实数', num3)
                Page_all = int(num3) // 10
                basic_holding = [("参控股企业名称", "参控关系", "投股比例"), (j, Query + '(' + num3 + ')')]
                # 返回窗口的网页源码
                Source0 = web.page_source
                Basic_holding(Source0)
                for i in range(Page_all):
                    # 点击下一页对外投资
                    try:
                        click_button = web.find_element_by_xpath(f'//*[@id="ipocgkglist"]/div[2]/nav/ul/li/a[text()={i}+2]')
                    except:
                        break
                    web.execute_script("arguments[0].click();", click_button)  # 由于标签重复，左右无法点击，所以需要通过这点代码来解决问题
                    time.sleep(0.8)
                    Source = web.page_source
                    Basic_holding(Source)
                basic_holding01 = pd.DataFrame(basic_holding[1:], columns=basic_holding[0])
                basic_holding02 = basic_holding01.drop_duplicates()
                basic_holding = basic_holding02.values
                get_sum = len(basic_holding) - 1
                if get_sum != int(num3):
                    click_button = web.find_element_by_xpath(
                        f'//*[@id="ipocgkglist"]/div[2]/nav/ul/li/a[text()={Page_all}+1]')
                    web.execute_script("arguments[0].click();", click_button)
                    Source = web.page_source
                    Basic_holding(Source)
                with open("D:/Desktop/对外投资表1.csv", "a", encoding="utf-8", newline='') as fp:
                    writer = csv.writer(fp)
                    writer.writerow(['--------------------------------------------------------'])
                    writer.writerows(basic_holding)
                with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                    writer = csv.writer(fp)
                    writer.writerow(('对外参股控股获取数',  get_sum))
                print('对外参股控股获取数',  get_sum)
                web.close()
            except:
                # 采集公司对外投资信息
                try:
                    button = web.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div/div/a/h2[contains(text(),"基本信息")]')
                except:
                    button = web.find_element_by_xpath(
                        '/html/body/div[1]/div/div/div/div/div/a/h2[contains(text(),"上市信息")]')
                web.execute_script("arguments[0].click();", button)
                time.sleep(1)
                try:
                    num2 = web.find_element_by_xpath('//*[@id="touzilist"]/div[3]/span[1]').text  # 对外投资数
                except:
                    num2 = web.find_element_by_xpath('//*[@id="touzilist"]/div[1]/span[1]').text
                with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                    writer = csv.writer(fp)
                    writer.writerow(('对外投资真实数', num2))
                print('对外投资真实数', num2)
                Page_all = int(num2) // 10  # 下一页需要点击次数
                # 创建列表
                basic_invest = [("公司", "成立日期", "投资占比", "状态"), (j, Query + '(' + num2 + ')')]
                # 返回窗口的网页源码
                Source1 = web.page_source
                Basic_invest(Source1)
                for i in range(Page_all):
                    # 点击下一页对外投资<a href="javascript:void(0)">"&gt;")</a>//*[@id="touzilist"]/div[2]/nav/ul/li[8]/a
                    try:
                        click_button = web.find_element_by_xpath(f'//*[@id="touzilist"]/div[4]/nav/ul/li/a[text()={i}+2]')
                    except:
                        try:
                            click_button = web.find_element_by_xpath(f'//*[@id="touzilist"]/div[2]/nav/ul/li/a[text()={i}+2]')  #//*[@id="touzilist"]/div[2]/nav/ul/li[2]/a
                        except:
                            break
                    web.execute_script("arguments[0].click();", click_button)  # 由于标签重复，所以需要通过JS脚本代码来解决问题//*[@id="touzilist"]/div[2]/nav/ul/li[9]
                    time.sleep(0.8)  #web.execute_script("arguments[0].click();", click_button)
                    Source2 = web.page_source
                    Basic_invest(Source2)
                basic_invest01 = pd.DataFrame(basic_invest[1:], columns=basic_invest[0])
                basic_invest02 = basic_invest01.drop_duplicates()
                basic_invest = basic_invest02.values
                get_sum = len(basic_invest)-1
                if get_sum != int(num2):
                    try:
                        click_button = web.find_element_by_xpath(f'//*[@id="touzilist"]/div[4]/nav/ul/li/a[text()={Page_all}+1]')
                    except:
                        click_button = web.find_element_by_xpath(f'//*[@id="touzilist"]/div[2]/nav/ul/li/a[text()={Page_all}+1]')
                    web.execute_script("arguments[0].click();", click_button)
                    Source = web.page_source
                    Basic_invest(Source)
                with open("D:/Desktop/对外投资表1.csv", "a", encoding="utf-8", newline='') as fp:
                    writer = csv.writer(fp)
                    writer.writerow(['--------------------------------------------------------'])
                    writer.writerows(basic_invest)
                with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                    writer = csv.writer(fp)
                    writer.writerow(('对外投资获取数', get_sum))
                print('对外投资获取数', get_sum)
                web.close()



        except:
            try:
                try:
                    # 查询对外对外参股控股信息
                    try:
                        button = web.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div/div/div/a/h2[contains(text(),"上市信息")]')
                    except:
                        button = web.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div/div/div/a/h2[contains(text(),"基本信息")')
                    web.execute_script("arguments[0].click();", button)
                    time.sleep(1)
                    num3 = web.find_element_by_xpath('//*[@id="ipocgkglist"]/div[1]/span[1]').text
                    with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                        writer = csv.writer(fp)
                        writer.writerow(('分支机构数', '无'))
                        writer.writerow(('对外参股控股真实数', num3))
                    print('分支机构数', '无')
                    print('对外参股控股真实数', num3)
                    Page_all = int(num3) // 10
                    basic_holding = [("参控股企业名称", "参控关系", "投股比例"), (j, Query + '(' + num3 + ')')]
                    # 返回窗口的网页源码
                    Source3 = web.page_source
                    Basic_holding(Source3)
                    for i in range(Page_all):
                        # 点击下一页控股信息//*[@id="ipocgkglist"]/div[2]/nav/ul/li[2]/a
                        try:
                            click_button = web.find_element_by_xpath(f'//*[@id="ipocgkglist"]/div[2]/nav/ul/li/a[text()={i}+2]')
                        except:
                            break
                        web.execute_script("arguments[0].click();", click_button)  # 由于标签重复，左右无法点击，所以需要通过这点代码来解决问题
                        time.sleep(0.8)
                        Source = web.page_source
                        Basic_holding(Source)
                    basic_holding01 = pd.DataFrame(basic_holding[1:], columns=basic_holding[0])
                    basic_holding02 = basic_holding01.drop_duplicates()
                    basic_holding = basic_holding02.values
                    get_sum = len(basic_holding)-1
                    if get_sum != int(num3):
                        click_button = web.find_element_by_xpath(f'//*[@id="ipocgkglist"]/div[2]/nav/ul/li/a[text()={Page_all}+1]')
                        web.execute_script("arguments[0].click();", click_button)
                        Source = web.page_source
                        Basic_holding(Source)
                    with open("D:/Desktop/控股表1.csv", "a", encoding="utf-8", newline='') as fp:
                        writer = csv.writer(fp)
                        writer.writerow(['--------------------------------------------------------'])
                        writer.writerows(basic_holding)
                    with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                        writer = csv.writer(fp)
                        writer.writerow(('对外参股控股获取数',  get_sum))
                    print('对外参股控股获取数',  get_sum)
                    web.close()

                except:
                    # 采集公司对外投资信息
                    try:
                        button = web.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div/div/div//h2[contains(text(),"基本信息")]')
                    except:
                        button = web.find_element_by_xpath(
                            '/html/body/div[1]/div/div/div/div/div//h2[contains(text(),"上市信息")]')
                    web.execute_script("arguments[0].click();", button)
                    time.sleep(1)
                    try:
                        num2 = web.find_element_by_xpath('//*[@id="touzilist"]/div[3]/span[1]').text  # 对外投资数//*[@id="touzilist"]/div[1]/span[1]
                    except:
                        num2 = web.find_element_by_xpath('//*[@id="touzilist"]/div[1]/span[1]').text
                    with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                        writer = csv.writer(fp)
                        writer.writerow(('分支机构数', '无'))
                        writer.writerow(('对外投资真实数',  num2))
                    print('分支机构数', '无')
                    print('对外投资真实数',  num2)
                    Page_all = int(num2) // 10
                    basic_invest = [("公司", "成立日期", "投资占比", "状态"), (j, Query + '(' + num2 + ')')]
                    # 返回窗口的网页源码
                    Source4 = web.page_source
                    Basic_invest(Source4)
                    for i in range(Page_all):
                        # 点击下一页对外投资
                        try:
                            click_button = web.find_element_by_xpath(f'//*[@id="touzilist"]/div[4]/nav/ul/li/a[text()={i}+2]')
                        except:
                            try:
                                click_button = web.find_element_by_xpath(
                                    f'//*[@id="touzilist"]/div[2]/nav/ul/li/a[text()={i}+2]')
                            except:
                                break
                        web.execute_script("arguments[0].click();", click_button)  # 由于标签重复，左右无法点击，所以需要通过这点代码来解决问题
                        time.sleep(0.8)
                        Source = web.page_source
                        Basic_invest(Source)
                    basic_invest01 = pd.DataFrame(basic_invest[1:], columns=basic_invest[0])
                    basic_invest02 = basic_invest01.drop_duplicates()
                    basic_invest = basic_invest02.values
                    get_sum = len(basic_invest)-1
                    if get_sum != int(num2):
                        try:
                            click_button = web.find_element_by_xpath(f'//*[@id="touzilist"]/div[4]/nav/ul/li/a[text()={Page_all}+1]')
                        except:
                            click_button = web.find_element_by_xpath(f'//*[@id="touzilist"]/div[2]/nav/ul/li/a[text()={Page_all}+1]')
                        web.execute_script("arguments[0].click();", click_button)
                        Source = web.page_source
                        Basic_invest(Source)
                    with open("D:/Desktop/对外投资表1.csv", "a", encoding="utf-8", newline='') as fp:
                        writer = csv.writer(fp)
                        writer.writerow(['--------------------------------------------------------'])
                        writer.writerows(basic_invest)
                    with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                        writer = csv.writer(fp)
                        writer.writerow(('对外投资获取数', get_sum))
                    print('对外投资获取数', get_sum)
                    web.close()

            except:
                with open("D:/Desktop/信息表1.csv", "a", encoding="utf-8", newline='') as fp:
                    writer = csv.writer(fp)
                    writer.writerow(('分支机构数', '无'))
                    writer.writerow(('对外参股控股数', '无'))
                    writer.writerow(('对外投资数', '无'))
                print('分支机构数', '无')
                print('对外参股控股数', '无')
                print('对外投资数', '无')
                web.close()
