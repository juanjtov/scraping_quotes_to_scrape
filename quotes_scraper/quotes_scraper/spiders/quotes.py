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
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUESTS': 24,  # requests at the same time
        'MEMUSAGE_LIMIT_MB': 2048,  # rRam limit for the scraper
        # Emails list which scrapy it's gonna send notifications after it reaches the limit.
        'MEMUSAGE_NOTIFY_MAIL': ['juanjosetmontana@gmail.com'],
        'ROBOTSTRXT_OBEY': True,  # if wether or not scrapy it's gonna follow robots.txt
        'USER_AGENT': 'Pudito Tov',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    # new parse for multiple callbacks
    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            authors = kwargs['authors']

        next_quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        next_authors = response.xpath(
            '//small[@class="author"]/text()').getall()

        if kwargs['quotes_number'] is not None:
            quotes_number = kwargs['quotes_number']
            next_quotes = next_quotes[:quotes_number]
            next_authors = next_authors[:quotes_number]

        quotes.extend(next_quotes)
        authors.extend(next_authors)

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()

        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'quotes_number': quotes_number, 'authors': authors})

        else:
            yield {
                'quotes': quotes,
                'authors': authors
            }

    def parse(self, response):

        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags = response.xpath(
            '//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        authors = response.xpath('//small[@class="author"]/text()').getall()

        top = getattr(self, 'top', None)
        quotes_number = getattr(self, 'quotes_number', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]

        if quotes_number:
            quotes_number = int(quotes_number)
            quotes = quotes[:quotes_number]
            authors = authors[:quotes_number]

        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath(
            '//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'quotes_number': quotes_number, 'authors': authors})
