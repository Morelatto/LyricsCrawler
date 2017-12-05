# -*- coding: utf-8 -*-

import scrapy

from scrapy import Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class DarkLyricsRecord(Item):
    artist = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    year = scrapy.Field()
    songs = scrapy.Field()


class DarkLyricsSong(Item):
    number = scrapy.Field()
    title = scrapy.Field()
    lyrics = scrapy.Field()


class DarkLyricsRecordLoader(ItemLoader):
    default_item_class = DarkLyricsRecord

    artist_out = TakeFirst()
    title_out = TakeFirst()
    type_out = TakeFirst()
    year_out = TakeFirst()


class DarkLyricsSongLoader(ItemLoader):
    default_item_class = DarkLyricsSong

    number_out = TakeFirst()
    title_out = TakeFirst()
