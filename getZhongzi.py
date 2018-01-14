# -*- coding: UTF-8 -*-

import ssl
from selenium import webdriver
import urllib.request
import os
import os
import time
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context
url = ""

totalCount = 0
currCount = 0
# http://www.cilizhu2.com/remen/index_101.html


# 获取URL每张图对应的详情
def getMainUrl(mainUrl):
    global index
    global totalCount
    global currCount
    dirver = webdriver.PhantomJS('phantomjs')
    dirver.get(mainUrl)
    time.sleep(0.3)
    bsObj = BeautifulSoup(dirver.page_source, 'lxml')
    zhongZiUrls = []


    for mainUrlData in bsObj.find_all('a', class_='movie-box'):
        imUrl = 'http://www.cilizhu2.com' + mainUrlData['href']
        print('******', imUrl)
        zhongZiUrls.append(imUrl)

    for zhongziUrl in zhongZiUrls:
        getZhongzi(zhongziUrl)
    
    totalCount = len(zhongZiUrls)


# 打开详情查看是否有种子相关信息
def getZhongzi(zhongZiurl):
    
    zhongziDriver = webdriver.PhantomJS()
    zhongziDriver.get(zhongZiurl)
    time.sleep(0.1)
    zhongZiObj = BeautifulSoup(zhongziDriver.page_source, 'lxml')
    realZhongZiUrl = zhongZiObj.find_all('a', class_='btn btn-lg btn-primary')
    if len(realZhongZiUrl) > 0:
        # if realZhongZiUrl[0].find('key'):
        #     print('real zhongziUrl', realZhongZiUrl['href'])
        #     torrentUrl = 'http://www.cilizhu2.com' + realZhongZiUrl['href']
        #     gettorrent(torrentUrl)
        
        item = realZhongZiUrl[0]
        if item.has_attr('href'):
            print('real zhongziUrl', item['href'])
            torrentUrl = 'http://www.cilizhu2.com' + item['href']
            gettorrent(torrentUrl)
        
    

# 打开种子页面
def gettorrent(torrentUrl):
    torrentDriver = webdriver.PhantomJS()
    torrentDriver.get(torrentUrl)
    time.sleep(0.1)
    torrentObj = BeautifulSoup(torrentDriver.page_source, 'lxml')
    
    torroentDiv = torrentObj.find_all('div', class_='btsowlist')
    if len(torroentDiv) > 0:
        torroentA = torroentDiv[0].find('div', class_='row')
        # print('torroentA', torroentA)
        if len(torroentA) > 0:
            torroent = torroentA.find('a')['href']
            print('find url ', torroent)
            finalTorroent(torroent)
        
# 招到最终可以下载的种子
def finalTorroent(findUrl):
    finalDriver =  webdriver.PhantomJS()
    finalDriver.get(findUrl)
    time.sleep(0.1)
    finalObj = BeautifulSoup(finalDriver.page_source, 'lxml')
    textEra = finalObj.find('textarea', class_='magnet-link')
    print('种子是', textEra.text)
    global url
    url = url + textEra.text + "\n"
    currCount += 1
    print('种子磁力链接%s, 当前数量是%s, 总的磁力数量是%s' %(url, currCount, totalCount))
    # writeTorroent(textEra.text)
    
    
def writeTorroent(torroent):
    fo = open('torroent.js', 'a+')
    fo.write(torroent+'\n')
    fo.close()

index = 102
# 遍历所有的URL
for i in range(index, index+1):
    mainUrl = 'http://www.cilizhu2.com/remen/index_%s.html'%(i)
    print(mainUrl)
    getMainUrl(mainUrl)

writeTorroent(url)
print("done!!!!")

# writeTorroent('我是想红菊1')
# writeTorroent('我是想红菊2')
# writeTorroent('我是想红菊3')
# writeTorroent('我是想红菊4')


# def addUrl(str):
#     global url
#     url = url + str + "\n"
#     print("now", url)
#     # url.append(str+"\n")
#
# addUrl("123a")
# addUrl("123b")
# addUrl("123c")
# addUrl("123d")
#
# print('url', url)

