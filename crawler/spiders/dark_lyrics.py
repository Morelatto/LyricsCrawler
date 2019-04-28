import scrapy
import string

from crawler.items import DarkLyricsSongLoader, DarkLyricsRecordLoader


class DarkLyricsSpider(scrapy.Spider):
    name = "dark_lyrics"
    url = "http://www.darklyrics.com"

    def start_requests(self):
        for char in list(string.ascii_lowercase) + ["19"]:
            yield scrapy.Request(url="{url}/{char}.html".format(url=self.url, char=char), callback=self.parse_artists)

    def parse_artists(self, response):
        for artist in response.css("div.artists a::attr(href)").extract():
            artist_url = response.urljoin(artist)
            yield scrapy.Request(artist_url, callback=self.parse_albums)

    def parse_albums(self, response):
        for album in response.css("div.album"):
            track_url = response.urljoin(album.css("a::attr(href)").extract_first())
            yield scrapy.Request(track_url, callback=self.parse)

    def parse(self, response):
        songs = list()
        for lyrics_n in response.css("div.lyrics a::attr(name)").extract():
            song_loader = DarkLyricsSongLoader(selector=response)

            lyrics_div_loader = song_loader.nested_xpath("//div[@class='lyrics']")
            lyrics_div_loader.add_xpath("number", "//a[@name={}]/text()".format(lyrics_n), re="(\d+)\.")
            lyrics_div_loader.add_xpath("title", "//a[@name={}]/text()".format(lyrics_n), re="\. (.+)")
            lyrics_div_loader.add_xpath("lyrics", "//text()[count(preceding-sibling::h3)={}]".format(lyrics_n))
            songs.append(song_loader.load_item())

        record_loader = DarkLyricsRecordLoader(selector=response)

        record_loader.add_css("artist", "h1 a::text", re="(.+) LYRICS")
        record_loader.add_css("title", "h2::text", re="\"(.+)\"")
        record_loader.add_css("type", "h2::text", re="(\w+):")
        record_loader.add_css("year", "h2::text", re="\((\d+)\)")
        record_loader.add_value("songs", songs)

        yield record_loader.load_item()
