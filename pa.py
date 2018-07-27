from bs4 import BeautifulSoup
from selenium import webdriver
from xlrd import open_workbook
from xlutils.copy import copy
import time
import dictionary
from bs4 import BeautifulSoup
import urllib.request
import traceback


def goUrl(company, cartype, carname, soup, rows, cols, sheet):
    f = open("text/titleList.txt", "r", encoding="utf-8")
    dic = f.read()
    titleList = eval(dic)
    f.close()
    num = 0
    try:
        div = soup.find("div", class_="pzbox")
        div1 = soup.find("div", class_="sub_nav")
        div2 = div1.find("div", class_="path")
        div2a = div2.find_all("a")[2]
        # 级别value
        val1 = div2a.get_text()
        # TOP
        divtop = div.find("div", id="config_nav")
        nrows = rows+1

        for td in divtop.find_all("td"):
            try:
                tddiv = td.find("div", class_="carbox")
                name = company+" "+tddiv.find("a").get_text().strip()
                sheet.write(nrows, 0, name)
                nrows += 1
                num += 1
            except Exception as err:
                pass

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
                    nrows = rows+1
                    th = tr.find("th")
                    if th.find("div"):
                        thdiv = th.find("div").get_text()
                        if thdiv in titleList:
                            ncols = titleList[thdiv]
                        else:
                            titleList[thdiv] = len(titleList)
                            ncols = titleList[thdiv]
                            sheet.write(0, ncols, thdiv)
                            cols += 1
                    num1 = 0
                    for td in tr.find_all("td"):
                        if num1 < num:
                            tddiv2 = td.find("div").get_text()
                            sheet.write(nrows, ncols, tddiv2)
                            nrows += 1
                            num1 += 1
                    flag += 1
                    continue
            else:
                flag2 = True
                # 第二个及之后TABLE
                for tr2 in table.find_all("tr"):
                    nrows = rows+1
                    if flag2:
                        # 标题
                        h3 = tr2.find("h3")
                        h3span = h3.find("span").get_text()
                        # print(h3span)
                        flag2 = False
                        continue
                    else:
                        num1 = 0
                        th = tr2.find("th")
                        try:
                            #  按图片找参数
                            small_title_href = th.find("a").get("href")
                            small_title = small_title_href[40:-22]
                            small_title = dictionary.dic[small_title]
                            if small_title in titleList:
                                ncols = titleList[small_title]
                            else:
                                titleList[small_title] = len(titleList)
                                ncols = titleList[small_title]
                                sheet.write(0, ncols, small_title)
                                cols += 1
                            if small_title == "厂商":
                                car_value = cartype
                                for td22 in tr2.find_all("td"):
                                    if num1 < num:
                                        sheet.write(nrows, ncols, car_value)
                                        nrows += 1
                                        num1 += 1
                            elif small_title == "级别":
                                car_value = val1
                                for td33 in tr2.find_all("td"):
                                    if num1 < num:
                                        sheet.write(nrows, ncols, car_value)
                                        nrows += 1
                                        num1 += 1
                            else:
                                for td2 in tr2.find_all("td"):
                                    if num1 < num:
                                        td2div = td2.find("div").get_text()
                                        car_value = td2div
                                        sheet.write(nrows, ncols, car_value)
                                        nrows += 1
                                        num1 += 1
                        except:
                            # 文字找参数
                            nrows = rows+1
                            try:
                                small_title = th.find("span").get_text()
                                if small_title in titleList:
                                    ncols = titleList[small_title]
                                else:
                                    titleList[small_title] = len(titleList)
                                    ncols = titleList[small_title]
                                    sheet.write(0, ncols, small_title)
                                    cols += 1
                                for trtd in tr2.find_all("td"):
                                    if num1 < num:
                                        trtddiv = trtd.find("div").get_text()
                                        sheet.write(nrows, ncols, trtddiv)
                                        nrows += 1
                                        num1 += 1
                            except:
                                pass
                flag += 1
                continue
    except:
        return rows
    f = open("text/titleList.txt", "w", encoding="utf-8")
    f.write(str(titleList))
    f.close()
    return rows + num + 1
    #return str(rows + num + 1)+":"+str(cols)
