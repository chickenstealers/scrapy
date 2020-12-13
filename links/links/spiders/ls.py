import re
from urllib.parse import urlparse
import scrapy

class LinkSpider(scrapy.Spider):
    name = "links"
    domain = ''

    def __init__(self, url='http://www.example.com', *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        div = response.css('div.download-eps')[1]
        #print(div)
        for linkep in div.css('ul li'):
            #print(linkep.css('strong::text').get())
            #print(linkep.css('span a::attr(href)')[0].get())
            if linkep.css('strong::text').get() != "360p ":
                yield {
                    'title': response.css('title::text').get(),
                    'quality': linkep.css('strong::text').get(),
                    'link': linkep.css('span a::attr(href)')[0].get()
                }
        next_page = response.css('div.rght a::attr(href)').get()
        print(next_page)
        if (next_page != '#'):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            print('No Next Page Dude')
