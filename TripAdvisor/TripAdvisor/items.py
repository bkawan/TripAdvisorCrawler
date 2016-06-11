# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    PlaceTitle = scrapy.Field()
    PlaceURL = scrapy.Field()
    TotalReviews = scrapy.Field()
    PlaceCategory = scrapy.Field()
    StreetAddress = scrapy.Field()
    AddressLocality = scrapy.Field()
    AddressRegion = scrapy.Field()
    PostCode = scrapy.Field()
    PhoneNumber = scrapy.Field()
    Ranking = scrapy.Field()
    LengthOfVisit = scrapy.Field()
    Fee = scrapy.Field()
    Description = scrapy.Field()
    AverageRating = scrapy.Field()
    OpeningHours = scrapy.Field()

    Email = scrapy.Field()
    Website = scrapy.Field()

    Longitude = scrapy.Field()
    Latitude = scrapy.Field()


    # state_attraction_link = scrapy.Field()
    # state_name = scrapy.Field()
    # state_attraction_name = scrapy.Field()


class TripReviewItem(scrapy.Item):
    LocationTitle = scrapy.Field()
    Username = scrapy.Field()
    UserImageURL = scrapy.Field()
    ReviewPictureURL = scrapy.Field()
    Rating = scrapy.Field()
    CommentTitle = scrapy.Field()
    CommentDate = scrapy.Field()
    Comment = scrapy.Field()
    LocationURL = scrapy.Field()

