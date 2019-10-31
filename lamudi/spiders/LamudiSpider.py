
import scrapy
import logging
import codecs
from datetime import datetime
import json

from lamudi.utils.LamudiPropertyPage import LamudiPropertyPage


class LamudiSpider(scrapy.Spider):
    name = "lamudi"

    def __init__(self, filename='properties.txt'):
        now = datetime.now(tz=None).strftime("%Y-%m-%d_%H_%M_%S.txt")
        logging.info("new filename for output is '{}'".format(now))
        self.filename = now
        # self.file_writer = open(filename, 'w+')
        self.file_writer = codecs.open(self.filename, "ab", "utf-8")
        logging.info("dataset file is " + self.filename)

    def append_property_json_to_file(self, dict_object):
        valid_json = json.dumps(dict_object, sort_keys=True)
        self.file_writer.write(valid_json + "\n")

    def start_requests(self):
        urls = [
            # 'https://www.lamudi.com.ph/condominium/buy/',
            # 'https://www.lamudi.com.ph/commercial/buy/',
            # 'https://www.lamudi.com.ph/land/buy/',
            # 'https://www.lamudi.com.ph/house/buy/',
            # 'https://www.lamudi.com.ph/apartment/buy/'
            'https://www.lamudi.com.ph/foreclosures/buy/'
        ]
        for url in urls:
            print("working on url " + url)
            yield scrapy.Request(url=url, callback=self.parse_index_page)

    @staticmethod
    def extract_next_index_page(response):
        selector = response.xpath('//*[@class="next "]/a/@href')
        if len(selector) > 0:
            return selector[0].get()
        return None

    def parse_index_page(self, response):
        logging.info('parsing index page ' + response.request.url)
        next_page = LamudiSpider.extract_next_index_page(response)
        linked_properties = LamudiSpider.extract_linked_properties(response)
        for linked_property in linked_properties:
            yield response.follow(linked_property, self.parse_property_page)
        logging.info("Found {} linked properties for index page '{}'".format(len(linked_properties), response.request.url))
        if next_page:
            yield response.follow(next_page, self.parse_index_page)

    @staticmethod
    def extract_linked_properties(response):
        selector = response.xpath('//h3[@class="ListingCell-KeyInfo-title"]/a/@href')
        return [s.get() for s in selector]

    def parse_property_page(self, response):
        logging.info("working on property page " + response.request.url)
        lpp = LamudiPropertyPage(response)
        json = lpp.dict
        self.append_property_json_to_file(json)

