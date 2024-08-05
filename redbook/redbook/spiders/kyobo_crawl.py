# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime
from selenium import webdriver
import time

class KyoboCrawlSpider(CrawlSpider):
    name = 'kyobo_crawl'
    allowed_domains = ['kyobobook.co.kr']
    start_urls = [
            'http://www.kyobobook.co.kr/categoryRenewal/categoryMain.laf?pageNumber=1&perPage=50&mallGb=KOR&linkClass=0101&ejkGb=&sortColumn=near_date',
        ]

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.Chrome('C:/chromedriver')
        #self.driver = webdriver.PhantomJS("C:/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs")
    def __del__(self):
        self.driver.close()

    def parse(self, response):
        pageNum = 2
        self.driver.get(response.url)
        time.sleep(1)
        for i in range(2):
            n = 1
            for j in range(50):
                xpath = '//*[@id="prd_list_type1"]/li[%d]/div/div[1]/div[2]/div[1]/a'%n
                n += 2
                elem = self.driver.find_element_by_xpath(xpath).click()
                time.sleep(2.5)
                html = self.driver.find_element_by_xpath('//*').get_attribute('outerHTML')
                selector = Selector(text=html)
                item = {}
                item["book_site"] = "교보문고"
                item['book_isbn'] = selector.xpath('//*[@class="table_simple2 table_opened margin_top10"]/tbody/tr[1]/td/span[1]/text()')[0].extract()
                item["book_cat"] = selector.xpath('//*[@id="container"]/div[1]/div[4]/p/span/a/text()')[0].extract()
                item["book_title"] = selector.xpath('//*[@id="container"]/div[2]/form/div[1]/h1/strong/text()')[0].extract().strip()
                item["book_price"] = selector.xpath('//*[@id="container"]/div[2]/form/div[3]/div[1]/ul/li[1]/span[2]/strong/text()')[0].extract()
                author = selector.xpath('//*[@class="author"]/span[1]/a/text()')[0].extract().strip()
                item["book_author"] = author.replace('\n','').replace('\t','')
                item["book_publish"] = selector.xpath('//*[@title="출판사"]/a/text()')[0].extract()
                publish_date = selector.xpath('//*[@title="출간일"]/text()')[0].extract().strip()
                item["book_publish_date"] = publish_date[:13]
                try:
                    item["book_img"] = selector.xpath('//*[@id="container"]/div[2]/form/div[2]/div[1]/div/a/img/@src')[0].extract()
                except IndexError:
                    item["book_img"] = selector.xpath('//*[@id="container"]/div[2]/form/div[2]/div[1]/div/img/@src')[0].extract()
                item["book_url"] = self.driver.current_url
                item["crawl_time"] = datetime.now()
                yield item
                self.driver.execute_script('window.history.go(-1)')
            page = '//*[@id="eventPaging"]/div/ul/li[%d]/a'%pageNum
            pageNum+=1
            elem = self.driver.find_element_by_xpath(page).click()