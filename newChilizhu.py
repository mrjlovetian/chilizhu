from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request
import os
import time
from bs4 import BeautifulSoup

allTorrents = ''
totalCount = 0
currCount = 0

# 获取URL每张图对应的详情
def getMainUrl(mainUrl):
    global index
    global totalCount
    browser.get(mainUrl)
    time.sleep(0.3)
    bsObj = BeautifulSoup(browser.page_source, 'lxml')
    zhongZiUrls = []

    for mainUrlData in bsObj.find_all('a', class_='movie-box'):
        imUrl = 'http://www.cilizhu2.com' + mainUrlData['href']
        zhongZiUrls.append(imUrl)

    totalCount += len(zhongZiUrls)
    for zhongziUrl in zhongZiUrls:
        getZhongzi(zhongziUrl)

# 打开详情查看是否有种子相关信息
def getZhongzi(zhongZiurl):
    browser.get(zhongZiurl)
    time.sleep(0.1)
    zhongZiObj = BeautifulSoup(browser.page_source, 'lxml')
    realZhongZiUrl = zhongZiObj.find_all('a', class_='btn btn-lg btn-primary')
    if len(realZhongZiUrl) > 0:
        item = realZhongZiUrl[0]
        if item.has_attr('href'):
            print('real zhongziUrl', item['href'])
            torrentUrl = 'http://www.cilizhu2.com' + item['href']
            gettorrent(torrentUrl)

# 打开种子页面
def gettorrent(torrentUrl):
    browser.get(torrentUrl)
    time.sleep(0.1)
    torrentObj = BeautifulSoup(browser.page_source, 'lxml')
    torroentDiv = torrentObj.find_all('div', class_='btsowlist')
    if len(torroentDiv) > 0:
        torroentA = torroentDiv[0].find('div', class_='row')
        if not torroentA is None:
            torroent = torroentA.find('a')['href']
            print('find url ', torroent)
            finalTorroent(torroent)

# 招到最终可以下载的种子
def finalTorroent(findUrl):
    browser.get(findUrl)
    time.sleep(0.5)
    finalObj = BeautifulSoup(browser.page_source, 'lxml')
    textEra = finalObj.find('textarea', class_='magnet-link')
    print ('************************', textEra)
    if not textEra is None:
        global allTorrents
        global currCount
        allTorrents = allTorrents + textEra.text + "\n"
        currCount += 1
        print(' 当前数量是%s, 总的磁力数量是%s' % (currCount, totalCount))
        print ('当前收集到种子为', allTorrents)

# 保存文件
def writeTorroent(torroent, name):
    print ('name', str(name))
    fileName = str(name) + 'torroent.js'
    fo = open(fileName, 'a+')
    fo.write(torroent + '\n')
    fo.close()

# 创建全局浏览驱动
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)

index = int(input("请输入页码:"))
pageCount = int(input("请输入翻页跨度:"))

# 遍历所有的URL
for i in range(index, index + pageCount):
    mainUrl = 'http://www.cilizhu2.com/remen/index_%s.html' % (i)
    print(mainUrl)
    getMainUrl(mainUrl)


writeTorroent(allTorrents, index)
print("done!!!!")
browser.close()

