#!/usr/bin/env python
# -*- coding : utf-8 -*-

#__author__ = 'DevinChang'
#__data__ = '2017/10/11'

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from lxml import etree
import lxml.etree
import re
import xlsxwriter
import requests
import io
import sys
from ipdb import set_trace
import xlsxwriter
#import requests

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') 

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

#create a excle
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', '品牌名称')
worksheet.write('B1', '地址')
worksheet.write('C1', '种类')
worksheet.write('D1', '地区')

def search():
    try:
        browser.get("http://sh.meituan.com/")
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div > header > div.header-content.clearfix > div.header-search-module > div.header-search-block > input'))
            )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#app > div > header > div.header-content.clearfix > div.header-search-module > div.header-search-block > button')))
        input.send_keys('有家酸菜鱼')
        submit.click()
        getinfo()
    except TimeoutException:
        search()

def get_links():
    pagesource = browser.page_source
                                          #/html/body/div/div/div/div[2] 
                                          #//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/a
    #links = browser.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]/div[2]/div//a/@href')
    #links = browser.find_element(By.CLASS_NAME, 'default-list-item clearfix')
    #link = browser.find_element_by_class_name('default-list-item clearfix')
    tree = etree.HTML(pagesource)
    links = tree.xpath("/html/body/div/div/div/div[2]/div/div[2]/div[2]/div/div/div[@class='default-list-item clearfix']/a/@href")
    return links

def parse(url):
     browser.get(url)


def getinfo2(url):
    browser.get(url)
    tree = etree.HTML(browser.page_source)
    title = tree.xpath('//*[@id="bd"]/div[2]/div[1]/h2/span.text()')
    city = tree.xpath('//*[@id="J-site-mast__branding"]/div[1]/h2/a.text()')
    address = tree.xpath('//*[@id="bd"]/div[2]/div[1]/p[1]/span[1].text()')
def getinfo(): 
    page_source = browser.page_source 
    #tree = etree.HTML(browser.page_source) 
    tree = etree.HTML(page_source) 
    items = tree.xpath('//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div[2]/div') 
    i = 1 
    for item in items: 
        title = tree.xpath('//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div[2]/div[{}]/div/div/div/div[1]/a/text()'.format(i)) 
        address = tree.xpath('//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div[2]/div[{}]/div/div/div/div[1]/div[2]/div[1]/span[2]/text()'.format(i)) 
        variety = tree.xpath('//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div[2]/div[{}]/div/div/div/div[1]/div[2]/div[1]/span[1]/span[1]/text()'.format(i)) 
        city = tree.xpath('//*[@id="app"]/div/header/div[1]/div/div/span[2]/text()')
        avgprice = tree.xpath('//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div[2]/div[{}]/div/div/div/div[1]/div[3]/div/span/text()'.format(i))
        score = tree.xpath('//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div[2]/div[{}]/div/div/div/div[1]/div[1]/span[2]/text()'.format(i)) 
        #set_trace()
        #print(''.join(score))
        print(avgprice) 
        print(score)
        product = [title, address, variety, city, avgprice[1:], score] 
        save_to_excel(product) 
        i += 1 

row = 0 
def global_row(): 
    global row 
    row += 1 
    return row 
def save_to_excel(items): 
    col = 0 
    g_row = global_row() 
    for item in items: 
        if item: 
             worksheet.write(g_row, col, item[0])
        else:
             worksheet.write(g_row, col, '暂无价格')
        col += 1


def main():
    search()
    links = get_links()
    for link in links:
        parse('http:' + link)
    workbook.close()
    
if __name__ == '__main__':
     main()



