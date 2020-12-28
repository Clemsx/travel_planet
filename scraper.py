import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

class Scraper():
    
    def __init__(self, url):
        self.url = url
        self.list_links = []
        self.airlines_df = pd.DataFrame()
    
    def get_url(self):
        # Get HTML content
        res = requests.get(self.url)
        html_text = res.content
        
        # Get all links in the first DIV only
        bsoup = BeautifulSoup(html_text, 'html.parser')
        links = bsoup.find('div')
        hrefs_text = links.find_all('a')
                
        # Append link to list_links
        for link in hrefs_text:
            print("Link found -> ",link['href'])
            self.list_links.append(link['href'])
        
    def get_tables_content(self):
        # Iterable each links to get data tables        
        for link in self.list_links:
            tmp_df = pd.read_html("http://www.al-airliners.be/codes/" + link)
            
            if len(tmp_df[0].columns) < 7:
                # Because read_html returns a list of DF 
                tmp_df[0] = pd.concat([tmp_df[0], tmp_df[1]])
                tmp_df[0].insert(loc = 0, column = np.nan, value = np.nan)
            
            # Get the first row for the name
            headers = tmp_df[0].iloc[0]
            new_df = pd.DataFrame(tmp_df[0].values[1:], columns=headers)
            new_df.columns = new_df.columns.fillna('Id')
            print(new_df)
            
            self.airlines_df = self.airlines_df.append(new_df, ignore_index = True)
            
        self.airlines_df = self.airlines_df.sort_values('Id', ascending = True)
        self.airlines_df = self.airlines_df.set_index(['Id'])
    
    def df_to_csv(self):
        self.airlines_df.to_csv('airlines_code.csv')

        
if __name__ == "__main__":
    
    print("--- Starting scraper ---")
    scraper = Scraper(url = "http://www.al-airliners.be/codes/oaci-01.htm")
    
    print("--- GET URL ---")
    scraper.get_url()
    
    print("--- GET TABLES CONTENT ---")
    scraper.get_tables_content()
    
    print("--- CONVERT DATA TO CSV ---")
    scraper.df_to_csv()
    
    print("--- Scraping finished ---")