# -*- coding: utf-8 -*-

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
import os
from hashlib import md5


#driver = webdriver.Chrome()
'''
@arg:
service_args 默认参数是none，为了节省流量与时间，可以设之PhantomJS不加载图片
'''
driver = webdriver.PhantomJS(service_args=['--load-images=false', '--disk-cache=true'])

web = WebDriverWait(driver, 10)
driver.set_window_size(1400, 900)



#创建一个excel表格
workbook = xlsxwriter.Workbook('Expenses01.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', '名称')
worksheet.write('B1', '图片')
worksheet.write('C1', '价格')
worksheet.write('D1', '商店')
worksheet.write('E1', '所在地')
row = 0

myimage = []

def save_to_excel(product):
    col = 0
    graw = globalraw()
    for item in product:
        worksheet.write(graw, col, item[0])
        col += 1


def globalraw():
    global row
    row += 1
    return row


def search():
    try:
        print('正在搜索...')
            
        input = web.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = web.until(element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys('美食')
        submit.click()
        getproduct()
        total_page = web.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        return total_page.text
    except TimeoutException:
        return search()

def getproduct():
    web.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    #tree = html.fromstring(driver.page_source)
    #el = driver.find_element_by_xpath(ixpath)
    #tree = etree.parse(page)
    #tree = html.fromstring(driver.page_source)
    #print(type(tree))
    #tree = etree.parse(driver.page_source)
    tree = etree.HTML(driver.page_source)
    #print(tree)
    el = tree.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
    #print(el)
    i = 1        
    for item in el:
        image_xpath = '//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[{}]/div[1]/div/div[1]//img/@data-src'.format(i)
        title_xpath = '//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[{}]/div[1]/div/div[1]//img/@alt'.format(i)
        price_xpath = '//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[{}]/div[2]/div[1]/div[1]/strong/text()'.format(i)
        location_xpath = '//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[{}]/div[2]/div[3]/div[2]/text()'.format(i)
        shop_xpath = '//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[{}]/div[2]/div[3]/div[1]/a/span[2]/text()'.format(i)
        i += 1
        
        '''
        product = {
            'title' : tree.xpath(title_xpath),
            'image' : tree.xpath(image_xpath),
            'price' : tree.xpath(price_xpath),
            'shop' : tree.xpath(shop_xpath),
            'location' : tree.xpath(location_xpath)
        }
        '''

        product2 = [tree.xpath(title_xpath),
            tree.xpath(image_xpath),
            tree.xpath(price_xpath),
            tree.xpath(shop_xpath),
            tree.xpath(location_xpath)]
        
        #print(product)
        #print(product['image'])
        #print(product['image'][0])
        #print(product2[0])
        myimage.append(product2[1][0])
        #save_to_excel(product2)


def next_page(page_number):
    try:
        print('正在翻页 %d' % page_number)
        input = web.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        submit = web.until(element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        web.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > ul > li.item.active > span"), str(page_number))
        )
        getproduct()
    except TimeoutException:
        next_page(page_number)


def download_image(url):
    print('Downloading image...')
    try:
        iurl = '{0}:{1}'.format('http', url)
        response = requests.get(iurl)
        if response.status_code == 200:
            save_image(response.content)
        #save_image(url)
        return None
    except ConnectionError:
        return None


def save_image(content):
    if not os.path.exists('{0}/{1}'.format(os.getcwd(), 'img')):
        os.mkdir('{0}/{1}'.format(os.getcwd(), 'img'))
    file_path = '{0}/{1}/{2}.{3}'.format(os.getcwd(), 'img', md5(content).hexdigest(), 'jpg')
    print(file_path)
    if not os.path.exists(file_path):
        with open (file_path, 'wb') as f:
            f.write(content)
            f.close()

def main():
    page = search()
    page = int(re.compile(r'(\d+)').search(page).group(1)) 
    for i in range (2, 5):
        next_page(i)

    for img in myimage:
        download_image(img)


if __name__ == '__main__':
    main()
    workbook.close()













