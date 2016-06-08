# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
from TripAdvisor.items import TripadvisorItem


class TripAdvisorAllLocationAllAttraction(CrawlSpider):
    name = "test"
    allowed_domains = ["tripadvisor.com"]
    start_urls = [
        "https://www.tripadvisor.com/Attractions-g191-Activities-United_States.html",
        "https://www.tripadvisor.com/Attractions-g191-Activities-oa20-United_States.html#LOCATION_LIST",
        # "https://www.tripadvisor.com/Attractions-g60827-Activities-Brooklyn_New_York.html"


    ]

    rules = (
        # rules for location list
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="guiArw sprite-pageNext  pid0"]',)),
             callback="parse_location",
             follow=True),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="nav next rndBtn ui_button primary taLnk"]',)),
             callback="parse_all_attraction",
             follow=True),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="nav next rndBtn ui_button primary taLnk"]',)),
             callback="parse_test",
             follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_location(response)




    def parse_location(self, response):
        sel = Selector(response)
        location = sel.xpath("//ul[@class='geoList']")

        for loc in location:
            state_link = loc.xpath("li/a/@href").extract()
            for link in state_link:
                trip_location_item = TripadvisorItem()
                trip_location_item['state_attraction_link'] = response.urljoin(link)
                # self.start_urls.append(response.urljoin(link))
                yield scrapy.Request(response.urljoin(link),callback=self.parse_all_attraction)



    def parse_all_attraction(self,response):
        links = []
        links.append(response)
        print("**********")

        print(links)
        print("**********")
        # print("IIIIIIIIIIIIIIII")
        # print(response.url)
        # yield scrapy.Request(response.url, callback = self.parse_test)
        # sel = Selector(response)
        # links = sel.xpath("//div[@class='property_title']")
        # print("**********************")
        # for link in links:
        #     l = link.xpath("a/text()").extract()
        #     print(l)
        #     # print(link.xpath("a/text()").extract())
        #
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        # for href in links:
        #     link_list = href.xpath("a/@href").extract()
        # #     print(link_list)
        # #     print("*******************")
        #     for link in link_list:
        #
        #
        #         attraction_link = response.urljoin(link)
        #         yield scrapy.Request(attraction_link,callback=self.parse_each_attraction)
        #         # print(attraction_link)
        #         # print("***********")


    def parse_test(self,response):

        sel = Selector(response)
        # links = sel.xpath("//div[@class='property_title']")
        # print("**********************")
        # for link in links:
        #      l = link.xpath("a/text()").extract()
        #      print(l)
        #     # print(link.xpath("a/text()").extract())





    # def parse_each_attraction(self, response):
    #     sel = Selector(response)


