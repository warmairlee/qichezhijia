import pa
import dictionary
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from xlrd import open_workbook
from xlutils.copy import copy

counter_lock = threading.Lock()


def paodd(i):
    global counter_lock
    driver = webdriver.Firefox()
    length = len(dictionary.urlList)
    lis = dictionary.urlList
    while i <= 1200:
        try:
            list_value = lis[i]
            list2 = list_value.split(":")
            company = list2[0]
            cartype = list2[1]
            carname = list2[2]
            url = list2[3]
            url2 = "https://" + url[:20].replace("www", "car") + "config/series/" + url[20:-41] + ".html"
            driver.get(url2)
            data = driver.page_source
            soup = BeautifulSoup(data, 'lxml')
            if counter_lock.acquire():
                if pa.start(company, cartype, carname, soup):
                    print("第" + str(i) + "个,保存成功")
                else:
                    print("第" + str(i) + "个,保存失败")
                i += 2
                counter_lock.release()
        except:
            pass
    driver.quit()


def paeven(i):
    global counter_lock
    driver = webdriver.Firefox()
    length = len(dictionary.urlList)
    lis = dictionary.urlList
    while i <= 1200:
        try:
            list_value = lis[i]
            list2 = list_value.split(":")
            company = list2[0]
            cartype = list2[1]
            carname = list2[2]
            url = list2[3]
            url2 = "https://" + url[:20].replace("www", "car") + "config/series/" + url[20:-41] + ".html"
            driver.get(url2)
            data = driver.page_source
            soup = BeautifulSoup(data, 'lxml')
            if counter_lock.acquire():
                if pa.start(company, cartype, carname, soup):
                    print("第" + str(i + 2) + "个,保存成功")
                else:
                    print("第" + str(i + 2) + "个,保存失败")
                i += 2
                counter_lock.release()
        except:
            pass
    driver.quit()


threads = []

t1 = threading.Thread(target=paodd, args=(1001,))
threads.append(t1)

t2 = threading.Thread(target=paeven, args=(1000,))
threads.append(t2)

if __name__ == '__main__':
    '''
    #1000-1200
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print("OK")
    '''

    rexcel = open_workbook(r"text/test.xls")
    rows = rexcel.sheets()[0].nrows
    cols = rexcel.sheets()[0].ncols

    excel = copy(rexcel)
    sheet = excel.get_sheet(0)

    driver = webdriver.Firefox()
    length = len(dictionary.urlList)
    lis = dictionary.urlList  # list:URL表
    i = 3001
    for key in lis:
        if i <= int(length):
            try:
                list_value = lis[i]
                list2 = list_value.split(":")
                company = list2[0]
                cartype = list2[1]
                carname = list2[2]
                url = list2[3]
                url2 = "https://" + url[:20].replace("www", "car") + "config/series/" + url[20:-41] + ".html"
                driver.get(url2)
                data = driver.page_source
                soup = BeautifulSoup(data, 'lxml')
                rows = pa.goUrl(company, cartype, carname, soup, rows, cols, sheet)
                print("第" + str(i + 1) + "个,保存成功")
                i += 1
            except:
                pass
    driver.quit()
    excel.save(r"text/test.xls")
    print("OK")

