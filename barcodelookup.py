#Barcode UPC Lookup using webscrape (c)2019 Rendy Zhang
#Install procedure
#sudo apt-get install software-properties-common
#sudo python3 -m pip install tabulate
#sudo apt-get install python3-bs4
#sudo apt-get install python3-requests

import requests
from bs4 import BeautifulSoup
import time
from tabulate import tabulate

while True:
    #upc lookup url (upc database)
    url="https://www.upcdatabase.com/item/"

    upc=input()

    global lookup_url
    lookup_url=url+upc

    response=requests.get(lookup_url)
    html_doc=response.text
    
    def scraper():
        #First print the UPC number
        #get the html response using requests
        response=requests.get(lookup_url)
        html_doc=response.text
        #website soup'ed
        soupypage=BeautifulSoup(html_doc,"html.parser")
        prettysoupypage=soupypage.prettify()
        #scrape based on tags
        itemdescription=soupypage.find({"table"},attrs={"class":"data"})
        if itemdescription != None:
            itemdescription=itemdescription.text.strip()
        else:
            itemdescription="Not found!"
    


        print (itemdescription)

    scraper()
