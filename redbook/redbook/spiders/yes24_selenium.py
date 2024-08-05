# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

class Yes24CrawlSpider(CrawlSpider):
    name = 'yes24_selenium'
    allowed_domains = ['yes24.com']
    start_urls = [
                'http://www.yes24.com/24/Category/Display/001001046001?ParamSortTp=01',
            ]

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.Chrome('C:/chromedriver')
        # self.driver = webdriver.PhantomJS("C:/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs")

    def __del__(self):
        self.driver.close()

    def parse(self, response):
        pageNum = 3
        self.driver.get(response.url)
        time.sleep(1)
        for i in range(5):
            n = 1
            for j in range(20):
                try:
                    xpath = '//*[@id="category_layout"]/ul/li[%d]/div/div[1]/div[2]/a[1]' % n
                    elem = self.driver.find_element_by_xpath(xpath).click()
                except NoSuchElementException:
                    xpath = '//*[@id="category_layout"]/ul/li[%d]/div/div[1]/div[1]/a[1]' % n
                    elem = self.driver.find_element_by_xpath(xpath).click()
                n += 1
                time.sleep(3)
                html = self.driver.find_element_by_xpath('//*').get_attribute('outerHTML')
                selector = Selector(text=html)
                item = {}
                item['book_site'] = 'yes24'
                item['book_isbn'] = selector.xpath('//*[@id="infoset_specific"]/div[2]/div/table/tbody/tr[3]/td/text()')[0].extract()
                item["book_cat"] = selector.xpath('//*[@id="yLocation"]/div/div[3]/a/text()')[0].extract().strip()
                item["book_title"] = selector.xpath('//*[@id="yDetailTopWrap"]/div[2]/div[1]/div/h2/text()')[0].extract().strip()
                item["book_price"] = selector.xpath('//*[@id="yDetailTopWrap"]/div[2]/div[2]/div[1]/div[1]/table/tbody/tr[2]/td/span/em/text()')[0].extract()
                item["book_author"] = selector.xpath('//*[@id="yDetailTopWrap"]/div[2]/div[1]/span[2]/span[1]/a/text()')[0].extract().strip()
                item["book_publish"] = selector.xpath('//*[@id="yDetailTopWrap"]/div[2]/div[1]/span[2]/span[2]/a/text()')[0].extract()
                item["book_publish_date"] = selector.xpath('//*[@id="yDetailTopWrap"]/div[2]/div[1]/span[2]/span[3]/text()')[0].extract()
                item["book_img"] = selector.xpath('//*[@id="yDetailTopWrap"]/div[1]/div[1]/span/em/img/@src')[0].extract()
                item["book_url"] = self.driver.current_url
                item['book_img'] = item['book_img'] + ".jpg"
                item["crawl_time"] = datetime.now()
                yield item
                self.driver.execute_script('window.history.go(-1)')
            page = '//*[@id="cateSubWrap"]/div[2]/div[3]/div[2]/span[1]/div/a[%d]' % pageNum
            pageNum += 1
            elem = self.driver.find_element_by_xpath(page).click()