import scrapy

# Title = //h1/a/text()
# Quotes = //span[@class="text" and @itemprop="text"]/text()'
# Top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        print('*'*10)
        print('\n\n\n')

        title = response.xpath('//h1/a/text()').get()
        print(f'Tille: {title}')
        print('\n\n')

        quotes=response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        print('Quotes')
        for quote in quotes:
            print(f'- {quote}')
        print('\n\n')

        top_ten_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        print('Top ten tags')
        for tag in top_ten_tags:
            print(f'- {tag}')
        print('\n\n')


        
        #print(response.status, response.headers)
        print('\n\n')
        print('*'*10)
        