from api.geocoder import Geocoder
from api.models import Article
import requests as rq
from bs4 import BeautifulSoup
import lxml
import cchardet
from newspaper import Article

class CrawlerCNN:
    """ month_string example: 2022-3 """
    @staticmethod
    def get_articles_from_month(db, month_string: str):
        geocoder = Geocoder()
        
        sitemap_base_url = "https://edition.cnn.com/article/sitemap-"
        requests_session = rq.Session()
        sitemap_url = sitemap_base_url + month_string + ".html"
        response = requests_session.get(sitemap_url)
        
        if response.status_code == 404:
            print("Wrong CNN sitemap URL: " + sitemap_url)
            return []
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        document = {"date": "", "locations": []}
        previous_date_string = ""
        
        articles_list_elements = soup.find_all("div", {"class": "sitemap-entry"})[1].find("ul").find_all("li" , recursive=False)
        for article_list_element in articles_list_elements:
            date_string = article_list_element.find("span", {"class": "date"}).getText()
            heading = article_list_element.find("span", {"class": "sitemap-link"}).find("a").getText()
            link = article_list_element.find("span", {"class": "sitemap-link"}).find("a")['href']
        
            
            # TODO nicht so  wichtig aber maybe ARTICLE TEXT SELBER GETTEN (RECURSIVE), nespaper package incomplete, missing after "READ MORE"
            article = Article(link)
            article.download()
            article.parse()
            
            print(date_string)
            
            if date_string != previous_date_string and previous_date_string != "":
                db.cnn.replace_one({'date': document['date']}, document, upsert=True)
                document = {"date": "", "locations": []}
            
            # print(heading)
            
            article_locations = []
            article_locations = article_locations + geocoder.get_all_locations(heading)
            article_locations = article_locations + geocoder.get_all_locations(article.text)
            
            if date_string == document["date"]:
                existing_locations = document["locations"]
                existing_locations = existing_locations + article_locations
                document["locations"] = existing_locations
            else:
                document["date"] = date_string
                document["locations"] = article_locations
                
            previous_date_string = date_string
                
        db.cnn.replace_one({'date': document['date']}, document, upsert=True)