import scrapy

from scrapy.loader import ItemLoader
from ..items import LbItem
from itemloaders.processors import TakeFirst


class LbSpider(scrapy.Spider):
	name = 'lb'
	start_urls = ['https://www.lb.lt/lt/naujienos']

	def parse(self, response):
		post_links = response.xpath('//div[@class="item col-xs-6 col-md-4 col-lg-3"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="page_next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('(//div[@class="text"])[2]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="item_date"]/text()').get()

		item = ItemLoader(item=LbItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
