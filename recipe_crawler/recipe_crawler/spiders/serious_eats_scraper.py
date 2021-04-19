import scrapy

#This is just preliminary work to scrape the necessary information off of the SeriousEats.com website. I used the most popular recipe page on the website according to them.

class ingredientsSpider(scrapy.Spider):

	name = "recipe" #We call our spider "recipe" to be referenced in the shell

	start_urls = ["https://www.seriouseats.com/recipes/2016/12/the-best-roast-potatoes-ever-recipe.html"] #our URL to work with

	def parse(self, response):

		for elements in response.css("div.recipe-body.summary"): # div.recipe-body.summary contains all the information we need
        
            #The information extracted below is self-explanatory

			title = response.css("h1.title.recipe-title.c-post__h1::text").get()

			author = response.css("a.name::text").get()

			ingredients = response.css("li.ingredient::text").getall() #Returns array

			recipe_procedure = response.css("ol.recipe-procedures-list.instructions").xpath('//*[@id="recipe-wrapper"]/div/ol/li/div/p/text()').getall() #Returns array

			yield{ #How we lay out our information in the outputted file
				"title" : title,
				"author" : author,
				"ingredients" : ingredients,
				"recipe procedure" : recipe_procedure
			}
            
            #As a lot of the text itself contains commas, it might not be best to utilize a .csv extension. Perhaps a .json file would help, using the JSON1 extension of SQLite3