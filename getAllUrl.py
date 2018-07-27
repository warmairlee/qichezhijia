from bs4 import BeautifulSoup
from selenium import webdriver
import time

def getAllUrl():
    list = []
    driver = webdriver.Firefox()
    url = "https://www.autohome.com.cn/car/#pvareaid=3311275"
    driver.get(url)
    j = 25
    while j >= 0:
        time.sleep(0.2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        j -= 1
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    data1 = soup.find("div", class_="tab-content-item")
    for datauibox in data1.find_all("div", class_="uibox"):
        data3 = datauibox.find("div", class_="uibox-con rank-list rank-list-pic")
        for datadl in data3.find_all("dl"):
            '''大标题'''
            dt = datadl.find("dt")
            dtdiv = dt.find("div")
            big_title = dtdiv.find("a").get_text()
            '''小标题'''
            dd = datadl.find("dd")
            dddiv = dd.find("div",class_="h3-tit")
            small_title = dddiv.find("a").get_text()
            '''车型'''
            for dataul in datadl.find_all("ul"):
                for datali in dataul.find_all("li"):
                    if datali.find("a"):
                        carsrc = datali.find("a").get("href")
                        carname = datali.find("a").get_text()
                        list.append(big_title+":"+small_title+":"+carname+":"+carsrc[2:])
                        print("\""+big_title+":"+small_title+":"+carname+":"+carsrc[2:]+"\",")

getAllUrl()