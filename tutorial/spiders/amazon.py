import scrapy
import re
import json
from urllib.parse import urlencode, urljoin

API = '<YOUR_API_KEY>'
queries = ['tshirt for men', 'tshirt for women']

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = ['http://www.amazon.com/']

    def get_url(url):
        payload = {'api_key': API, 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url

    def parse(self, response):
        pass
    
    def start_requests(self):
        for query in queries:
            url = 'https://www.amazon.com/s?' + urlencode({'k': query})
            yield scrapy.Request(url=url, callback=self.parse_keyword_response)
            

    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')

        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.com/dp/{asin}"
            yield scrapy.Request(url=product_url, callback=self.parse_product_page, meta={'asin': asin})

        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            url = urljoin("https://www.amazon.com",next_page)
            yield scrapy.Request(url=product_url, callback=self.parse_keyword_response)

    def parse_product_page(self, response):
        asin = response.meta['asin']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        image = re.search('"large":"(.*?)"',response.text).groups()[0]
        rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
        number_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()

        if not price:
            price = response.xpath('//*[@data-asin-price]/@data-asin-price').extract_first() or \
                    response.xpath('//*[@id="price_inside_buybox"]/text()').extract_first()

        temp = response.xpath('//*[@id="twister"]')
        sizes = []
        colors = []
        if temp:
            s = re.search('"variationValues" : ({.*})', response.text).groups()[0]
            json_acceptable = s.replace("'", "\"")
            di = json.loads(json_acceptable)
            sizes = di.get('size_name', [])
            colors = di.get('color_name', [])

        bullet_points = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()
        seller_rank = response.xpath('//*[text()="Amazon Best Sellers Rank:"]/parent::*//text()[not(parent::style)]').extract()
        yield {'asin': asin, 'Title': title, 'MainImage': image, 'Rating': rating, 'NumberOfReviews': number_of_reviews,
               'Price': price, 'AvailableSizes': sizes, 'AvailableColors': colors, 'BulletPoints': bullet_points,
               'SellerRank': seller_rank}