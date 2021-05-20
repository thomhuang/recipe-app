import scrapy


# This is just preliminary work to scrape the necessary information off of the SeriousEats.com website.
# I used the most popular recipe page on the website according to them.
class ingredients_spider(scrapy.Spider):
    name = "recipe"  # We call our spider "recipe" to be referenced in the shell

    start_urls = [
        "https://www.seriouseats.com/recipes/2016/12/the-best-roast-potatoes-ever-recipe.html"]  # our URL to work with

    def parse(self, response):
        # The information extracted below is self-explanatory

        title = response.css("h1.title.recipe-title.c-post__h1::text").get()

        author = response.css("a.name::text").get()

        ingredients = "\n".join(response.css("li.ingredient::text").getall())
        # Returns string with each ingredient separated with a new line

        recipe_procedure = "\n\n".join(response.css("ol.recipe-procedures-list.instructions").xpath(
            '//*[@id="recipe-wrapper"]/div/ol/li/div/p/text()').getall())
        # Returns string with each step of the recipe separated with a new line

        tags = "\n".join(response.css("a.tag::text").getall())
        # Returns a string with each tag separated with a new line

        yield {  # How we lay out our information in the outputted file
            "title": title,
            "author": author,
            "ingredients": ingredients,
            "recipe procedure": recipe_procedure,
            "tags": tags
        }

    # to save as .csv, in your terminal: scrapy crawl recipe -o recipes.csv
