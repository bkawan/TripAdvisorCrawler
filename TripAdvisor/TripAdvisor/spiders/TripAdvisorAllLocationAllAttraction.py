# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import Selector
from TripAdvisor.items import TripadvisorItem


class TripAdvisorAllLocationAllAttraction(CrawlSpider):
    name = "tripAllAttraction"
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
             callback="parse_each_attraction",
             follow=True),
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="nav next rndBtn ui_button primary taLnk"]',)),
             callback="parse_all_attraction",
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
                yield scrapy.Request(response.urljoin(link),callback=self.parse_all_attraction)



    def parse_all_attraction(self,response):


        sel = Selector(response)
        links = sel.xpath("//div[@class='property_title']")
        # print("**********")
        for link in links:
            l = link.xpath("a/text()").extract()
            # print(l)
            # print(link.xpath("a/text()").extract())

        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        for href in links:
            link_list = href.xpath("a/@href").extract()
        #     print(link_list)
        #     print("*******************")
            for link in link_list:


                attraction_link = response.urljoin(link)
                yield scrapy.Request(attraction_link,callback=self.parse_each_attraction)
                # print(attraction_link)
                # print("***********")



    def parse_each_attraction(self, response):
        sel = Selector(response)
        # print("********")
        # print(response.url)
        # print("********")


        for select in response.xpath('//span[@class="format_address"]'):
            street = select.xpath('span[@class="street-address"]/text()').extract() + select.xpath('span[@class="extended-address"]/text()').extract()
            print("**********")
            print(street)
            print("**********")



            trip_item = TripadvisorItem()  # instantiate TripadvisorItem to store data extracted
            trip_item['link'] = response.url

            trip_item['street_address'] = select.xpath('span[@class="street-address"]/text()').extract() + select.xpath(
                'span[@class="extended-address"]/text()').extract()

            trip_item['address_locality'] = select.xpath(
                'span[@class="locality"]/span[@property="addressLocality"]/text()').extract()
            trip_item['address_region'] = select.xpath(
                'span[@class="locality"]/span[@property="addressRegion"]/text()').extract()
            trip_item['postal_code'] = select.xpath(
                'span[@class="locality"]/span[@property="postalCode"]/text()').extract()
            trip_item['title'] = response.xpath("//h1[@id='HEADING']/text()")[1].extract().strip()

            trip_item['review'] = response.xpath('//a[@class="more"]/text()').extract()
            div = response.xpath("//div[@class='slim_ranking']").extract()
            sel = Selector(text=div[0])
            trip_item['rank'] = sel.xpath("string(//div[1])").extract_first().strip()

            trip_item['phone'] = response.xpath('//div[@class="phoneNumber"]/text()').extract()[0][
                                 14:]  # slicing to extract only number

            yield trip_item


