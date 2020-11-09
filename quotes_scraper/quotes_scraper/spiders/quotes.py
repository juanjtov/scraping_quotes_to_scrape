import scrapy

# Title = //h1/a/text()
# Quotes = //span[@class="text" and @itemprop="text"]/text()'
# Top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
# Next page button = //ul[@class="pager"]/li[@class="next"]/a/@href').get()


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    # Saving JSON automatically
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json'
    }

    # new parse for multiple callbacks
    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']

        next_quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()

        if kwargs['quotes_number'] is not None:
            quotes_number = kwargs['quotes_number']
            next_quotes = next_quotes[:quotes_number]

        quotes.extend(next_quotes)

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'quotes_number': quotes_number})

        else:
            yield {
                'quotes': quotes
            }

    def parse(self, response):

        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        top = getattr(self, 'top', None)
        quotes_number = getattr(self, 'quotes_number', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        if quotes_number:
            quotes_number = int(quotes_number)
            quotes = quotes[:quotes_number]

        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'quotes_number': quotes_number})
