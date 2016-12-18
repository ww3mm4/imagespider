# -*- coding: utf-8 -*-
import scrapy
from imagespider.settings import ALLOWED_DOMAINS,START_URL,BASE_URL
from imagespider.items import ImagespiderItem
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader


class ImgspiderSpider(scrapy.Spider):
    name = "imgspider"
    allowed_domains = [ALLOWED_DOMAINS]
    start_urls = [START_URL]

    def parse(self, response):
        sel = Selector(response)
        for link in sel.xpath("//*[@id='showImg']/li/a/@href").extract():
            request = scrapy.Request(BASE_URL+link,callback=self.parse)
            yield request

        for link in sel.xpath("//*[@id='1920x1080']/@href").extract():
            request = scrapy.Request(BASE_URL+link,callback=self.parse_item)
            yield request

    def parse_item(self,response):
        l = ItemLoader(item=ImagespiderItem(), response=response)
        l.add_xpath("img_url","/html/body/img[1]/@src")
        return l.load_item()
