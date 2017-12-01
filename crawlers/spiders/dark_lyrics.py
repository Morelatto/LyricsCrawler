import scrapy
import string

from crawlers.items import DarkLyricsItemLoader


class DarkLyricsSpider(scrapy.Spider):
    name = "dark_lyrics"
    url = "http://www.darklyrics.com"

    def start_requests(self):
        for char in list(string.ascii_lowercase) + ["19"]:
            yield scrapy.Request(url="{url}/{char}.html".format(url=self.url, char=char), callback=self.parse_artists)
            break

    def parse_artists(self, response):
        for artist in response.css("div.artists a::attr(href)").extract():
            artist_url = response.urljoin(artist)
            yield scrapy.Request(artist_url, callback=self.parse_albums)
            break

    def parse_albums(self, response):
        for album in response.css("div.album"):
            track_url = response.urljoin(album.css("a::attr(href)").extract_first())
            yield scrapy.Request(track_url, callback=self.parse)

    def parse(self, response):
        for lyric_n in response.css("div.lyrics a::attr(name)").extract():
            loader = DarkLyricsItemLoader(selector=response)

            loader.add_css("artist", "h1 a::text")
            loader.add_css("record", "h2::text")
            loader.add_css("record_type", "h2::text")
            loader.add_css("year", "h2::text")
            loader.add_css("track", "")
            loader.add_xpath("lyrics", "//div[@class='lyrics']/text()[count(preceding-sibling::h3)={}]".format(lyric_n))

            yield loader.load_item()
