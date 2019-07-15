# 封装爬虫类

```
封装1：

from urllib.error import HTTPError,URLError 
from lxml import etree 
import urllib.request
import urllib.parse
import threading
import chardet
import random
import json
import time
import os 
import re 

# 请求
def requestWithUrl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    time.sleep(random.randrange(1, 3))
    request = urllib.request.Request(url=url, headers=headers)
    try:
    	response = urllib.request.urlopen(request)
    except HTTPError as e:
    	return e
    except URLError as e:
    	return e
    except Exception as e:
    	return e
    else:
    	encoding = chardet.detect(response.read())['encoding']
        if encoding is 'GB2312' or 'GB18030':
            encoding = 'gbk'
        htmlString = response.read().decode(encoding)
        return htmlString

# 解析
def parseHomepage(htmlString):
	nodeXpath = '//div[@class="listmain"]//dd/a'
	tree = etree.HTML(htmlString)
	nodeList = tree.xpath(nodeXpath)
	contents = []
	for node in nodeList:
		text = node.xpath('./text()')[0]
		href = node.xpath('./@href')[0]
		contents.append({
			"name": text,
			"href": href
			})
		return contents
		
# 不涉及二级页面时：
# 写入文件必须以字符串的形式，但是直接强制转换会破坏原始数据的结构，所以采用json	模块进行字符串转换
# jsonString = json.dumps(contents)
# with open("titles.txt", "w", encoding="utf-8") as fp:
#	 fp.write(jsonString)
# with open("titles.txt", "r", encoding="utf-8") as fp:
#	 contentsString = fp.read()
#	 因为写入的时候是以json格式的字符串写入的，所以需要转换成json对象在使用
#	 jsonObj = json.loads(contentsString)
#	 for titleDic in jsonObj:
#	 	print(titleDic)
    
# 接收一级页面链接解析二级页面
def parseDetailPage(htmlString):
    tree = etree.HTML(htmlString)
    contentPath = '//div[@id="content"]/text()'
    lines = tree.xpath(contentPath)
    content = ""
    for line in lines:
        content += line.strip() + '\n'
    return content
    
# 保存
def saveData(filePath, fileName , content):
	if not os.path.exists(filePath):
		os.mkdir(filePath)
    path = os.path.join(filePath, fileName)
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(content)
 
# 下载
def downloadImage(src, alt, pathName):
    if not os.path.exists(pathName):
        os.mkdir(pathName)
    filePath = os.path.join(pathName, alt)
    urllib.request.urlretrieve(src, filePath)
    print(alt,"下载完成..")

# 封装耗时操作
def Logic(detailUrl, fileName):
    detailHtmlString = requestWithUrl(detailUrl)
    content = parseDetailPage(HdetailHtmlString)
    saveData("novel", fileName, content)
  
url = "https://www.biqiuge.com/book/4772"

homePageString = requestWithUrl(url)

novelList = parseHomepage(homePageString)

for novelDic in novelList[6:11]:
    fileName = novelDic["name"] + '.txt'
    href = novelDic["href"]
    baseUrl = "https://www.biqiuge.com"
    detailUrl = baseUrl + href
    # 线程
    thread = threading.Thread(target=Logic, args=(detailUrl, fileName))
    thread.start()
```



```
封装2：
from urllib.error import HTTPError,URLError 
from lxml import etree 
import urllib.request
import urllib.parse
import threading
import chardet
import random
import json
import time
import os 
import re 

# 响应结果为htmlString：
# 请求解析
def reqeustLogic(response):
    htmlString = response.read().decode('utf-8')
    tree = etree.HTML(htmlString)
    titleList = tree.xpath('//header/h2/a/@title')
    contents = []
    for title in titleList:
        dic = {
            "title": title,
        }
        contents.append(dic)
    return contents
    
allData = []
page = 1
while True:
    url = "https://cuiqingcai.com/category/technique/python/page/{}".format(page)
    page += 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    time.sleep(random.randrange(1, 3))
    request = urllib.request.Request(url=url, headers=headers)
    try：
        response = urllib.request.urlopen(request)
    except Exception as e:
        print(e)
        break
    else:
        print(response.geturl())
        pageDataList = reqeustLogic(response)
        allData += pageDataList
        
jsonString = json.dumps(allData)
with open("allTitles.txt", "w", encoding="utf-8") as fp:
    fp.write(jsonString)
    
# 响应结果为jsonString：
filmList = []
page = 1
while True:
    url = "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start={}".format(
        (page - 1) * 20)
    page += 1
    response = urllib.request.urlopen(url)
    jsonString = response.read().decode('utf-8')
    jsonObj = json.loads(jsonString)
    subjects = jsonObj['subjects']
    if len(subjects) == 0:
        break
    for subject in subjects:
        filmList.append({
            "rate": subject['rate'],
            "title": subject['title'],
            "url": subject['url']
        })

jsonString = json.dumps(filmList)
with open("film.txt", "w", encoding="utf-8") as fp:
    fp.write(jsonString)
```

