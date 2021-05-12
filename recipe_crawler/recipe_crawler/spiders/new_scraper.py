import scrapy 
import requests

class food_spider(scrapy.Spider):

	name = "ultra"

	'''
	def __init__(self):
		self.subc = "default"
	'''

	start_urls = ["https://www.seriouseats.com/north-american-recipes-5117205",
	"https://www.seriouseats.com/asian-recipes-5117262",
	"https://www.seriouseats.com/caribbean-cuisine-guides-5117113",
	"https://www.seriouseats.com/african-cuisine-guides-5117176",
	"https://www.seriouseats.com/south-american-cuisine-guides-5117118",
	"https://www.seriouseats.com/european-cuisine-guides-5117108"]

	def parse(self, response):

		# all the recipe links in the cuisine page
		recipes = response.xpath("//div [@class='comp card-list__item mntl-block']")

		# all the sub cuisine links in the main cuisine page 
		sub_cuisines = response.xpath("//div [@class='loc section-header']")

		# scrape the recipes in the main cuisine page
		for recipe in recipes:

			recipe_url = recipe.css('a').attrib['href']

			yield scrapy.Request(recipe_url, callback = self.parse_recipe)

		# scrape the sub cuisine pages
		for cuisine in sub_cuisines:

			subc_link = cuisine.css('a').attrib['href']

			#self.subc = cuisine.css('span.link__wrapper::text').get()

			yield scrapy.Request(subc_link, callback = self.parse_subc)

	
	# function to parse the subcuisines
	def parse_subc(self, response):

		# all the recipe links in the cuisine page
		recipes = response.xpath("//div [@class='comp card-list__item mntl-block']")

		# scrap the recipes in the main cuisine page
		for recipe in recipes:

			recipe_url = recipe.css('a').attrib['href']

			yield scrapy.Request(recipe_url, callback = self.parse_recipe)

	
	# function to parse the recipe
	def parse_recipe(self,response):

		# get the title 
		title = response.css("h1.heading__title::text").get()

		# get the author 
		author = response.css('span.link__wrapper::text').get()

		# get the ingredients
		ingred = response.xpath("//div [@class='loc section-content section__content ']")
		li = ingred[0].css('li').css('::text').extract()
		li = [str.strip(sen) for sen in li]
		ingreds = ",".join(li)

		# get the directions
		dirs = response.xpath("//div [@class='loc section-content section__content ']")[1]
		li = dirs.css('li').css('::text').extract()
		li = [str.strip(sen) for sen in li]
		dirs = "".join(li)

		# getting tags
		tags = response.xpath("//div [@class='loc tag-nav-content']")
		tags = tags.css('a').css('::text').extract()

		yield { 
			"title" : title,
			#"sub_cs": self.subc,
			"author" : author,
			"ingredients" : ingreds,
			"recipe procedure" : dirs,
			"tags" : tags
		}

	# test the sub cuisine scraper manually

