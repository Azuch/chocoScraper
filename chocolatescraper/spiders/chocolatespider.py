import scrapy
from chocolatescraper.items import ChocolateProduct  
from chocolatescraper.itemloaders import ChocolateProductLoader

class ChocolateSpider(scrapy.Spider):

  #the name of the spider
  name = 'chocolatespider'

  #these are the urls that we will start scraping
  start_urls = ['https://www.chocolate.co.uk/collections/all']

  def parse(self, response):

      products = response.css('product-item')

      for product in products:
          chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
          chocolate.add_css('name', "a.product-item-meta__title::text")
          chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
          chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
          yield chocolate.load_item()

      next_page = response.css('[rel="next"] ::attr(href)').get()

      if next_page is not None:
          next_page_url = 'https://www.chocolate.co.uk' + next_page
          yield response.follow(next_page_url, callback=self.parse)

