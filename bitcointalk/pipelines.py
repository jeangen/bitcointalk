# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sys
sys.path.append('..')
from client import Client
from table_creator import Creator
import datetime

class BitcointalkPipeline(object):
    def __init__(self):
        self.database_name = 'heimdall'
        self.crawler_name = 'bitcointalk_realtime'
        self.client = Client()
        self.client.start_client()
        
    def open_spider(self,spider):
        self.client.database_name = self.database_name
        self.client.crawler_name = self.crawler_name
        with Creator() as creator:
            creator.try_create_database(self.crawler_name,subject= str, replies = int,views= int,last_post= 'timestamp',topic_url= str, topic_id= float)

    def process_item(self, item, spider):
        try:
            message = {
                'database':self.database_name,
                'table':self.crawler_name,
                'data':
                {
                    'datetime': str(datetime.datetime.utcnow()),
                    'subject':item['subject'][0],
                    'replies':item['replies'][0],
                    'views':item['views'][0],
                    'last_post':str(item['last_post'][0]),
                    'topic_url':item['topic_url'][0],
                    'topic_id':item['topic_id'][0]
                },
            }
            self.client.send(message)
            print(message)
            return item

        except Exception as e:
            self.client.exception(e)

        
