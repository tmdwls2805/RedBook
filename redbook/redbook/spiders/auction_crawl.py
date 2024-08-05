# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import datetime


class AuctionCrawlSpider(CrawlSpider):
    name = 'auction_crawl'
    allow_domains = ['auction.co.kr']

    start_urls = [
    'http://browse.auction.co.kr/list?category=36060105&s=8&t=a'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'http://itempage3.auction.co.kr/DetailView.aspx\?itemno=.*'),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'http://browse.auction.co.kr/list\?category=.*.+&s=8+&t=a+&k=0+&p=\d'),
             callback='parse_url', follow=True)
    )


    def parse_url(self, response):
        url = {}
        return url

    def parse_item(self, response):
        item = {}
        item['book_site'] = '옥션'
        item['book_isbn'] = response.xpath('//*[@id="wrapDetail"]/div[2]/div[2]/div[5]/div[3]/span[1]/text()').extract()
        item['book_cat'] = '한국소설'
        item['book_title'] = response.xpath('//*[@id="frmMain"]/h1/span/text()').extract()
        item['book_price'] = response.xpath('//*[@class="price_real"]/text()').extract()
        item['book_author'] = response.xpath('//*[@id="ucBookItemInfo_htrAuthor"]/p[2]/text()').extract()
        item['book_publish'] = response.xpath('//*[@id="ucBookItemInfo_htrPublisher"]/p[2]/text()').extract()
        item['book_publish_date'] = response.xpath('//*[@id="frmMain"]/ul/li[5]/div/div/ul/li[4]/p[2]/text()').extract()
        item['book_img'] = response.xpath('///*[@id="content"]/div[2]/div[1]/div/div/ul/li[1]/a/img/@src').extract()
        item['book_url'] = response.request.url
        item["crawl_time"] = datetime.now()
        return item
