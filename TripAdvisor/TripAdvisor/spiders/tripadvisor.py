# -*- coding: utf-8 -*-
import scrapy
from TripAdvisor.items import TripadvisorItem
from scrapy import Selector


class TripadvisorSpider(scrapy.Spider):
    name = "tripadvisor"
    allowed_domains = ["tripadvisor.com"]

    i = 0
    increment = 20
    first_link ="https://www.tripadvisor.com/Attractions-g191-Activities-United_States.html"
    start_urls = []

    # loop through all pagination link from location list
    while i < 333:

        link = "https://www.tripadvisor.com/Attractions-g191-Activities-oa{}-United_States.html#LOCATION_LIST".format(
        str(increment))
        start_urls.append(link)
        increment +=50
        i +=1

    def parse(self,response):
        '''
        parse  each link from the location list and callback parse_attraction_list
        '''
        for sel in response.xpath("//ul[@class='geoList']"):
            location_link = sel.xpath("li/a/@href").extract()
            links = []
            for href in location_link:
                location_link = response.urljoin(href)
                links.append(location_link)

                yield scrapy.Request(location_link, callback=self.parse_attraction_list)

    def parse_attraction_list(self, response):
        '''
        parse each attraction link from list of attractions from each  location and callback parse_attraction_contents
        '''
        for href in response.xpath("//div[@class='property_title']/a/@href").extract():
            url = response.urljoin(href)
            print("I am here"+url)
            yield scrapy.Request(url, callback=self.parse_attraction_contents)
    #

    def parse_attraction_contents(self, response):
        '''
        parse each attraction  to extract its contents
        '''
        for select in response.xpath('//span[@class="format_address"]'):

            trip_item = TripadvisorItem()# instantiate TripadvisorItem to store data extracted
            trip_item['link'] = response.url

            trip_item['street_address'] = select.xpath('span[@class="street-address"]/text()').extract() + select.xpath('span[@class="extended-address"]/text()').extract()

            trip_item['address_locality'] = select.xpath('span[@class="locality"]/span[@property="addressLocality"]/text()').extract()
            trip_item['address_region'] = select.xpath('span[@class="locality"]/span[@property="addressRegion"]/text()').extract()
            trip_item['postal_code'] = select.xpath('span[@class="locality"]/span[@property="postalCode"]/text()').extract()
            trip_item['title']=  response.xpath("//h1[@id='HEADING']/text()")[1].extract().strip()

            trip_item['review'] = response.xpath('//a[@class="more"]/text()').extract()
            div = response.xpath("//div[@class='slim_ranking']").extract()
            sel = Selector(text=div[0])
            trip_item['rank'] = sel.xpath("string(//div[1])").extract_first().strip()

            trip_item['phone'] = response.xpath('//div[@class="phoneNumber"]/text()').extract()[0][14:]#slicing to extract only number

            yield trip_item









