import scrapy 
import requests
from scrapy.linkextractors import LinkExtractor

class food_spider(scrapy.Spider):

	"""
	This objects creates a Scrapy scraper which scrapes recipe information from seriouseats.com. 
	It returns a csv with the following columns representing each recipe:

	1. Recipe Title
	2. Author
	3. Cuisine
	4. Ingredients
	5. Recipe Procedure
	6. Tags
	7. Website URL

	The scraper is given a main cuisine page Eg. Asia. It scrapes all the recipes from this page and also scans the links to other sub cuisines such as Indian, Chinese etc. 
	The scraper visits the links of these subcuisines and scrapes the recipes from those pages as well. 
	"""

	name = "ultra"

	start_urls = [
		"https://www.seriouseats.com/southern-european-cuisine-guides-5117097", # Europe
		"https://www.seriouseats.com/greek-cuisine-guides-5117096",
		"https://www.seriouseats.com/mediterranean-cuisine-guides-5117094",
		"https://www.seriouseats.com/spanish-cuisine-guides-5117092",
		"https://www.seriouseats.com/northern-european-cuisine-guides-5117102",
		"https://www.seriouseats.com/eastern-european-cuisine-guides-5117107",
		"https://www.seriouseats.com/western-european-cuisine-guides-5117091",
		"https://www.seriouseats.com/central-african-cuisine-guides-5117175", # Africa
		"https://www.seriouseats.com/east-african-cuisine-guides-5117174",
		"https://www.seriouseats.com/north-african-cuisine-guides-5117171",
		"https://www.seriouseats.com/southern-african-cuisine-guides-5117168",
		"https://www.seriouseats.com/west-african-cuisine-guides-5117167",
		"https://www.seriouseats.com/african-recipes-5117276",
		"https://www.seriouseats.com/central-asian-cuisine-guides-5117163", # Asia
        "https://www.seriouseats.com/east-asian-cuisine-guides-5117162",
        "https://www.seriouseats.com/south-asian-cuisine-guides-5117153",
        "https://www.seriouseats.com/southeast-asian-cuisine-guides-5117147",
        "https://www.seriouseats.com/middle-eastern-cuisine-guides-5117157",
		"https://www.seriouseats.com/north-american-cuisine-guides-5117134", # North and South America
        "https://www.seriouseats.com/american-cuisine-guides-5117133",
        "https://www.seriouseats.com/canadian-cuisine-guides-5117121",
        "https://www.seriouseats.com/mexican-cuisine-guides-5117119",
        "https://www.seriouseats.com/south-american-cuisine-guides-5117118",
        "https://www.seriouseats.com/brazilian-cuisine-guides-5117117",
        'https://www.seriouseats.com/colombian-cuisine-guides-5117116',
        "https://www.seriouseats.com/venezuelan-cuisine-guides-5117114",
        "https://www.seriouseats.com/peruvian-cuisine-guides-5117115" 	
	]

	def __init__(self):
		self.link = "default"
		self.cuisine = "default"

	def parse(self, response):

		# all the recipe links in the cuisine page
		recipes = response.xpath("//div [@class='comp card-list__item mntl-block']")

		# all the sub cuisine links in the main cuisine page 
		sub_cuisines = response.xpath("//div [@class='loc section-header']")

		# scrape the recipes in the main cuisine page
		for recipe in recipes:

			recipe_url = recipe.css('a').attrib['href']

			self.cuisine = recipe.css("div.card__tag").attrib['data-tax-tag']

			yield scrapy.Request(recipe_url, callback = self.parse_recipe)

		# scrape the sub cuisine pages
		for cuisine in sub_cuisines:

			subc_link = cuisine.css('a').attrib['href']

			yield scrapy.Request(subc_link, callback = self.parse_subc)

	
	# function to parse the subcuisines
	def parse_subc(self, response):

		# all the recipe links in the cuisine page
		recipes = response.xpath("//div [@class='comp card-list__item mntl-block']")

		# scrap the recipes in the main cuisine page
		for recipe in recipes:

			self.cuisine = recipe.css("div.card__tag").attrib['data-tax-tag']

			recipe_url = recipe.css('a').attrib['href']

			yield scrapy.Request(recipe_url, callback = self.parse_recipe)

	
	# function to parse the recipe
	def parse_recipe(self,response):

		# get the title 
		title = response.css("h1.heading__title::text").get()

		# get the author 
		author = response.css('span.link__wrapper::text').get()

		# get the ingredients
		ingred = response.xpath("//div [@class='loc section-content section__content ']")[0] # Ingredient portion of section is first element
		li = ingred.css('li').xpath('string()').extract() # This gives full strings of each ingredient while ignoring hyperlink splitting
		li = [str.strip(sen) for sen in li] # Removes all unnecessary text such as \n or html elements
		li = [empty_str for empty_str in li if empty_str] # Remove any unnecessary empty strings from our ingredient list
		ingreds = '\n\n'.join(li) # Join together by new lines

		# get the directions, same process as ingredients
		dirs = response.xpath("//div [@class='loc section-content section__content ']")[1]  # Recipe directions portion of section is first element
		li = dirs.css('li').xpath('string()').extract()
		li = [str.strip(sen) for sen in li]
		li = [empty_str for empty_str in li if empty_str]
		
		to_remove = response.xpath("/html/body/main/article/div[1]/div/div[2]/div[2]/section[2]/div/div[1]/ul").css('li').css("::text").extract()
		li = [steps for steps in li if steps not in to_remove]

		dirs = '\n\n'.join(li)

		# getting tags
		tags = response.xpath("//div [@class='loc tag-nav-content']")
		tags = tags.css('a').css('::text').extract()

		#getting url

		curr_url = response.url

		yield { 
			"Recipe Title" : title,
			"Author" : author,
			"Cuisine": self.cuisine,
			"Ingredients" : ingreds,
			"Recipe Procedure" : dirs,
			"Tags" : tags,
			"Website URL": curr_url
		}

	# test the sub cuisine scraper manually

