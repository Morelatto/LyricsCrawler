# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, MapCompose, TakeFirst
from w3lib.html import remove_tags as _remove_tags

remove_tags = Compose(MapCompose(_remove_tags), TakeFirst())
remove_lyrics_text = lambda text: text[:-7] if text.endswith(" LYRICS") else text


class DarkLyricsItemLoader(ItemLoader):
    default_item_class = DarkLyricsItem

    artist_in = remove_lyrics_text
    lyrics_out = remove_tags


class DarkLyricsItem(scrapy.Item):
    artist = scrapy.Field()
    record = scrapy.Field()
    record_type = scrapy.Field()
    year = scrapy.Field()
    track = scrapy.Field()
    lyrics = scrapy.Field()
