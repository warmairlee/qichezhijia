import xlwt
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import sys
import time
import dictionary


def goUrl(company, cartype, carname, url, sheet, rows, cols, num):

    rows = 1
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(1)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    div1 = soup.find("div", class_="sub_nav")
    div = soup.find("div", class_="pzbox")
    div2 = div1.find("div", class_="path")
    div2a = div2.find_all("a")[2]
    # 级别value
    val1 = div2a.get_text()
    # TOP
    divtop = div.find("div", id="config_nav")
    for td in divtop.find_all("td"):
        tddiv = td.find("div", class_="carbox")
        name = company+" "+tddiv.find("a").get_text().strip()
        sheet.write(rows, cols, name)
        rows += 1
    cols += 1

    # BODY
    divbody = div.find("div", class_="conbox")
    flag = 1
    for table in divbody.find_all("table"):
        if flag == 1:
            flag += 1
            continue
        if flag == 2:
            # 第一个TABLE
            for tr in table.find_all("tr"):
                rows = 0
                th = tr.find("th")
                if th.find("div"):
                    thdiv = th.find("div").get_text()
                    titleList[thdiv] = num
                    sheet.write(rows, cols, thdiv)
                    rows += 1
                for td in tr.find_all("td"):
                    tddiv2 = td.find("div").get_text()
                    sheet.write(rows, cols, tddiv2)
                    rows += 1
                flag += 1
                cols += 1
                continue
        else:
            flag2 = True
            # 第二个及之后TABLE
            for tr2 in table.find_all("tr"):
                rows = 0
                if flag2:
                    # 标题
                    h3 = tr2.find("h3")
                    h3span = h3.find("span").get_text()
                    print(h3span)
                    flag2 = False
                    continue
                else:
                    th = tr2.find("th")
                    try:
                        #  按图片照参数
                        small_title_href = th.find("a").get("href")
                        small_title = small_title_href[40:-22]
                        small_title = dictionary.dic[small_title]
                        sheet.write(rows, cols, small_title)
                        rows += 1
                        if small_title == "厂商":
                            car_value = cartype + "  "
                            for td22 in tr2.find_all("td"):
                                sheet.write(rows, cols, car_value)
                                rows += 1
                        elif small_title == "级别":
                            car_value = val1
                            for td33 in tr2.find_all("td"):
                                sheet.write(rows, cols, car_value)
                                rows += 1
                        else:
                            for td2 in tr2.find_all("td"):
                                td2div = td2.find("div").get_text()
                                car_value = td2div
                                sheet.write(rows, cols, car_value)
                                rows += 1
                        cols += 1
                    except:
                        # 文字找参数
                        rows = 0
                        try:
                            small_title = th.find("span").get_text()
                            sheet.write(rows, cols, small_title)
                            for trtd in tr2.find_all("td"):
                                trtddiv = trtd.find("div").get_text()
                                sheet.write(rows, cols, trtddiv)
                                rows += 1
                        except:
                            pass
            flag += 1
            continue
    driver.quit()
    return str(rows) + ":" + str(cols)


if __name__ == '__main__':
    num = 0
    f = open("text/titleList.txt", "r", encoding="utf-8")
    d = f.read()
    titleList = eval(d)
    f.close()

    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet("carInfo")

    list = dictionary.urlList
    list2 = list[6].split(":")
    company = list2[0]
    cartype = list2[1]
    carname = list2[2]
    url = list2[3]
    url2 = "https://" + url[:20].replace("www", "car") + "config/series/" + url[20:-41] + ".html"
    rows = 0
    cols = 0
    randc = goUrl(company, cartype, carname, url2, sheet, rows, cols, num)
    rows = randc.split(":")[0]
    cols = randc.split(":")[1]
    book.save('text/carInfo6.xls')
    f = open("text/titleList.txt", "w", encoding="utf-8")
    f.write(str(titleList))
    f.close()


