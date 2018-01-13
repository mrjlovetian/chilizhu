import ssl
from selenium import webdriver
import urllib.request
import os
import os
import time
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context
url = ''

# http://www.cilizhu2.com/remen/index_101.html


# 获取URL每张图对应的详情
def getMainUrl(mainUrl):
    global index
    dirver = webdriver.PhantomJS('phantomjs')
    dirver.get(mainUrl)
    time.sleep(1.3)
    bsObj = BeautifulSoup(dirver.page_source, 'lxml')
    zhongZiUrls = []


    for mainUrlData in bsObj.find_all('a', class_='movie-box'):
        imUrl = 'http://www.cilizhu2.com' + mainUrlData['href']
        print('******', imUrl)
        zhongZiUrls.append(imUrl)

    for zhongziUrl in zhongZiUrls:
        getZhongzi(zhongziUrl)


# 打开详情查看是否有种子相关信息
def getZhongzi(zhongZiurl):
    
    zhongziDriver = webdriver.PhantomJS()
    zhongziDriver.get(zhongZiurl)
    time.sleep(0.5)
    zhongZiObj = BeautifulSoup(zhongziDriver.page_source, 'lxml')
    realZhongZiUrl = zhongZiObj.find('a', class_='btn btn-lg btn-primary')
    print('real zhongziUrl', realZhongZiUrl['href'])
    torrentUrl = 'http://www.cilizhu2.com' + realZhongZiUrl['href']
    gettorrent(torrentUrl)

# 打开种子页面
def gettorrent(torrentUrl):
    torrentDriver = webdriver.PhantomJS()
    torrentDriver.get(torrentUrl)
    time.sleep(0.5)
    torrentObj = BeautifulSoup(torrentDriver.page_source, 'lxml')
    
    torroentDiv = torrentObj.find('div', class_='btsowlist')
    if len(torroentDiv) > 0:
        torroentA = torroentDiv.find('div', class_='row')
        # print('torroentA', torroentA)
        if len(torroentA) > 0:
            torroent = torroentA.find('a')['href']
            print('find url ', torroent)
            finalTorroent(torroent)
        
# 招到最终可以下载的种子
def finalTorroent(findUrl):
    finalDriver =  webdriver.PhantomJS()
    finalDriver.get(findUrl)
    time.sleep(0.5)
    finalObj = BeautifulSoup(finalDriver.page_source, 'lxml')
    textEra = finalObj.find('textarea', class_='magnet-link')
    print('种子是', textEra.text)

# 遍历所有的URL
for i in range(101, 160):
    mainUrl = 'http://www.cilizhu2.com/remen/index_%s.html'%(i)
    print(mainUrl)
    getMainUrl(mainUrl)

