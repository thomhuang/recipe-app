import scrapy
import pandas as pd
import numpy as np
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup


class cuisine_spider(scrapy.Spider):
    name = "cuisine"

    start_urls = ["https://www.seriouseats.com/recipes/topics/cuisine/american"]

    def parse(self, response):
        section = response.css('section.c-cards.c-cards--3-wide')
        articles = section.css('article')
        for i in range(0, 24):
            url = articles[i].css('a').attrib['href']
            yield scrapy.Request(url, callback=self.parse_recipe)

    def parse_recipe(self, response):
        title = response.css("h1.title.recipe-title.c-post__h1::text").get()

        author = response.css("a.name::text").get()

        ingredients = "\n".join(response.css("li.ingredient::text").getall())

        recipe_procedure = "\n\n".join(response.css("ol.recipe-procedures-list.instructions").xpath(
            '//*[@id="recipe-wrapper"]/div/ol/li/div/p/text()').getall())

        tags = "\n".join(response.css("a.tag::text").getall())

        yield {
            "title": title,
            "author": author,
            "ingredients": ingredients,
            "recipe procedure": recipe_procedure,
            "tags": tags
        }
