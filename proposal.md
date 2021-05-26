## Abstract

With the unexpected lockdown, many people are sure to have started cooking themselves, so we decided to create this app to make home cooks’ lives easier in the kitchen. Often times, home cooks have trouble finding recipes, not to mention those that work with what they have in their pantry and this hopefully solves this issue. Thus, our app works to retrieve data from www.SeriousEats.com and utilize the information to query recipes containing specific ingredients/authors/cuisines/etc. directly to the user.

## Planned Deliverables

As stated in the abstract, we will work to web scrape website(s) such as www.SeriousEats.com to obtain recipe data. With this information, we will be able to create an application that utilizes this information and display the user with recipes that use ingredients they have on hand.
A partial success of our project would entail getting the bare necessities in terms of the features done. So, for example:

* web-scraping all recipes from the website(s) successfully and completely
* manipulating and cleaning the data to be readable/clear in its contents
* After a user inputs a list of their ingredients at hand, they get back an easy to view list of recipes that correspond to it
* Any form of a user-interface OR a repository that provides all necessary algorithms/data needed to make it a user interface.
A full success of our project would of course do everything our partial success would have, but also allow us to:
* query recipes from specific authors
* query under a specific category
* unit conversions
* additional notes within the recipe
* recipe suggestions from given ingredients

## Resources Required

We practically will not need to obtain resources other than the websites that we take the data from. From the website(s) that we are choosing, they will all be free to access and public so there will not be any problems with obtaining data legally and fairly, as well as us not obtaining any profit in any way from this application.

## Tools/Skills Required

The tools needed will be:

* `scrapy`
* `pandas`
* `SQLite3`
* `PyQt5`

## Risks

There are a few things that could potentially stop us from achieving our full deliverables. For instance, the querying for recipes could be too slow for an enjoyable user experience, or our data taken from the website is unusable.

## Ethics

With our specific project, there shouldn’t be any particular ethical issues. With the scope of our project, the techniques used such as web-scraping and compiling data COULD be unethical, we are only taking information that is shown publicly on the websites that contain no personal data, etc.

In terms of the ***kinds*** of recipes that will be represented, there may be concern of bias towards certain cuisines/regions of the world, however we simply take the cuisines that are available on the website itself, which cover the 6 major continents of the world. So, we take recipes originating from:

* Africa
* Asia
* Europe
* North America
* South America

Which we'd say is a pretty broad and diverse range of recipes.

Furthermore, there may be questions of what differentiates our app from simply using the webite itself. In our eyes, our app gives a more focused and personalized experience for the user, where they can query for ***specific*** recipes from certain authors, ingredients, cuisines, and tags. In addition to that, it gives the user an option to find recipes in an offline setting on the off-chance that they don't have access to internet/has access to unreliable internet.

## Timeline

* Week 2 : By the end of week two, we should have web-scraped all the information we need from the websites.
* Week 4: We should have manipulated and cleaned the data so that it is actually parseable and readable.
* Week 6: We’ll work on matching the user’s input to the data values, and if time permits we could make a user interface to compliment the functionality.
