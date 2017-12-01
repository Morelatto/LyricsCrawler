#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapy import cmdline

cmdline.execute("scrapy crawl dark_lyrics -o dark_lyrics.json".split())
