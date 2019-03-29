#Barcode UPC Lookup using webscrape (c)2019 Rendy Zhang
#Install procedure
#sudo apt-get install software-properties-common
#sudo apt-get install python3-bs4


from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup
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
        itemdescription=soupypage.find("table",{"class":"data"}).findAll("tr")[2].findAll("td")[2].text
        sizeweight=soupypage.find("table",{"class":"data"}).findAll("tr")[3].findAll("td")[2].text
        country=soupypage.find("table",{"class":"data"}).findAll("tr")[4].findAll("td")[2].text
        print("UPC:" +upc)
        print("The item is: " + itemdescription)
        print("Size and weight of: " + sizeweight)
        print("From country: " +country)
        now = datetime.datetime.now()
        print ("Current date and time : " + now.strftime("%Y-%m-%d %H:%M:%S"))
    scraper()


