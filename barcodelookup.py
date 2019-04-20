#Barcode UPC Lookup using webscrape (c)2019 Rendy Zhang
#Install procedure
#sudo apt-get install software-properties-common
#sudo apt-get install python3-bs4

import urllib
from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup
from Naked.toolshed.shell import execute_js, muterun_js, run_js
import datetime
url="https://www.upcdatabase.com/item/"


while True:
    upc=input()
    global lookup_url
    lookup_url=url+upc
    
    def scraper():
        response=req(lookup_url)
        html_page=response.read()
        response.close()
        #website soup'ed
        soupypage=soup(html_page,"html.parser")
        #making sure the UPC is valid and also exists in the database
        check=soupypage.h2.text
        if (check=="Item Not Found") or (check=="UPC Error"):
            return
        #scrape based on tags
        itemdescription3=str(soupypage.find("table",{"class":"data"}).findAll("tr")[3].findAll("td"))
        itemdescription2=str(soupypage.find("table",{"class":"data"}).findAll("tr")[2].findAll("td"))
    
        
        if (itemdescription3.find("Description",0,len(itemdescription3)))!=-1:
            itemdescription=soupypage.find("table",{"class":"data"}).findAll("tr")[3].findAll("td")[2].text
            print("hi")
        elif (itemdescription2.find("Description",0,len(itemdescription2)))!=-1:
            itemdescription=soupypage.find("table",{"class":"data"}).findAll("tr")[2].findAll("td")[2].text
            print("he")
        else:
            itemdescription=soupypage.find("table",{"class":"data"}).findAll("tr")[1].findAll("td")[2].text
            print("ho")
        
        print("UPC:" +upc)
        print("The item is: " + itemdescription)
        muterun_js('node/index.js', "'" + itemdescription.lower() + "'")
        #if success:
         #   print("success")
        #else:
        #    print("fail")
        now = datetime.datetime.now()
        print ("Current date and time : " + now.strftime("%Y-%m-%d %H:%M:%S"))
    scraper()


