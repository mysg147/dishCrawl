from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException,WebDriverException
#from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.action_chains import ActionChains
import sqlite3
import json
import ssl
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import os
import time

conn=sqlite3.connect('dish_url.sqlite')
cur=conn.cursor()


cur.execute('CREATE TABLE IF NOT EXISTS url (id INTEGER PRIMARY KEY,url TEXT UNIQUE)')


options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(30)
driver.get("https://food.ndtv.com/recipes")
#print(driver.page_source)
os.system('cls' if os.name=='nt' else 'clear')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


#Get list of text in all element by class name
def get_list_by_className(class_name='main_image'):
    element_list=[]
    try:
        all_elements=driver.find_elements_by_class_name(class_name)
        element_list=[x.text for x in all_elements if len(x.text)>0]
    except NoSuchElementException as e:
        print(e)
    except(WebDriverException) as e:
        print(e)
    #print(element_list)
    #print ("*"*25)
    return element_list

#Find link in the page with given text
def get_link_by_text(text):
    element=driver.find_element_by_link_text(text.strip())
    return element.get_attribute("href")


category_links={x:get_link_by_text(x) for x in  get_list_by_className('recipe-tab-heading') if x=='CATEGORIES'}

#print(category_links)
#print("#"*25)


sub_category_links={}

for category,url in category_links.items():
    driver.get(url) # this will open url in firefox

    sub_category_list=get_list_by_className("main_image")
    sub_category_links[category]={x:get_link_by_text(x) for x in sub_category_list if x=='SNACKS' }

#print(sub_category_links)
#print("/"*25)


#loop till show more doesn't have anything to load
def keep_clicking_show_more():
    #print("^"*25)
    while (True):
        try:
            element=driver.find_element_by_link_text('Show More')
            driver.execute_script("arguments[0].click();",element)
            
            #print("&"*25)
            #print(element)
            #element.click()
            '''
            wait till the container of the recipes gets loaded
            after load more is clicked
            '''
            time.sleep(5)

            recipe_container=driver.find_element_by_id("recipeListing")
            if 'No Record Found' in recipe_container.text:
                break
        except (NoSuchElementException,WebDriverException) as e:
            print(e)
            break
        except:
            break

all_recipe_links = {}

for category, urls in sub_category_links.items():
    if category == 'CHEFS':
        # we want to ignore chefs.
        continue
    elif category == 'MEMBER RECIPES':
        # there's no additional tree traversal for member recipes
        all_recipe_links[category] = {
            'dummy_sub_category': urls
        }
    else:
        all_recipe_links[category] = {}
        for sub_category, url in urls.items():
            try:
                driver.get(url)
                keep_clicking_show_more()
                all_recipe_links[category][sub_category] = {x: get_link_by_text(x) for x in get_list_by_className("main_image") }
            except KeyboardInterrupt as e:
                break
            except :
                break
driver.quit()

for category,sub_category in all_recipe_links.items():
    for ssub,dishurl in sub_category.items():
        for title,url in dishurl.items():
            cur.execute('INSERT or IGNORE into url (url) VALUES(?)',(url,))
            conn.commit()

cur.execute('SELECT url FROM url')
durl=list()
for row in cur:
    durl.append(str(row[0]))


recipes={}

for i in durl:
    rurl=Request(str(i), headers={'User-Agent': 'Mozilla/5.0'})
    document=urlopen(rurl,context=ctx)
    html=document.read()
    if document.getcode()!=200:
        print(str(i) + " " + "Has error")
        continue
    soup=BeautifulSoup(html,'html.parser')
    recipe_container = soup.find("div", {"class": "recp-det-cont"})

    # name was in h1 html tag inside recipe container div
    name = recipe_container.find('h1').get_text().strip()

    #image
    image = recipe_container.find('div', {'class': 'art_imgwrap'}).img['src']

    # ingredients
    recipe_ingredients = recipe_container.find('div', {"class": "ingredients"})
    ingredients = [x.get_text().strip()    for x in recipe_ingredients.find_all('li')]

    # instructions
    recipe_method = recipe_container.find('div', {"class": "method"})
    instructions = [x.get_text().strip()    for x in recipe_method.find_all('li')]

    #details
    recipe_details=recipe_container.find('div',{"class":"recipe-details"})
    details=[x.get_text().strip().split(' ')  for x in recipe_details.find_all('li')]

    recipes[name]={'Difficulty Level':details[5][2], 'Recipe Serving':details[1][2], 'Prep Time':details[2][3]+' '+details[2][4], 'Cook Time':details[3][3]+' '+details[3][4], 'Souce url':str(i),  'Image source':str(image) , 'Ingredients':ingredients, 'Instructions':instructions}

with open('dish.json','w') as fp:
    json.dump(recipes,fp,indent=4)

#print(recipes)




