# dishCrawl
 A spider that get all the urls of dishes and then exacts complete detail about that and then stores them in JSON file. I use Selenium and BeautifulSoup to collect  recipes from a food website and store them in a structured format in a database. The two tasks involved in collecting the recipes are:
- Get all the recipe urls from the website using selenium
- Convert the html information of a recipe webpage into a structed json using beautiful soup.

 For our task, I picked the [NDTV food](https://food.ndtv.com/recipes) as a source for extracting recipes.

## Selenium
 [Selenim Webdriver](https://www.selenium.dev/projects/) automates web browsers. The important use case of it is for autmating web applications for the testing purposes. It can also be used for web scraping. In our case, I used it for extracting all the urls corresponding to the recipes.
### Installation
 I used selenium python bindings for using selenium web dirver. Through this python API, we can access all the functionalities of selenium web dirvers like Firefox, IE, Chrome, etc. We can use the following command for installing the selenium python API.
 ```bash
 pip install selenium
 ```
 Selenium python API requires a web driver to interface with your choosen browser. The corresponding web drivers can be downloaded from the following links. And also make sure it is in your PATH, e.g. ```/usr/bin``` or ```/usr/local/bin```. For more information regarding installation, please refer to the [link](https://selenium-python.readthedocs.io/installation.html).
 I used geckodriver to automate Firefox browser.
 
 ## Beautiful Soup
  [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) library is use to parse the opened html,which is done by [urllib](https://docs.python.org/3/library/urllib.html) library of python.
  
 **Note:-** This project is solely based on [Swetha's Blog](https://swethatanamala.github.io/2018/09/01/web-scraping-using-python-selenium-and-beautiful-soup/)
 
