import time
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from status.models import ScrapedData

class Command(BaseCommand):
    help = "Scrapes target static website every 5 minutes"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Scraper started..."))
        
        #url of the site to be scraped

        URL = "https://quotes.toscrape.com/" 

        while True:
            try:
                self.stdout.write(f"Fetching data from  {URL}")

                response = requests.get(URL, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')


                   
                   # this will extract the title and the text from the websites html
                   
                    quote_blocks = soup.find_all('div',class_='quote')
                    if not quote_blocks:
                        self.stdout.write(self.style.WARNING("No blocks found"))
                        continue

                    self.stdout.write(self.style.SUCCESS(f"Found {len (quote_blocks)} quotes. Saving to db"))

                    for block in quote_blocks:
                        text_element=block.find('span', class_='text')
                        author_element=block.find('small', class_='author')
                         
                        if text_element and author_element:
                            quote_text=text_element.text.strip()
                            author_name=author_element.text.strip()

                            ScrapedData.objects.create(title=author_name, value=quote_text)

                    self.stdout.write(self.style.SUCCESS("Saved successfuly!"))         
                   
                    """
                    title_element = soup.find('h1')
                    body_element = soup.find('p')

                    title = title_element.text.strip() if title_element else "No Title Found"

                    value = body_element.text.strip() if body_element else "No Content Found"

                    #savign to db

                    ScrapedData.objects.create(title=title, value=value)
                    self.stdout.write(self.style.SUCCESS(f"Successfully saved: {title}"))
                    
                     """




                else: self.stdout.write(self.style.WARNING(f"Failed to fetch the data/site, status code: {response.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error occurred: {str(e)}"))        

            self.stdout.write("Will run again in 5 mins")
            time.sleep(300)    

