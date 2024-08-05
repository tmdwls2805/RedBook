# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RedbookItem(scrapy.Item):
    # 쇼핑몰 이름
    book_site = scrapy.Field()
    book_isbn = scrapy.Field()
    # 책 제목
    book_title = scrapy.Field()
    # 책 카테고리
    book_cat = scrapy.Field()
    # 책 가격
    book_price = scrapy.Field()
    # 책 작가
    book_author = scrapy.Field()
    # 책 출판사
    book_publish = scrapy.Field()
    # 책 출판일
    book_publish_date = scrapy.Field()
    # 책 이미지
    book_img = scrapy.Field()
    # 책 쇼핑몰 상세보기 주소
    book_url = scrapy.Field()
    pass
