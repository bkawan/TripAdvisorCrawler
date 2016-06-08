# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
from TripAdvisor.items import TripadvisorItem


class TripAdvisorAllLocation(CrawlSpider):
    name = "tripAllLocation"
    allowed_domains = ["tripadvisor.com"]
    start_urls = [
        "https://www.tripadvisor.com/Attractions-g191-Activities-United_States.html",
        "https://www.tripadvisor.com/Attractions-g191-Activities-oa20-United_States.html#LOCATION_LIST"


    ]

    rules = (
        # rules for location list
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="guiArw sprite-pageNext  pid0"]',)),
             callback="parse_location",
             follow=True),

        # rules for location list
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="nav next rndBtn ui_button primary taLnk"]',)),
             callback="parse_attraction",
             follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_location(response)




    def parse_location(self, response):
        sel = Selector(response)
        location = sel.xpath("//ul[@class='geoList']")

        print("************************")
        for loc in location:
            state_link = loc.xpath("li/a/@href").extract()
            for link in state_link:
                print(link)
                trip_location_item = TripadvisorItem()
                trip_location_item['state_attraction_link'] = response.urljoin(link)
                yield trip_location_item

        print("***********************")


    def parse_attraction(self,response):
        link = response.url



