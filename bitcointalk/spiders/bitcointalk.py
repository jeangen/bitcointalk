import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from ..items import BitcointalkItem
import time
import datetime

class BitcointalkSpider(scrapy.Spider):
    name='bitcointalk'
    allowed_domains = ['bitcointalk.org']
    start_urls = ['https://bitcointalk.org']

    def parse_last_posts(self, posts):
        parsed_posts=[]
        for post in posts:
            post = post.replace("at","").replace("by","")
            parsed_posts.append(post)
        return parsed_posts

    def format_last_post(self,posts):
        formatted_posts = []
        for post in posts:
            if post[0].isalpha() == True:
                formatted_posts.append(datetime.datetime.strptime(post, "%B %d, %Y, %I:%M:%S %p"))
            elif post[0].isdigit() == True:
                formatted_posts.append(datetime.datetime.strptime(post, "%I:%M:%S %p"))
        return formatted_posts
    
    def get_topic_id(self, topic_ids):
        id_array = []
        for tid in topic_ids:
            id_array.append(tid[tid.find('=')+1:])
        return id_array

    def parse(self, response):
        links = response.css('.windowbg2 a::attr(href)').getall()
        for link in links:
            if 'board' in link:
                yield response.follow(link, self.get_board_items)

    def get_board_items(self, response):
        subjects = response.css('.windowbg3 span a::text').getall() + response.css('.windowbg span a::text').getall()
        replies_views = response.css('td.windowbg3::text').getall() + response.css('td.windowbg::text').getall()
        last_posts = response.css('td.windowbg2.lastpostcol > span.smalltext::text').getall()
        topic_url = response.css('.windowbg3 span a::attr(href)').getall() + response.css('.windowbg span a::attr(href)').getall()
        
        striped_replies_views =  list(map(lambda x: x.strip(),replies_views))
        parsed_replies_views = list(filter(None,striped_replies_views))

        striped_last_posts = list(map(lambda x: x.strip(),last_posts))
        parsed_last_posts = self.parse_last_posts(striped_last_posts)
        filtered_last_posts = list(filter(None,parsed_last_posts))
        formated_last_posts = self.format_last_post(filtered_last_posts)
        
        replies = parsed_replies_views[::2]
        views = parsed_replies_views[1::2]
        topic_id = self.get_topic_id(topic_url)

        for quad in zip(subjects, replies, views, formated_last_posts, topic_url, topic_id):
            loader = ItemLoader(item=BitcointalkItem(), response = response)
            loader.add_value('subject', quad[0])
            loader.add_value('replies', int(quad[1]))
            loader.add_value('views', int(quad[2]))
            loader.add_value('last_post', quad[3])
            loader.add_value('topic_url', quad[4])
            loader.add_value('topic_id', float(quad[5]))
            btc_item = loader.load_item()
            yield btc_item
