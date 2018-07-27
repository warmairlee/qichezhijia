import dictionary
from xlrd import open_workbook
from xlutils.copy import copy
from bs4 import BeautifulSoup
import urllib.request
if __name__ == "__main__":
    '''
    f = open("text/test.txt", "w", encoding="utf-8")
    dic = dictionary.dic
    f.write(str(dic))
    f.close()
    
    f = open("text/test.txt", "r", encoding="utf-8")
    dic = f.read()
    dict_name = eval(dic)
    f.close()


    rexcel = open_workbook(r"text/test.xls")
    rows = rexcel.sheets()[0].nrows
    cols = rexcel.sheets()[0].ncols
    print(str(rows)+":"+str(cols))
    excel = copy(rexcel)
    table = excel.get_sheet(0)
    table.write(0, 1, "hello")
    excel.save(r"text/test.xls")print(dict_name["40_41_194"])
    '''
    url = "https://car.autohome.com.cn/config/series/3170.html"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    if soup.find("div", class_="pzbox"):
        print(soup.find("div", class_="pzbox"))
        print("1")
    else:
        print("2")