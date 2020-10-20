# -*- coding: utf-8 -*-
import scrapy
from TripAdvisor.items import TripadvisorItem
from scrapy import Selector


class TripadvisorSpider(scrapy.Spider):
    name = "tripadvisor"
    allowed_domains = ["tripadvisor.com"]
    start_urls = [
        "https://www.tripadvisor.com/Attractions-g191-Activities-United_States.html",
        # "https://www.tripadvisor.com/Attractions-g34345-Activities-oa30-Key_West_Florida_Keys_Florida.html"
    ]

    def parse(self, response):

        sel = Selector(response)
        print("************** First **************************")

        subject = sel.xpath('//div[@class="property_title"]/a/text()').extract()
        links = sel.xpath('//div[@class="property_title"]/a/@href').extract()

        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_each_attraction)

        sites = sel.xpath('//a[contains(text(), "Next")]/@href').extract()
        for site in sites:
            if not site:
                continue
            site_link = response.urljoin(si)
            yield scrapy.Request(site_link, callback=self.parse_location)

        print("************** First **************************")

    def parse_location(self, response):
        sel = Selector(response)
        print(" **************** LOCATION LIST *************")
        print(response.url)
        print(" **************** LOCATION LIST *************")

        location = sel.xpath("//ul[@class='geoList']")
        for loc in location:
            state_link = loc.xpath("li/a/@href").extract()
            print(" **************** Attraction List starts *************")

            for link in state_link:
                url_link = response.urljoin(link)
                print(url_link)
                # "https://www.tripadvisor.com/Attractions-g34345-Activities-Key_West_Florida_Keys_Florida.html"
                yield scrapy.Request(url_link, callback=self.parse_attraction)
            print(" **************** Attraction List  ends *************")



            # yield scrapy.Request(url_link,callback=self.parse_test)

        locations = sel.xpath("//a[@class='guiArw sprite-pageNext  pid0']/@href").extract()
        print(" **************** LOCATION LIST  PAGINATION  starts *************")
        print(locations)
        print(" **************** LOCATION Link *************")

        for location in locations:
            if location:
                location_link = response.urljoin(location)
                print(location_link)
                yield scrapy.Request(location_link, callback=self.parse_location)
        print(" **************** LOCATION Link *************")

        print(" **************** LOCATION LIST  PAGINATION  ends *************")

    def parse_attraction(self, response):

        print(" **************** Attraction URL reponse *************")
        print(response.url)
        print(" **************** Attraction URL reponse *************")

        sel = Selector(response)
        subject = sel.xpath('//div[@class="property_title"]/a/text()').extract()
        links = sel.xpath('//div[@class="property_title"]/a/@href').extract()

        print(" **************** Attraction URL List starts *************")

        for link in links:
            link = response.urljoin(link)
            print(link)

            yield scrapy.Request(link, callback=self.parse_each_attraction)
        print(" **************** Attraction URL List ends *************")

        sites = sel.xpath('//a[contains(text(), "Next")]/@href').extract()
        for si in sites:
            if si:
                ss = response.urljoin(si)
                yield scrapy.Request(ss, callback=self.parse_attraction)

    def parse_each_attraction(self, response):
        sel = Selector(response)
        # print("********")
        # print(response.url)
        # print("********")

        trip_item = TripadvisorItem()
        title = response.xpath("//h1[@id='HEADING']/text()").extract()
        place_title = ""
        for t in title:
            place_title += t
        trip_item['PlaceTitle'] = place_title.strip()

        trip_item['PlaceURL'] = response.url

        if len(response.xpath('//a[@class="more"]/text()').extract()) > 0:
            total_reviews = response.xpath('//a[@class="more"]/text()').extract()[0].split("R")[0]
            trip_item['TotalReviews'] = total_reviews
        else:
            trip_item['TotalReviews'] = ""
        # total_reviews = response.xpath('//a[@class="more"]/text()').extract()[0].split("R")[0]


        #
        if len(response.xpath("//div[@class='separator']").extract()) > 0:
            placeCatDiv = response.xpath("//div[@class='separator']").extract()
            placeCatSel = Selector(text=placeCatDiv[0])
            trip_item['PlaceCategory'] = placeCatSel.xpath("string(//div[1])").extract_first().strip()
        else:
            trip_item['PlaceCategory'] = ""

        trip_item['StreetAddress'] = response.xpath(
            '//span[@class="street-address"]/text()').extract() + response.xpath(
            'span[@class="extended-address"]/text()').extract()
        trip_item['AddressLocality'] = response.xpath(
            '//span[@class="locality"]/span[@property="addressLocality"]/text()').extract()
        trip_item['AddressRegion'] = response.xpath(
            '//span[@class="locality"]/span[@property="addressRegion"]/text()').extract()
        trip_item['PostCode'] = response.xpath(
            '//span[@class="locality"]/span[@property="postalCode"]/text()').extract()
        phone_number = response.xpath('//div[@class="phoneNumber"]/text()').extract()
        if phone_number:
            trip_item['PhoneNumber'] = phone_number[0].split(":")[1].strip()

        #
        #
        div = response.xpath("//div[@class='slim_ranking']").extract()
        if div:
            sel = Selector(text=div[0])
            trip_item['Ranking'] = sel.xpath("string(//div[1])").extract_first().strip()
        else:
            trip_item['Ranking'] = ""

        len_fee = response.xpath("//div[@class='details_wrapper']/div[@class='detail']/text()").extract()

        if len_fee:
            trip_item['LengthOfVisit'] = len_fee[-3].strip()
            trip_item['Fee'] = len_fee[-1].strip()
        else:
            trip_item['LengthOfVisit'] = ""
            trip_item['Fee'] = ""

        trip_item['Description'] = response.xpath("//div[@class='listing_details']/p/text()").extract()
        # trip_item['AverageRating'] = response.xpath("//div[@class='valueCount fr part']/text()")[2].extract()
        rating = response.xpath("//div[@class='valueCount fr part']/text()").extract()
        if rating:
            trip_item['AverageRating'] = rating[2]
        else:
            trip_item['AverageRating'] = ""

        email_div = response.xpath("//div[@class='taLnk fl']/@onclick").extract()

        if len(email_div) > 0:
            email = email_div[0].split(",")
            trip_item['Email'] = email[6].strip("/'")
        else:
            trip_item['Email'] = ""

        days = [d.strip() for d in response.xpath("//span[@class='days']/text()").extract() if d]
        hours = [h.strip() for h in response.xpath("//span[@class='hours']/text()").extract() if h]
        days_hours = dict(zip(days, hours))
        trip_item['OpeningHours'] = ""
        for day, hour in days_hours.items():
            trip_item['OpeningHours'] += day + " " + hour + " , "

        yield trip_item

