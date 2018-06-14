# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Repository, engine
from shiyanlou.items import RepositoryItem

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = datetime.strptime(item['update_time'], '%Y-%m-%dT%H:%M:%SZ' ) + timedelta(hours=8)
        self.session.add(Repository(**item))
        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    
    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

