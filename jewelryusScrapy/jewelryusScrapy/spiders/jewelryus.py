# -*- coding: utf-8 -*-
import scrapy
from jewelryusScrapy.items import *
from scrapy import Request

class JewelryusSpider(scrapy.Spider):
	name = 'jewelryus'
	allowed_domains = ['jewelryus.shop']
	start_urls = ['https://www.jewelryus.shop/index.php?main_page=all_products']
	# jewelry_list_url = 'https://www.jewelryus.shop/index.php?main_page=all_products&page={page}'
	# jewelry_detail_url = 'https://www.jewelryus.shop/index.php?main_page=product&pID={pid}'
 
	def parse(self, response):
		# self.logger.debug(response.text)
		# self.logger.debug(response.text)
		jewelries = response.css('.products-grid')
		for jewelry in jewelries:
			# item = JewelryusscrapyItem()
			# item['name'] = jewelry.css('.product-name a::text').extract_first()
			# item['regular_price'] = jewelry.css('.old-price .price::text').extract_first()
			# item['sale_price'] = jewelry.css('.specials-price .price::text').extract_first()
			# yield item

			jewelry_detail_url = jewelry.css('a::attr("href")').extract_first()
			yield Request(jewelry_detail_url, self.parse_jewelry_detail)
		next_page = response.css('.pages .next::attr("href")').extract_first()
		yield Request(url=next_page, callback=self.parse)

	def parse_jewelry_detail(self, response):
		jewelry = response.css('.product-shop-box')
		item = JewelryusscrapyItem()
		item['name'] = jewelry.css('.product-name h1::text').extract_first()
		item['sku'] = jewelry.css('.sku span::text').extract_first()
		item['availability'] = jewelry.css('.availability span::text').extract_first()
		item['regular_price'] = jewelry.css('.old-price .price::text').extract_first()
		item['sale_price'] = jewelry.css('.specials-price .price::text').extract_first()
		item['detail'] = jewelry.css('.description .std::text').extract_first()
		image = response.css('.product-img-box a::attr("href")').extract_first()
		item['images'] = response.urljoin(image)
		yield item