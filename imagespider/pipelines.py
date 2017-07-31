# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline, Image
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from wheel import metadata

from imagespider import dao
from imagespider.dao import Base

try:
    from cStringIO import StringIO as BytesIO, StringIO
except ImportError:
    from io import BytesIO

class ImagespiderPipeline(ImagesPipeline):

    def image_custom_key(self, response):
        name = response.meta['title']
        image_guid = response.url.split('/')[-1]
        img_key = name+'/%s' % (image_guid)
        return img_key

    def get_images(self, response, request, info):
        for key, image, buf, in super(ImagespiderPipeline, self).get_images(response, request, info):
            key = self.image_custom_key(response)
            yield key, image, buf



    def get_media_requests(self, item, info):
        for image_url in item['img_url']:
            yield scrapy.Request(image_url,meta={'title':item['title']})


    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['img_url'] = image_paths
        return item

class SqlPipeline(object):
    collection_name = 'scrapy_items'

    def open_spider(self, spider):
        # 初始化数据库连接:
        engine = create_engine('mysql+mysqldb://root:root@localhost/image', echo=True)

        #创建表
        Base.metadata.create_all(engine)

        # 创建DBSession类型:
        self.DBSession = sessionmaker(bind=engine)
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        for image_url in item['img_url']:
            new_image = dao.Image(img_url=image_url, title=item['title'])
            session = self.DBSession()
            session.add(new_image)
            session.commit()
            session.close()
        return item