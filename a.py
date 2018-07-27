import urllib.request
from bs4 import BeautifulSoup
import sys


url = []
url.append("https://car.autohome.com.cn/shuyu/list_1_0_76.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_150.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_8.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_3.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_13.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_16.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_11.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_18.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_32.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_38.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_25.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_60.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_27.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_29.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_36.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_57.html")
url.append("https://car.autohome.com.cn/shuyu/list_1_0_40.html")

output = sys.stdout
fo = open("text/info.txt", 'a', encoding='utf-8')
sys.stdout = fo

for i in range(0, 17):
    request = urllib.request.Request(url[i])
    response = urllib.request.urlopen(request)
    data = response.read().decode("gb2312", "ignore")
    soup = BeautifulSoup(data, "lxml")
    div = soup.find("div", class_="frame_tree")
    ul = div.find("ul")
    li = ul.find_all("li")[i]
    h3 = li.find("h3")
    h3a = h3.find("a").get_text()
    print("# " + h3a)
    list = li.find("div", class_="listtree")
    try:
        dl = list.find("dl")
        for dd in dl.find_all("dd"):
            a1 = dd.find("a").get("href")
            a2 = dd.find("a").get_text()
            print("\"" + a1[14:-5] + "\"" + ": " + "\"" + a2 + "\",")
    except: pass

fo.flush()
sys.stdout = output
fo.close()

